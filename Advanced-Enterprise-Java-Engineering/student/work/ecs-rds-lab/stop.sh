#!/usr/bin/env bash
# Tear down the optional ECS + RDS demo. This is the only honest $0 path.
# desired_count=0, RDS stop, and Expiration tags still leave ALB / storage / IPv4 bills.
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${LAB_DIR}"

if [[ ! -d .terraform ]]; then
  echo "No .terraform directory. Nothing to destroy, or run terraform init first." >&2
  exit 1
fi

echo "This destroys the whole stack in us-west-2: ALB, ECS, ECR images, RDS, secrets, IAM, VPC."
if [[ "${1:-}" != "-y" && "${1:-}" != "--yes" ]]; then
  read -r -p "Type DESTROY to continue: " confirm
  if [[ "${confirm}" != "DESTROY" ]]; then
    echo "Aborted. Stack is still billing."
    exit 1
  fi
fi

if [[ ! -f generated.auto.tfvars ]]; then
  echo "generated.auto.tfvars missing; destroy will use variable defaults (state still wins)."
fi

terraform destroy -input=false -auto-approve

rm -f generated.auto.tfvars

echo
echo "Destroy finished. Confirm in the console (us-west-2) that these are gone:"
echo "  - ALB / target group named baypay-ecsrd-*"
echo "  - RDS instance baypay-ecsrd-pg"
echo "  - ECR repository baypay/payment-service-ecs-demo"
echo "  - Secrets Manager secret baypay-ecsrd/db"
echo "If any remain, they are still billing."
