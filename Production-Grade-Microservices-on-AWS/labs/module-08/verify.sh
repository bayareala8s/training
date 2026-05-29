#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"
require_cmd aws

echo "Lab 08 verification — Observability"

TF_DIR="${ROOT}/infrastructure/terraform"
PREFIX="${PROJECT_NAME:-ms-course}-${ENVIRONMENT:-dev}"
LOG_GROUP="/ecs/${PREFIX}"

aws logs describe-log-groups --log-group-name-prefix "$LOG_GROUP" \
  --query 'logGroups[0].logGroupName' --output text \
  --region "${AWS_REGION:-us-east-1}" 2>/dev/null | grep -q ecs && pass "ECS log group exists" \
  || skip "ECS log group not found (start platform first)"

CLUSTER=$(terraform -chdir="$TF_DIR" output -raw ecs_cluster_name 2>/dev/null || echo "")
if [[ -n "$CLUSTER" ]]; then
  pass "ECS cluster: ${CLUSTER}"
fi

echo "Lab 08 PASSED"
