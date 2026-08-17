#!/usr/bin/env bash
# Cleanup Lab 05 — Cloud Platform Foundation (BayLearn)
# Destroys Terraform-managed resources for environments/lab05.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_DIR="${ROOT}/environments/lab05"

echo "==> BayLearn Lab 05 cleanup"
echo "    Environment: ${ENV_DIR}"

if [[ ! -d "${ENV_DIR}" ]]; then
  echo "ERROR: lab05 environment not found" >&2
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

echo "==> terraform destroy"
terraform destroy -auto-approve -input=false

echo "==> Optional: list residual BayLearn Module=05 resources (manual review)"
if command -v aws >/dev/null 2>&1; then
  aws resourcegroupstaggingapi get-resources \
    --tag-filters Key=Project,Values=BayLearn Key=Module,Values=05 \
    --query 'ResourceTagMappingList[].ResourceARN' \
    --output text 2>/dev/null || true
fi

echo "==> Lab 05 cleanup complete. Confirm AWS Budgets and S3 buckets in console."
