#!/usr/bin/env bash
# Start lab AWS resources before a session.
# Usage: ./start-lab.sh [--ec2-only|--rds-only|--all]

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

MODE="${1:---all}"

for lib in ec2 rds ecs asg nat; do
  source "${SCRIPT_DIR}/lib/${lib}.sh"
done

require_aws_cli
log INFO "Starting lab resources in ${AWS_REGION} (${LAB_TAG_KEY}=${LAB_TAG_VALUE})"

case "$MODE" in
  --ec2-only)
    ec2_start_lab_instances
    nat_instance_start
    ;;
  --rds-only)
    rds_start_lab_instances
    ;;
  --ecs-only)
    ecs_start_lab_services
    ;;
  --asg-only)
    asg_start_lab
    ;;
  --all|"")
    rds_start_lab_instances
    ec2_start_lab_instances
    nat_instance_start
    asg_start_lab
    ecs_start_lab_services
    ;;
  -h|--help)
    cat <<EOF
Usage: $(basename "$0") [OPTION]

Options:
  --all        Start RDS, EC2, NAT, ASG, ECS (default)
  --ec2-only   Start EC2 and NAT instances
  --rds-only   Start RDS instances
  --ecs-only   Scale ECS services to ECS_LAB_DESIRED_COUNT (default 1)
  --asg-only   Scale ASGs to ASG_LAB_DESIRED_COUNT (default 1)

Wait 2-5 minutes after start before running Terraform or health checks.
EOF
    exit 0
    ;;
  *)
    echo "Unknown option: $MODE" >&2
    exit 1
    ;;
esac

log INFO "Start requested. RDS can take several minutes. Run ./status-lab.sh to verify."
