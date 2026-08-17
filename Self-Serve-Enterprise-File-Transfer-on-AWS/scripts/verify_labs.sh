#!/usr/bin/env bash
# Smoke-test provisioned lab resources (weeks 1–7 infrastructure).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

baylearn_require_tools
export AWS_REGION="$(baylearn_aws_region)"

BUCKET="$(baylearn_tf_raw landing_bucket)"
PREFIX="$(baylearn_tf_raw inbound_s3_prefix)"
SFN="$(baylearn_tf_raw state_machine_arn)"
API="$(baylearn_tf_raw api_endpoint)"
POOL="$(baylearn_tf_raw cognito_user_pool_id)"
CLIENT="$(baylearn_tf_raw cognito_client_id)"
USER="$(baylearn_tf_raw cognito_test_username)"
ENDPOINT="$(baylearn_tf_raw transfer_server_endpoint)"

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1" >&2; exit 1; }

[[ -n "$BUCKET" ]] && pass "landing bucket $BUCKET" || fail "landing bucket output missing"
aws s3api head-bucket --bucket "$BUCKET" >/dev/null 2>&1 && pass "S3 head-bucket" || fail "S3 head-bucket"

echo "sample,data" > /tmp/baylearn-sample.csv
KEY="${PREFIX}baylearn-verify-$(date +%s).csv"
aws s3 cp /tmp/baylearn-sample.csv "s3://${BUCKET}/${KEY}" && pass "uploaded s3://${BUCKET}/${KEY}"

sleep 8
aws s3 ls "s3://${BUCKET}/partners/demo/processing/" 2>/dev/null | grep -q . && pass "S3 processor routed to processing/" || \
  echo "WARN: processing/ prefix empty (wait longer or check Lambda logs)"

[[ -n "$SFN" ]] && pass "state machine $SFN" || fail "state machine missing"
EXEC=$(aws stepfunctions start-execution \
  --state-machine-arn "$SFN" \
  --name "verify-$(date +%s)" \
  --input "{\"bucket\":\"$BUCKET\",\"key\":\"$KEY\",\"correlation_id\":\"verify-1\"}" \
  --query executionArn --output text)
pass "started execution $EXEC"
sleep 10

[[ -n "$API" && -n "$POOL" && -n "$CLIENT" ]] && pass "API $API" || fail "API/Cognito outputs missing"

if [[ -n "$ENDPOINT" ]]; then
  pass "SFTP endpoint ${ENDPOINT} (use ./scripts/get_sftp_private_key.sh)"
else
  echo "WARN: Transfer Family disabled (enable_transfer_family=false)"
fi

DASH="$(baylearn_tf_raw cloudwatch_dashboard_name)"
[[ -n "$DASH" ]] && pass "dashboard $DASH" || fail "dashboard missing"

ECS_CLUSTER="$(baylearn_tf_raw ecs_cluster_name)"
if [[ -n "$ECS_CLUSTER" && "$ECS_CLUSTER" != "null" ]]; then
  pass "ECS cluster $ECS_CLUSTER (Lab 9)"
  ECR="$(baylearn_tf_raw ecr_repository_url)"
  [[ -n "$ECR" ]] && pass "ECR $ECR" || fail "ECR missing"
  aws ecs describe-task-definition --task-definition "$(baylearn_tf_raw ecs_task_definition)" >/dev/null 2>&1 && pass "ECS task definition" || fail "ECS task definition"
else
  echo "WARN: ECS worker disabled (enable_ecs_worker=false)"
fi

echo ""
echo "All automated checks completed."
echo "Manual: confirm SNS email subscriptions; SFTP upload; POST /v1/connections via ./scripts/cognito_login.sh"
