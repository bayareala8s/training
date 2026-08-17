#!/usr/bin/env bash
# Stop lab AWS resources to reduce cost (end of day / weekend).
# Usage: ./stop-lab.sh [--ec2-only|--rds-only|--all]
# Requires: AWS CLI, credentials, resources tagged Course=terraform-enterprise

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=config.sh
source "${SCRIPT_DIR}/config.sh"

MODE="${1:---all}"

for lib in ec2 rds ecs asg nat; do
  # shellcheck source=/dev/null
  source "${SCRIPT_DIR}/lib/${lib}.sh"
done

require_aws_cli
log INFO "Stopping lab resources in ${AWS_REGION} (${LAB_TAG_KEY}=${LAB_TAG_VALUE})"

case "$MODE" in
  --ec2-only)
    ec2_stop_lab_instances
    nat_instance_stop
    ;;
  --rds-only)
    rds_stop_lab_instances
    ;;
  --ecs-only)
    ecs_stop_lab_services
    ;;
  --asg-only)
    asg_stop_lab
    ;;
  --all|"")
    ecs_stop_lab_services
    asg_stop_lab
    ec2_stop_lab_instances
    nat_instance_stop
    rds_stop_lab_instances
    ;;
  -h|--help)
    cat <<EOF
Usage: $(basename "$0") [OPTION]

Options:
  --all        Stop EC2, NAT instances, RDS, ECS (scale 0), ASG (default)
  --ec2-only   Stop EC2 and NAT instances only
  --rds-only   Stop RDS instances only
  --ecs-only   Scale ECS services to 0
  --asg-only   Scale ASGs to 0

Environment:
  AWS_REGION              AWS region (default: us-west-2)
  LAB_TAG_KEY             Tag key (default: Course)
  LAB_TAG_VALUE           Tag value (default: terraform-enterprise)
  DRY_RUN=1               Print actions without executing

Note: Managed NAT Gateways cannot be stopped; destroy via Terraform or use NAT instances.
EOF
    exit 0
    ;;
  *)
    echo "Unknown option: $MODE" >&2
    exit 1
    ;;
esac

log INFO "Stop complete. Run ./status-lab.sh to verify."
