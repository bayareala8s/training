#!/usr/bin/env bash
# Maximum cost reduction: stop tagged resources + destroy dev Terraform stack.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DEV_DIR="${REPO_ROOT}/labs/shared/environments/dev"

echo "Stopping all lab-tagged resources..."
"${SCRIPT_DIR}/stop-lab.sh" --all

if [[ -f "${DEV_DIR}/terraform.tfvars" && -f "${DEV_DIR}/backend.hcl" ]]; then
  echo "Destroying dev Terraform stack..."
  cd "${DEV_DIR}"
  terraform init -backend-config=backend.hcl -input=false
  terraform destroy -var-file=terraform.tfvars -auto-approve -input=false || true
fi

echo "Teardown complete. Verify:"
"${SCRIPT_DIR}/status-lab.sh"
echo ""
echo "Note: S3 state bucket and DynamoDB lock table are retained (minimal cost)."
