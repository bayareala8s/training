#!/usr/bin/env bash
# Pause all course labs — stop billable compute and destroy NAT Gateways.
#
# After pause, typical hourly cost is near zero:
#   - EC2 stopped (no compute charge)
#   - NAT Gateways destroyed (prod)
#   - VPC/subnets/IGW remain (no hourly charge)
#   - S3 state + DynamoDB locks (pennies)
#
# Usage: ./pause-labs.sh [--skip-terraform]
#   --skip-terraform  Only stop EC2/RDS/ECS/ASG (NAT GW still bills if prod deployed)

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

Pauses all BayAreaLa8s Terraform course labs to minimize AWS cost.

Steps:
  1. Stop EC2, RDS, scale ECS/ASG to zero
  2. Destroy NAT Gateways via Terraform (prod) — they cannot be stopped

Resume with: ./resume-labs.sh

Options:
  --skip-terraform  Stop compute only; NAT Gateways keep billing

Environment:
  DRY_RUN=1         Preview actions
  AWS_REGION        Default: us-west-2
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
log INFO "=== Pausing labs (${LAB_TAG_KEY}=${LAB_TAG_VALUE}) in ${AWS_REGION} ==="

"${SCRIPT_DIR}/stop-lab.sh" --all

if [[ "$SKIP_TERRAFORM" == "0" ]]; then
  for env in prod; do
    if terraform_lab_nat_gateway_exists "$env"; then
      terraform_lab_destroy_nat_gateway "$env" || log WARN "NAT destroy failed for $env"
    fi
  done
else
  log INFO "Skipping Terraform NAT Gateway destroy (--skip-terraform)"
fi

echo ""
log INFO "=== Pause complete ==="
"${SCRIPT_DIR}/status-lab.sh"
echo ""
echo "Resume before next session: ./resume-labs.sh  (or: make lab-resume)"
