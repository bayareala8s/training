#!/usr/bin/env bash
# Terraform helpers for pause/resume (NAT Gateway destroy/recreate).

terraform_lab_repo_root() {
  cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd
}

terraform_lab_env_dir() {
  local env="$1"
  echo "$(terraform_lab_repo_root)/labs/shared/environments/${env}"
}

terraform_lab_ensure_provider() {
  local dir="$1"
  local aws_scripts="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  if terraform -chdir="$dir" init -backend=false -input=false 2>/dev/null; then
    return 0
  fi
  log INFO "terraform init failed — trying local provider install"
  if [[ -x "${aws_scripts}/install-provider.sh" ]]; then
    "${aws_scripts}/install-provider.sh" "${AWS_PROVIDER_VERSION:-5.90.0}"
    export TF_CLI_CONFIG_FILE="${TF_CLI_CONFIG_FILE:-/tmp/terraform-lab.rc}"
    terraform -chdir="$dir" init -backend=false -input=false
  else
    return 1
  fi
}

terraform_lab_backend_file() {
  local dir="$1"
  if [[ -f "${dir}/backend.hcl" ]]; then
    echo "${dir}/backend.hcl"
  elif [[ -f "${dir}/backend.hcl.example" ]]; then
    echo "${dir}/backend.hcl.example"
  else
    return 1
  fi
}

terraform_lab_tfvars_file() {
  local dir="$1"
  if [[ -f "${dir}/terraform.tfvars" ]]; then
    echo "${dir}/terraform.tfvars"
  elif [[ -f "${dir}/terraform.tfvars.example" ]]; then
    echo "${dir}/terraform.tfvars.example"
  else
    return 1
  fi
}

terraform_lab_init_backend() {
  local env="$1"
  local dir
  dir="$(terraform_lab_env_dir "$env")"
  local backend tfvars
  backend="$(terraform_lab_backend_file "$dir")" || { log ERROR "No backend config for $env"; return 1; }
  tfvars="$(terraform_lab_tfvars_file "$dir")" || { log ERROR "No tfvars for $env"; return 1; }

  export TF_VAR_FILE="$tfvars"
  terraform_lab_ensure_provider "$dir" || return 1
  terraform -chdir="$dir" init -backend-config="$backend" -input=false -reconfigure
}

terraform_lab_nat_gateway_exists() {
  local env="$1"
  aws ec2 describe-nat-gateways --region "$AWS_REGION" \
    --filter "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
             "Name=tag:Environment,Values=${env}" \
             "Name=state,Values=available,pending,deleting" \
    --query 'length(NatGateways)' --output text 2>/dev/null | grep -qv '^0$'
}

terraform_lab_destroy_nat_gateway() {
  local env="$1"
  local dir targets
  dir="$(terraform_lab_env_dir "$env")"

  if ! terraform_lab_nat_gateway_exists "$env"; then
    log INFO "NAT Gateway (${env}): none active — skip destroy"
    return 0
  fi

  log INFO "NAT Gateway (${env}): destroying via Terraform (cannot be stopped)"
  terraform_lab_init_backend "$env" || return 1

  targets=(
    -target=module.vpc.aws_nat_gateway.this[0]
    -target=module.vpc.aws_eip.nat[0]
  )

  if [[ "$DRY_RUN" == "1" ]]; then
    log INFO "[DRY-RUN] terraform destroy ${targets[*]} -var-file=..."
    return 0
  fi

  terraform -chdir="$dir" destroy \
    -var-file="$(terraform_lab_tfvars_file "$dir")" \
    "${targets[@]}" \
    -auto-approve -input=false
}

terraform_lab_apply_env() {
  local env="$1"
  local dir
  dir="$(terraform_lab_env_dir "$env")"

  log INFO "Terraform apply (${env})"
  terraform_lab_init_backend "$env" || return 1

  if [[ "$DRY_RUN" == "1" ]]; then
    log INFO "[DRY-RUN] terraform apply -var-file=... ($env)"
    return 0
  fi

  terraform -chdir="$dir" apply \
    -var-file="$(terraform_lab_tfvars_file "$dir")" \
    -auto-approve -input=false
}

terraform_lab_apply_if_nat_missing() {
  local env="$1"
  if terraform_lab_nat_gateway_exists "$env"; then
    log INFO "NAT Gateway (${env}): already present"
    return 0
  fi

  # Only prod uses NAT Gateway in default course tfvars
  local tfvars
  tfvars="$(terraform_lab_tfvars_file "$(terraform_lab_env_dir "$env")")"
  if ! grep -q 'enable_nat_gateway\s*=\s*true' "$tfvars" 2>/dev/null; then
    log INFO "NAT Gateway (${env}): not configured in tfvars — skip apply"
    return 0
  fi

  terraform_lab_apply_env "$env"
}
