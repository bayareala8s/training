#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

for lib in ec2 rds ecs asg; do
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
echo "--- RDS (tagged resources) ---"
rds_lab_status
echo ""
echo "--- Cost reminder ---"
echo "NAT Gateways and EIPs bill while provisioned. Use ./stop-lab.sh when not in lab."
echo "Destroy sandboxes with: make destroy ENV=dev (from labs/)"
