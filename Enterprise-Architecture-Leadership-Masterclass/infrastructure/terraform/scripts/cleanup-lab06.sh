#!/usr/bin/env bash
# Cleanup Lab 06 — Integration Platform (BayLearn)
# Destroys Terraform-managed resources for environments/lab06.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_DIR="${ROOT}/environments/lab06"

echo "==> BayLearn Lab 06 cleanup"
echo "    Environment: ${ENV_DIR}"

if [[ ! -d "${ENV_DIR}" ]]; then
  echo "ERROR: lab06 environment not found" >&2
  exit 1
fi

cd "${ENV_DIR}"

if [[ ! -f terraform.tfvars && ! -f terraform.tfvars.json ]]; then
  echo "WARNING: No terraform.tfvars found. Destroy may prompt for variables."
fi

if [[ ! -d .terraform ]]; then
  echo "==> terraform init"
  terraform init -input=false
fi

# Empty partner bucket if force_destroy somehow fails mid-run
if command -v aws >/dev/null 2>&1 && [[ -f terraform.tfstate || -d .terraform ]]; then
  BUCKET="$(terraform output -raw partner_bucket_name 2>/dev/null || true)"
  if [[ -n "${BUCKET}" ]]; then
    echo "==> Emptying partner bucket ${BUCKET} (best effort)"
    aws s3 rm "s3://${BUCKET}" --recursive 2>/dev/null || true
  fi
fi

echo "==> terraform destroy"
terraform destroy -auto-approve -input=false

echo "==> Optional: list residual BayLearn Module=06 resources (manual review)"
if command -v aws >/dev/null 2>&1; then
  aws resourcegroupstaggingapi get-resources \
    --tag-filters Key=Project,Values=BayLearn Key=Module,Values=06 \
    --query 'ResourceTagMappingList[].ResourceARN' \
    --output text 2>/dev/null || true
fi

echo "==> Lab 06 cleanup complete. Confirm SNS subscriptions cancelled and queues gone."
