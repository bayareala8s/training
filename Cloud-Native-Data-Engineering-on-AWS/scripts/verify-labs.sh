#!/usr/bin/env bash
# Verify course lab infrastructure is deployed and healthy.
set -uo pipefail

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true

export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TF_DIR="${REPO_ROOT}/infrastructure/environments/dev"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

pass=0
fail=0

check() {
  local label="$1"
  shift
  if "$@" &>/dev/null; then
    echo -e "${GREEN}✓${NC} ${label}"
    pass=$((pass + 1))
  else
    echo -e "${RED}✗${NC} ${label}"
    fail=$((fail + 1))
  fi
}

cd "${TF_DIR}"

BUCKET="$(terraform output -raw data_lake_bucket 2>/dev/null || echo "")"
GLUE_JOB="$(terraform output -raw glue_job_name 2>/dev/null || echo "")"
SFN_ARN="$(terraform output -raw state_machine_arn 2>/dev/null || echo "")"
DASHBOARD="$(terraform output -raw dashboard_name 2>/dev/null || echo "")"

echo "=== Lab Infrastructure Verification (region: ${AWS_REGION}) ==="
echo

check "Terraform state exists" terraform state list
check "S3 data lake bucket exists" aws s3api head-bucket --bucket "${BUCKET}"
check "Glue job exists" aws glue get-job --job-name "${GLUE_JOB}"
check "Step Functions state machine exists" aws stepfunctions describe-state-machine --state-machine-arn "${SFN_ARN}"
check "CloudWatch dashboard exists" aws cloudwatch get-dashboard --dashboard-name "${DASHBOARD}"

while IFS= read -r fn; do
  [[ -z "${fn}" ]] && continue
  check "Lambda function: ${fn}" aws lambda get-function --function-name "${fn}"
done < <(terraform output -json lambda_function_names 2>/dev/null | python3 -c 'import json,sys; [print(x) for x in json.load(sys.stdin)]' 2>/dev/null || true)

QV="$(terraform output -raw quality_validation_lambda 2>/dev/null || echo "")"
check "Quality validation Lambda: ${QV}" aws lambda get-function --function-name "${QV}"

echo
echo "Results: ${pass} passed, ${fail} failed"

if [[ ${fail} -gt 0 ]]; then
  exit 1
fi
