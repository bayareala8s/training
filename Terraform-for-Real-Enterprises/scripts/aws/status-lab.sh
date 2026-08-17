#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

for lib in ec2 rds ecs asg nat; do
  source "${SCRIPT_DIR}/lib/${lib}.sh"
done

require_aws_cli

echo "=============================================="
echo " Lab resource status"
echo " Region: ${AWS_REGION}"
echo " Tag:    ${LAB_TAG_KEY}=${LAB_TAG_VALUE}"
echo " Account: $(aws sts get-caller-identity --query Account --output text)"
echo "=============================================="
echo ""
echo "--- EC2 ---"
ec2_lab_status
echo ""
echo "--- NAT Gateway ---"
nat_gateway_status
echo ""
echo "--- RDS (tagged resources) ---"
rds_lab_status
echo ""
echo "--- Cost ---"
nat_gateway_hourly_cost_warning
running_ec2=$(aws ec2 describe-instances --region "$AWS_REGION" \
  --filters "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
            "Name=instance-state-name,Values=running,pending" \
  --query 'length(Reservations[].Instances[])' --output text 2>/dev/null || echo "0")
if [[ "$running_ec2" != "0" && "$running_ec2" != "None" ]]; then
  echo "WARNING: Running EC2 instances bill hourly. Run: ./pause-labs.sh or ./stop-lab.sh"
else
  echo "EC2: all stopped (no compute hourly charge)"
fi
echo ""
echo "Pause (zero cost):  ./pause-labs.sh"
echo "Resume:             ./resume-labs.sh"
echo "Full destroy:       make destroy ENV=dev (per environment)"
