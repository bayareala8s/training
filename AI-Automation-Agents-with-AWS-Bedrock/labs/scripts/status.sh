#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"

echo "=============================================="
echo "  Lab stack status"
echo "=============================================="
echo "Project prefix: $PROJECT_PREFIX"
echo "Stack name:     $STACK_NAME"
echo "Region:         $AWS_REGION"
echo ""

if status="$(stack_exists 2>/dev/null)"; then
  echo "State: RUNNING ($status)"
  echo ""
  echo "⚠️  Stack is UP — you incur AWS charges while deployed."
  echo "    Stop charges: ./scripts/stop.sh"
  echo ""

  if stack_is_active 2>/dev/null; then
    write_stack_env 2>/dev/null || true
    if [[ -f "$STACK_ENV_FILE" ]]; then
      echo "Endpoints (from $STACK_ENV_FILE):"
      grep -E '^export (API_ENDPOINT|STATE_MACHINE_ARN|CAPSTONE_INCIDENT_SM_ARN|CAPSTONE_FUNCTION)=' "$STACK_ENV_FILE" | sed 's/^export /  /' || true
    fi
    echo ""
    echo "Resources in stack:"
    aws cloudformation list-stack-resources \
      --stack-name "$STACK_NAME" \
      --region "$AWS_REGION" \
      --query "StackResourceSummaries[?ResourceStatus!='DELETE_COMPLETE'].{Type:ResourceType,Id:LogicalResourceId}" \
      --output table 2>/dev/null || echo "  (unable to list resources)"
  fi
else
  echo "State: STOPPED (stack not found)"
  echo ""
  echo "✓ No ongoing stack charges."
  echo "  Start labs: ./scripts/start.sh"
fi
