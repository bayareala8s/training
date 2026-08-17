#!/usr/bin/env bash
# Verify course labs on AWS: validate Terraform, apply dev, test start/stop, teardown.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DEV_DIR="${REPO_ROOT}/labs/shared/environments/dev"
AWS_SCRIPTS="${REPO_ROOT}/scripts/aws"
export AWS_REGION="${AWS_REGION:-us-west-2}"
AWS_PROVIDER_VERSION="${AWS_PROVIDER_VERSION:-5.90.0}"

log() { echo "[$(date +%H:%M:%S)] $*"; }

require_files() {
  [[ -f "${DEV_DIR}/backend.hcl" ]] || { echo "Missing ${DEV_DIR}/backend.hcl — copy from backend.hcl.example"; exit 1; }
  [[ -f "${DEV_DIR}/terraform.tfvars" ]] || { echo "Missing ${DEV_DIR}/terraform.tfvars — copy from terraform.tfvars.example"; exit 1; }
}

ensure_provider() {
  # Some environments block Terraform's provider registry queries. If init fails,
  # install the AWS provider into a local filesystem mirror and retry.
  local init_args=("$@")
  if terraform init "${init_args[@]}"; then
    return 0
  fi

  log "terraform init failed — attempting local provider install (aws ${AWS_PROVIDER_VERSION})"
  chmod +x "${AWS_SCRIPTS}/install-provider.sh" 2>/dev/null || true
  "${AWS_SCRIPTS}/install-provider.sh" "${AWS_PROVIDER_VERSION}"
  export TF_CLI_CONFIG_FILE="${TF_CLI_CONFIG_FILE:-/tmp/terraform-lab.rc}"

  terraform init "${init_args[@]}"
}

step_validate() {
  log "=== Step 1: Terraform fmt & validate (all environments) ==="
  cd "${REPO_ROOT}"
  terraform fmt -recursive modules labs
  for env in dev test prod; do
    log "Validating ${env}..."
    cd "${REPO_ROOT}/labs/shared/environments/${env}"
    ensure_provider -backend=false -input=false
    terraform validate
  done
}

step_apply_dev() {
  log "=== Step 2: Apply dev environment ==="
  cd "${DEV_DIR}"

  # Pre-clean: a previous failed run may have left the flow log group unmanaged
  # (not in Terraform state). If it exists, creation will fail with
  # ResourceAlreadyExistsException.
  if aws logs describe-log-groups --log-group-name-prefix "/vpc/bal8s-tf-dev-flow-logs" \
      --query 'length(logGroups)' --output text 1>/dev/null 2>&1; then
    if aws logs describe-log-groups --log-group-name-prefix "/vpc/bal8s-tf-dev-flow-logs" \
        --query 'logGroups[?logGroupName==`/vpc/bal8s-tf-dev-flow-logs`].logGroupName' --output text 2>/dev/null \
        | grep -q "/vpc/bal8s-tf-dev-flow-logs"; then
      log "Pre-clean: deleting existing log group /vpc/bal8s-tf-dev-flow-logs"
      aws logs delete-log-group --log-group-name "/vpc/bal8s-tf-dev-flow-logs" 2>/dev/null || true
    fi
  fi

  ensure_provider -backend-config=backend.hcl -input=false
  terraform plan -var-file=terraform.tfvars -input=false -out=/tmp/tf-dev.plan
  terraform apply -input=false /tmp/tf-dev.plan
  terraform output
}

step_test_start_stop() {
  log "=== Step 3: Test start/stop scripts ==="
  chmod +x "${AWS_SCRIPTS}"/*.sh "${AWS_SCRIPTS}"/lib/*.sh
  "${AWS_SCRIPTS}/status-lab.sh"
  log "Stopping lab instances..."
  "${AWS_SCRIPTS}/stop-lab.sh" --all
  sleep 15
  "${AWS_SCRIPTS}/status-lab.sh"
  log "Starting lab instances..."
  "${AWS_SCRIPTS}/start-lab.sh" --all
  sleep 20
  "${AWS_SCRIPTS}/status-lab.sh"
}

step_teardown() {
  log "=== Step 4: Teardown (destroy dev + stop) ==="
  "${AWS_SCRIPTS}/stop-lab.sh" --all || true
  cd "${DEV_DIR}"
  terraform destroy -var-file=terraform.tfvars -auto-approve -input=false
  log "Dev environment destroyed. State bucket retained."
}

main() {
  require_files
  aws sts get-caller-identity
  case "${1:-all}" in
    validate) step_validate ;;
    apply)    step_validate; step_apply_dev ;;
    test)     step_test_start_stop ;;
    teardown) step_teardown ;;
    all)
      step_validate
      step_apply_dev
      step_test_start_stop
      step_teardown
      ;;
    *)
      echo "Usage: $0 [validate|apply|test|teardown|all]"
      exit 1
      ;;
  esac
  log "Done."
}

main "$@"
