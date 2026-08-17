#!/usr/bin/env bash
# cleanup-lab08.sh — Destroy BayLearn Module 08 lab resources
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ENV_DIR="${ROOT}/infrastructure/terraform/environments/lab08"

echo "=== BayLearn Lab 08 cleanup ==="
echo "Environment: ${ENV_DIR}"
echo "Fiction notice: NorthStar AI lab resources only."

cd "${ENV_DIR}"

if [[ ! -d .terraform && ! -f .terraform.lock.hcl ]]; then
  terraform init -input=false
fi

BUCKET="$(terraform output -raw artifacts_bucket 2>/dev/null || true)"
REGION="$(grep -E '^aws_region' terraform.tfvars 2>/dev/null | cut -d'"' -f2 || echo us-east-1)"

if [[ -n "${BUCKET}" && "${BUCKET}" != "null" ]] && command -v aws >/dev/null 2>&1; then
  echo "Emptying s3://${BUCKET}..."
  aws s3 rm "s3://${BUCKET}" --recursive --region "${REGION}" || true
fi

echo "Running terraform destroy..."
terraform destroy -auto-approve

echo "=== Cleanup complete ==="
echo "Verify: no Module=08 API Gateway, Lambda, Step Functions, DynamoDB, or S3 lab resources remain."
