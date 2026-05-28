#!/usr/bin/env bash
# Stop labs: delete entire stack to avoid ongoing AWS charges.
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"
cd "$LABS_ROOT"

require_aws_cli

echo "=== STOP: Tearing down course labs stack ==="
echo "Stack: $STACK_NAME ($AWS_REGION)"

if ! stack_exists 2>/dev/null; then
  echo "Stack not found — nothing to delete."
  rm -f "$STACK_ENV_FILE"
  exit 0
fi

STATUS="$(stack_exists)"
echo "Current status: $STATUS"

if [[ "$STATUS" == "DELETE_IN_PROGRESS" ]]; then
  echo "Delete already in progress — waiting..."
else
  if command -v sam &>/dev/null; then
    sam delete \
      --stack-name "$STACK_NAME" \
      --region "$AWS_REGION" \
      --no-prompts \
      --resolve-s3 2>/dev/null || true
  fi

  # Ensure delete is triggered even if sam delete fails
  aws cloudformation delete-stack \
    --stack-name "$STACK_NAME" \
    --region "$AWS_REGION" 2>/dev/null || true
fi

echo "Waiting for stack deletion (this may take several minutes)..."
if aws cloudformation wait stack-delete-complete \
  --stack-name "$STACK_NAME" \
  --region "$AWS_REGION" 2>/dev/null; then
  echo "Stack deleted successfully."
else
  echo "WARN: Timed out or stack already gone. Check AWS Console → CloudFormation."
fi

rm -f "$STACK_ENV_FILE" "${LABS_ROOT}/.aws-sam/build.toml" 2>/dev/null || true
echo "=== STOP complete — no stack resources should remain ==="
