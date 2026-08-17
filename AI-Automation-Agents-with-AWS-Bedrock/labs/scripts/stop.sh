#!/usr/bin/env bash
# Stop labs: delete entire stack to avoid ongoing AWS charges.
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"
cd "$LABS_ROOT"

usage() {
  cat <<EOF
Usage: $(basename "$0")

Delete the entire CloudFormation stack. This is the only way to stop
ongoing charges for Lambda, API Gateway, DynamoDB, and Step Functions.

Environment:
  AWS_REGION, PROJECT_PREFIX (must match the stack you started)
EOF
}

[[ "${1:-}" == "-h" || "${1:-}" == "--help" ]] && { usage; exit 0; }

require_aws_cli

echo "=============================================="
echo "  STOP — Delete course labs stack"
echo "=============================================="
echo "Stack: $STACK_NAME ($AWS_REGION)"
echo ""
echo "Deleting: Lambda, API Gateway, Step Functions, DynamoDB, CloudWatch..."
echo ""

if ! stack_exists 2>/dev/null; then
  echo "Stack not found — already stopped. No ongoing stack charges."
  rm -f "$STACK_ENV_FILE"
  exit 0
fi

STATUS="$(stack_exists)"
echo "Current status: $STATUS"

if [[ "$STATUS" == "DELETE_IN_PROGRESS" ]]; then
  echo "Delete already in progress — waiting..."
else
  if command -v sam &>/dev/null; then
    echo "Running sam delete..."
    sam delete \
      --stack-name "$STACK_NAME" \
      --region "$AWS_REGION" \
      --no-prompts \
      --resolve-s3 2>/dev/null || true
  fi

  echo "Running cloudformation delete-stack..."
  aws cloudformation delete-stack \
    --stack-name "$STACK_NAME" \
    --region "$AWS_REGION" 2>/dev/null || true
fi

echo "Waiting for stack deletion (typically 2–5 minutes)..."
if aws cloudformation wait stack-delete-complete \
  --stack-name "$STACK_NAME" \
  --region "$AWS_REGION" 2>/dev/null; then
  echo "Stack deleted successfully."
else
  echo "WARN: Timed out or stack already gone. Check AWS Console → CloudFormation."
fi

# Verify gone
if stack_exists 2>/dev/null; then
  echo "WARN: Stack may still exist with status: $(stack_exists)"
  echo "      Check CloudFormation console and retry ./scripts/stop.sh"
  exit 1
fi

rm -f "$STACK_ENV_FILE" "${LABS_ROOT}/.aws-sam/build.toml" 2>/dev/null || true

echo ""
echo "=============================================="
echo "  STOP complete — stack charges STOPPED"
echo "=============================================="
echo "Bedrock invokes during past labs may appear on your bill."
echo "SAM S3 artifacts may retain minimal storage (usually < \$0.01)."
