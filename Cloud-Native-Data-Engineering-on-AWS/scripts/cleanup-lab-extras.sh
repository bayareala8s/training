#!/usr/bin/env bash
# Remove AWS resources created outside Terraform (Module 7 labs, log groups, etc.)
set -euo pipefail

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TF_DIR="${REPO_ROOT}/infrastructure/environments/dev"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[cleanup]${NC} $*"; }
warn() { echo -e "${YELLOW}[cleanup]${NC} $*"; }

# ---------------------------------------------------------------------------
# Module 7: IAM roles created during Lab 7.2 demos
# ---------------------------------------------------------------------------
cleanup_iam_roles() {
  log "Removing Lab 7.2 IAM roles (if present)..."
  for PAIR in "cnde-dev-analyst-curated:analyst-curated-read" \
              "cnde-dev-engineer-pipeline:engineer-pipeline-write" \
              "cnde-dev-steward-quarantine:steward-quarantine"; do
    ROLE="${PAIR%%:*}"
    POLICY="${PAIR##*:}"
    aws iam delete-role-policy --role-name "$ROLE" --policy-name "$POLICY" 2>/dev/null || true
    aws iam delete-role --role-name "$ROLE" 2>/dev/null || true
  done
}

# ---------------------------------------------------------------------------
# Module 7: KMS key from Lab 7.1 (customer-managed keys incur ~$1/mo until deleted)
# ---------------------------------------------------------------------------
cleanup_kms_keys() {
  log "Scheduling Lab 7.1 KMS key deletion (7-day minimum)..."
  local alias kms_alias="alias/cnde-dev-datalake-key"
  local key_id

  key_id=$(aws kms describe-key --key-id "$kms_alias" --query 'KeyMetadata.KeyId' --output text 2>/dev/null || echo "")
  if [[ -z "$key_id" || "$key_id" == "None" ]]; then
    warn "No KMS alias ${kms_alias} — skipping"
    return 0
  fi

  local state
  state=$(aws kms describe-key --key-id "$key_id" --query 'KeyMetadata.KeyState' --output text 2>/dev/null || echo "")

  if [[ "$state" == "PendingDeletion" ]]; then
    warn "KMS key ${key_id} already pending deletion"
    return 0
  fi

  aws kms delete-alias --alias-name "$kms_alias" 2>/dev/null || true
  aws kms disable-key --key-id "$key_id" 2>/dev/null || true
  aws kms schedule-key-deletion --key-id "$key_id" --pending-window-in-days 7 2>/dev/null \
    && log "KMS key ${key_id} scheduled for deletion in 7 days" \
    || warn "Could not schedule KMS key deletion (may be in use)"
}

# ---------------------------------------------------------------------------
# Leftover CloudWatch log groups (Lambda/SFN retain after destroy)
# ---------------------------------------------------------------------------
cleanup_log_groups() {
  log "Removing course CloudWatch log groups..."
  local prefixes=(
    "/aws/lambda/cnde-dev-"
    "/aws/vendedlogs/states/cnde-dev-"
    "/aws-glue/jobs/cnde-"
  )
  for prefix in "${prefixes[@]}"; do
    while IFS= read -r lg; do
      [[ -z "$lg" ]] && continue
      aws logs delete-log-group --log-group-name "$lg" 2>/dev/null \
        && log "Deleted log group: ${lg}" \
        || warn "Could not delete log group: ${lg}"
    done < <(aws logs describe-log-groups --log-group-name-prefix "$prefix" \
      --query 'logGroups[].logGroupName' --output text 2>/dev/null | tr '\t' '\n')
  done
}

# ---------------------------------------------------------------------------
# SNS subscriptions / topics not in Terraform (should be destroyed by TF)
# ---------------------------------------------------------------------------
cleanup_orphan_sns() {
  log "Checking for orphan CNDE SNS topics..."
  while IFS= read -r arn; do
    [[ -z "$arn" ]] && continue
    warn "Orphan SNS topic still exists: ${arn} (delete manually if needed)"
  done < <(aws sns list-topics --query "Topics[?contains(TopicArn, 'cnde-dev')].TopicArn" --output text 2>/dev/null | tr '\t' '\n')
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
  cleanup_iam_roles
  cleanup_kms_keys
  cleanup_log_groups
  cleanup_orphan_sns
  log "Extra resource cleanup complete."
}

main "$@"
