#!/usr/bin/env bash
# Manually run the Fargate worker task (instructor demo without waiting for S3 trigger).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

baylearn_require_tools
export AWS_REGION="$(baylearn_aws_region)"

CLUSTER="$(baylearn_tf_raw ecs_cluster_name)"
TASK_DEF="$(baylearn_tf_raw ecs_task_definition)"
BUCKET="$(baylearn_tf_raw landing_bucket)"
DEST_PREFIX="$(baylearn_tf_raw large_file_processed_prefix)"
LOG_GROUP="$(baylearn_tf_raw ecs_worker_log_group)"
SOURCE_KEY="${1:-}"

if [[ -z "$SOURCE_KEY" ]]; then
  echo "Usage: $0 <s3-object-key>" >&2
  echo "Example: $0 partners/demo/large/inbound/myfile.bin" >&2
  exit 1
fi

SUBNETS=$(terraform -chdir="$BAYLEARN_TF_DIR" output -json ecs_subnet_ids | jq -r 'join(",")')
SG=$(terraform -chdir="$BAYLEARN_TF_DIR" output -raw ecs_security_group_id)

JOB=$(jq -n \
  --arg bucket "$BUCKET" \
  --arg key "$SOURCE_KEY" \
  --arg dest "$DEST_PREFIX" \
  --arg cid "manual-$(date +%s)" \
  '{bucket:$bucket,source_key:$key,dest_prefix:$dest,correlation_id:$cid}')

JOB_ESCAPED=$(echo "$JOB" | jq -c . | jq -R .)

TASK_ARN=$(aws ecs run-task \
  --cluster "$CLUSTER" \
  --task-definition "$TASK_DEF" \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[${SUBNETS}],securityGroups=[${SG}],assignPublicIp=ENABLED}" \
  --overrides "{\"containerOverrides\":[{\"name\":\"worker\",\"environment\":[{\"name\":\"TRANSFER_JOB\",\"value\":${JOB_ESCAPED}}]}]}" \
  --query 'tasks[0].taskArn' --output text)

echo "Started: $TASK_ARN"
echo "Logs: aws logs tail ${LOG_GROUP} --since 5m --follow"
