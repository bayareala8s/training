#!/usr/bin/env bash
# Report whether course lab resources are running and estimate cost risk.
set -euo pipefail

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TF_DIR="${REPO_ROOT}/infrastructure/environments/dev"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

RUNNING=0
STOPPED=0
WARN=0

ok_stopped() { echo -e "  ${GREEN}○${NC} $1 (not running)"; STOPPED=$((STOPPED + 1)); }
ok_running() { echo -e "  ${GREEN}●${NC} $1"; RUNNING=$((RUNNING + 1)); }
warn_item()  { echo -e "  ${YELLOW}!${NC} $1"; WARN=$((WARN + 1)); }
bad_item()   { echo -e "  ${RED}●${NC} $1"; RUNNING=$((RUNNING + 1)); }

echo "=== CNDE Lab Environment Status ==="
echo "Region: ${AWS_REGION}"
echo "Account: $(aws sts get-caller-identity --query Account --output text 2>/dev/null || echo 'N/A')"
echo

# Terraform state
echo "Core infrastructure (Terraform):"
BUCKET=$(terraform -chdir="$TF_DIR" output -raw data_lake_bucket 2>/dev/null || echo "")
if [[ -n "$BUCKET" ]] && aws s3api head-bucket --bucket "$BUCKET" &>/dev/null; then
  bad_item "S3 data lake: ${BUCKET}"
  GLUE_JOB=$(terraform -chdir="$TF_DIR" output -raw glue_job_name 2>/dev/null || echo "")
  [[ -n "$GLUE_JOB" ]] && aws glue get-job --job-name "$GLUE_JOB" &>/dev/null && bad_item "Glue job: ${GLUE_JOB}" || true
  SFN=$(terraform -chdir="$TF_DIR" output -raw state_machine_name 2>/dev/null || echo "")
  [[ -n "$SFN" ]] && aws stepfunctions list-state-machines --query "stateMachines[?name=='${SFN}'].name" --output text 2>/dev/null | grep -q . && bad_item "Step Functions: ${SFN}" || true
  while IFS= read -r fn; do
    [[ -z "$fn" ]] && continue
    aws lambda get-function --function-name "$fn" &>/dev/null && bad_item "Lambda: ${fn}" || true
  done < <(terraform -chdir="$TF_DIR" output -json lambda_function_names 2>/dev/null | python3 -c 'import json,sys; [print(x) for x in json.load(sys.stdin)]' 2>/dev/null || true)
else
  ok_stopped "Terraform stack (S3, Lambda, Glue, Step Functions, monitoring)"
fi

echo
echo "Lab extras (outside Terraform):"
KMS=$(aws kms describe-key --key-id alias/cnde-dev-datalake-key --query 'KeyMetadata.{Id:KeyId,State:KeyState}' --output text 2>/dev/null || echo "")
if [[ -n "$KMS" && "$KMS" != "None" ]]; then
  warn_item "KMS key (Lab 7.1): ${KMS} — ~\$1/mo until deleted"
else
  ok_stopped "KMS key (Lab 7.1)"
fi

IAM_COUNT=0
for ROLE in cnde-dev-analyst-curated cnde-dev-engineer-pipeline cnde-dev-steward-quarantine; do
  aws iam get-role --role-name "$ROLE" &>/dev/null && IAM_COUNT=$((IAM_COUNT + 1)) || true
done
if [[ $IAM_COUNT -gt 0 ]]; then
  warn_item "IAM roles (Lab 7.2): ${IAM_COUNT} role(s) present"
else
  ok_stopped "IAM roles (Lab 7.2)"
fi

LOG_COUNT=$(aws logs describe-log-groups --log-group-name-prefix /aws/lambda/cnde-dev- \
  --query 'length(logGroups)' --output text 2>/dev/null || echo 0)
if [[ "${LOG_COUNT}" != "0" && "${LOG_COUNT}" != "None" ]]; then
  warn_item "CloudWatch log groups: ${LOG_COUNT} Lambda log group(s) (~\$0)"
else
  ok_stopped "CloudWatch log groups"
fi

echo
echo "--- Summary ---"
if [[ $RUNNING -eq 0 && $WARN -eq 0 ]]; then
  echo -e "${GREEN}STOPPED${NC} — No course resources detected. No ongoing charges expected."
  echo "Start labs: ./scripts/lab-cycle.sh start"
elif [[ $RUNNING -gt 0 ]]; then
  echo -e "${YELLOW}RUNNING${NC} — ${RUNNING} billable resource group(s) active."
  echo "Stop labs:  ./scripts/lab-cycle.sh stop"
  echo "Demo guide: docs/LAB-DEMO-GUIDE.md"
else
  echo -e "${YELLOW}PARTIAL${NC} — Core stack stopped; ${WARN} extra item(s) may incur small charges."
  echo "Full stop:  ./scripts/lab-cycle.sh stop"
fi
echo
echo "Schedules: disabled by default (enable_schedules=false in terraform.tfvars)"
echo "Glue/Step Functions only run when you start them manually."
