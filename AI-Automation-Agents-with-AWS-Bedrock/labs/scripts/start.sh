#!/usr/bin/env bash
# Start labs: deploy CloudFormation stack (incurs cost only while stack exists + on invoke).
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"
cd "$LABS_ROOT"

require_aws_cli
require_sam_cli

echo "=== START: Deploying course labs stack ==="
echo "Stack:  $STACK_NAME"
echo "Region: $AWS_REGION"
echo "Model:  $BEDROCK_MODEL_ID"

if stack_is_active 2>/dev/null; then
  echo "Stack already active — refreshing outputs."
  write_stack_env
  echo "Stack env: $STACK_ENV_FILE"
  exit 0
fi

sam build --cached
sam deploy \
  --stack-name "$STACK_NAME" \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --region "$AWS_REGION" \
  --parameter-overrides \
    "ProjectPrefix=${PROJECT_PREFIX}" \
    "BedrockModelId=${BEDROCK_MODEL_ID}" \
  --no-fail-on-empty-changeset

echo "Waiting for stack to stabilize..."
if ! aws cloudformation wait stack-create-complete \
  --stack-name "$STACK_NAME" \
  --region "$AWS_REGION" 2>/dev/null; then
  aws cloudformation wait stack-update-complete \
    --stack-name "$STACK_NAME" \
    --region "$AWS_REGION"
fi

write_stack_env
echo ""
echo "=== START complete ==="
echo "API: $API_ENDPOINT"
echo "Run: ./scripts/verify.sh  or  ./scripts/cycle.sh"
