#!/usr/bin/env bash
# Tear down all course lab infrastructure from AWS.
set -euo pipefail

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true

export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TF_DIR="${REPO_ROOT}/infrastructure/environments/dev"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[stop-labs]${NC} $*"; }
warn() { echo -e "${YELLOW}[stop-labs]${NC} $*"; }
err()  { echo -e "${RED}[stop-labs]${NC} $*" >&2; }

# ---------------------------------------------------------------------------
# Empty S3 bucket (required before Terraform can delete it)
# ---------------------------------------------------------------------------
empty_bucket() {
  local bucket
  bucket="$(terraform -chdir="${TF_DIR}" output -raw data_lake_bucket 2>/dev/null || true)"

  if [[ -z "${bucket}" ]]; then
    warn "No data lake bucket in state — skipping S3 cleanup"
    return 0
  fi

  log "Emptying S3 bucket: ${bucket}"

  # Delete all object versions (versioning is enabled on the data lake)
  aws s3api list-object-versions --bucket "${bucket}" --output json \
    | python3 -c "
import json, sys, subprocess
data = json.load(sys.stdin)
to_delete = []
for v in data.get('Versions', []) + data.get('DeleteMarkers', []):
    to_delete.append({'Key': v['Key'], 'VersionId': v['VersionId']})
if not to_delete:
    sys.exit(0)
# Delete in batches of 1000
for i in range(0, len(to_delete), 1000):
    batch = {'Objects': to_delete[i:i+1000], 'Quiet': True}
    subprocess.run(['aws', 's3api', 'delete-objects', '--bucket', '${bucket}',
                    '--delete', json.dumps(batch)], check=True)
" 2>/dev/null || {
    warn "Versioned delete failed — trying simple recursive delete"
    aws s3 rm "s3://${bucket}" --recursive || true
  }

  log "S3 bucket emptied."
}

# ---------------------------------------------------------------------------
# Terraform destroy
# ---------------------------------------------------------------------------
destroy_terraform() {
  log "Destroying Terraform infrastructure..."
  cd "${TF_DIR}"

  if [[ ! -d .terraform ]]; then
    terraform init
  fi

  # Only destroy if state exists
  if ! terraform state list &>/dev/null || [[ -z "$(terraform state list 2>/dev/null)" ]]; then
    warn "No Terraform state found — nothing to destroy"
    return 0
  fi

  empty_bucket

  terraform destroy -auto-approve
  log "All lab resources destroyed."
}

# ---------------------------------------------------------------------------
# Cleanup local artifacts
# ---------------------------------------------------------------------------
cleanup_local() {
  log "Cleaning local build artifacts..."
  find "${REPO_ROOT}/infrastructure/modules" -type d -name build -exec rm -rf {} + 2>/dev/null || true
  rm -f "${TF_DIR}/tfplan" /tmp/cnde-lambda-response.json 2>/dev/null || true
  log "Local cleanup complete."
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
  if ! command -v aws &>/dev/null || ! command -v terraform &>/dev/null; then
    err "aws and terraform are required"
    exit 1
  fi

  if ! aws sts get-caller-identity &>/dev/null; then
    err "AWS credentials not configured"
    exit 1
  fi

  warn "This will DELETE all course lab AWS resources."
  if [[ "${1:-}" != "--yes" ]]; then
    read -r -p "Continue? [y/N] " confirm
    if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
      log "Aborted."
      exit 0
    fi
  fi

  destroy_terraform
  cleanup_local
  log "=== Lab environment stopped. No ongoing AWS charges from course resources. ==="
  log "Run ./scripts/cleanup-lab-extras.sh if you used Module 7 labs (KMS/IAM)."
  log "Or use: ./scripts/lab-cycle.sh stop --yes  (includes full cleanup)"
}

main "$@"
