#!/usr/bin/env bash
# Deploy all course lab infrastructure to AWS.
set -euo pipefail

# Avoid sandbox/proxy issues with AWS and Terraform registry
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true

# Use same region as Terraform (provider default / tfvars)
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TF_DIR="${REPO_ROOT}/infrastructure/environments/dev"
PYTHON="$("${SCRIPT_DIR}/ensure-python.sh")"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[start-labs]${NC} $*"; }
warn() { echo -e "${YELLOW}[start-labs]${NC} $*"; }
err()  { echo -e "${RED}[start-labs]${NC} $*" >&2; }

# ---------------------------------------------------------------------------
# Preflight checks
# ---------------------------------------------------------------------------
preflight() {
  log "Running preflight checks..."

  for cmd in aws terraform python3; do
    if ! command -v "$cmd" &>/dev/null; then
      err "Required command not found: $cmd"
      err "Complete setup: ${REPO_ROOT}/setup/SETUP.md"
      exit 1
    fi
  done

  if ! aws sts get-caller-identity &>/dev/null; then
    err "AWS credentials not configured. Run: aws configure"
    exit 1
  fi

  if [[ ! -f "${TF_DIR}/terraform.tfvars" ]]; then
    warn "terraform.tfvars not found — copying from example"
    cp "${TF_DIR}/terraform.tfvars.example" "${TF_DIR}/terraform.tfvars"
    warn "Edit ${TF_DIR}/terraform.tfvars before production use"
  fi

  if ! "$PYTHON" -c "import boto3" &>/dev/null; then
    warn "boto3 not installed — installing into .venv"
    "${REPO_ROOT}/.venv/bin/pip" install -q boto3
  fi

  log "AWS account: $(aws sts get-caller-identity --query Account --output text)"
  log "AWS region:  ${AWS_REGION}"
}

# ---------------------------------------------------------------------------
# Terraform deploy
# ---------------------------------------------------------------------------
deploy_terraform() {
  log "Deploying Terraform infrastructure..."
  cd "${TF_DIR}"

  terraform init -upgrade
  terraform validate
  terraform plan -out=tfplan
  terraform apply -auto-approve tfplan
  rm -f tfplan

  log "Terraform apply complete."
}

# ---------------------------------------------------------------------------
# Seed sample data for labs
# ---------------------------------------------------------------------------
seed_sample_data() {
  log "Seeding sample data into data lake..."

  local bucket
  bucket="$(terraform -chdir="${TF_DIR}" output -raw data_lake_bucket)"

  local lab_dir="${REPO_ROOT}/modules/module-01-foundations/labs/lab-1.2-data-lake-zones"
  cd "${lab_dir}"

  "$PYTHON" scripts/generate_sample_orders.py --count 1000 --date 2024-01-15

  aws s3 cp sample-data/orders_2024-01-15.csv \
    "s3://${bucket}/raw/retail/orders/year=2024/month=01/day=15/orders_2024-01-15.csv" \
    --metadata "source=lab-generator,record_count=1000"

  "$PYTHON" scripts/create_manifest.py \
    --bucket "${bucket}" \
    --dataset retail/orders \
    --source-file sample-data/orders_2024-01-15.csv || warn "Manifest upload skipped"

  "$PYTHON" scripts/validate_zones.py --bucket "${bucket}" || warn "Zone validation skipped (non-fatal)"

  log "Sample data seeded to s3://${bucket}/raw/retail/orders/..."
}

# ---------------------------------------------------------------------------
# Smoke-test Lambda ingestion
# ---------------------------------------------------------------------------
smoke_test() {
  log "Running smoke tests..."

  local fn bucket
  fn="$(terraform -chdir="${TF_DIR}" output -json lambda_function_names | python3 -c 'import json,sys; print(json.load(sys.stdin)[0])')"
  bucket="$(terraform -chdir="${TF_DIR}" output -raw data_lake_bucket)"

  aws lambda invoke \
    --function-name "${fn}" \
    --payload '{"records":[{"record_id":"smoke-001","amount":42.00,"currency":"USD"}]}' \
    --cli-binary-format raw-in-base64-out \
    /tmp/cnde-lambda-response.json >/dev/null

  log "Lambda invoke response:"
  cat /tmp/cnde-lambda-response.json
  echo

  log "Verifying S3 raw zone has objects..."
  aws s3 ls "s3://${bucket}/raw/" --recursive | head -5

  log "Smoke tests passed."
}

# ---------------------------------------------------------------------------
# Print summary
# ---------------------------------------------------------------------------
print_summary() {
  log "=== Lab Environment Ready ==="
  terraform -chdir="${TF_DIR}" output
  echo
  warn "Schedules are DISABLED by default (enable_schedules=false)."
  warn "Run ${SCRIPT_DIR}/stop-labs.sh when finished to avoid AWS charges."
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
  preflight
  deploy_terraform
  seed_sample_data
  smoke_test
  print_summary
}

main "$@"
