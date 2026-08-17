#!/usr/bin/env bash
# Resume course labs after pause — recreate NAT Gateways and start compute.
#
# Usage: ./resume-labs.sh [--skip-terraform]
#   --skip-terraform  Only start EC2 (assumes NAT GW already exists)

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

SKIP_TERRAFORM=0
for arg in "$@"; do
  case "$arg" in
    --skip-terraform) SKIP_TERRAFORM=1 ;;
    -h|--help)
      cat <<EOF
Usage: $(basename "$0") [--skip-terraform]

Resumes BayAreaLa8s Terraform course labs after pause-labs.sh.

Steps:
  1. Terraform apply prod if NAT Gateway missing (takes ~2 min)
  2. Start EC2, RDS, ECS, ASG

Options:
  --skip-terraform  Skip Terraform apply (only start stopped instances)

Wait 2-5 minutes after resume before health checks or Terraform apply in labs.
EOF
      exit 0
      ;;
  esac
done

for lib in ec2 rds ecs asg nat terraform-lab; do
  # shellcheck source=/dev/null
  source "${SCRIPT_DIR}/lib/${lib}.sh"
done

require_aws_cli
log INFO "=== Resuming labs (${LAB_TAG_KEY}=${LAB_TAG_VALUE}) in ${AWS_REGION} ==="

if [[ "$SKIP_TERRAFORM" == "0" ]]; then
  terraform_lab_apply_if_nat_missing prod || log WARN "Prod apply for NAT GW failed"
else
  log INFO "Skipping Terraform apply (--skip-terraform)"
fi

"${SCRIPT_DIR}/start-lab.sh" --all

echo ""
log INFO "=== Resume complete ==="
"${SCRIPT_DIR}/status-lab.sh"
echo ""
echo "Pause when done: ./pause-labs.sh  (or: make lab-pause)"
