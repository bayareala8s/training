#!/usr/bin/env bash
# Start labs: deploy CloudFormation stack (incurs cost only while stack exists + on invoke).
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"
cd "$LABS_ROOT"

usage() {
  cat <<EOF
Usage: $(basename "$0")

Deploy or update the full course stack (Weeks 2–8 + capstone).

Environment:
  AWS_REGION, PROJECT_PREFIX, BEDROCK_MODEL_ID

Stop charges: ./scripts/stop.sh  or  ./scripts/labs.sh stop
EOF
}

[[ "${1:-}" == "-h" || "${1:-}" == "--help" ]] && { usage; exit 0; }

require_aws_cli
require_sam_cli

echo "=============================================="
echo "  START — Deploy course labs to AWS"
echo "=============================================="
echo "Stack:  $STACK_NAME"
echo "Region: $AWS_REGION"
echo "Model:  $BEDROCK_MODEL_ID"
echo ""
echo "⚠️  COST: You pay while this stack exists + per Bedrock invoke."
echo "    Run ./scripts/stop.sh when finished."
echo ""

if stack_is_active 2>/dev/null; then
  echo "Stack active — building and deploying updates..."
else
  echo "Creating new stack..."
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
echo "=============================================="
echo "  START complete — stack is RUNNING"
echo "=============================================="
echo "API:              $API_ENDPOINT"
echo "State machine:    $STATE_MACHINE_ARN"
echo "Capstone SM:      $CAPSTONE_INCIDENT_SM_ARN"
echo "Env file:         $STACK_ENV_FILE"
echo ""
echo "Load env:         source .stack.env"
echo "Verify labs:      ./scripts/verify.sh"
echo "Verify capstone:  ./scripts/verify-capstone.sh"
echo "STOP (no cost):   ./scripts/stop.sh"
