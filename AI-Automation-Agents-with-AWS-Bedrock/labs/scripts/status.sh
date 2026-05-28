#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"

if status="$(stack_exists 2>/dev/null)"; then
  echo "Stack: $STACK_NAME"
  echo "Status: $status"
  echo "Region: $AWS_REGION"
  if stack_is_active 2>/dev/null && [[ -f "$STACK_ENV_FILE" ]]; then
    echo "Env file: $STACK_ENV_FILE"
    grep -E '^export (API_ENDPOINT|STATE_MACHINE_ARN)=' "$STACK_ENV_FILE" || true
  fi
else
  echo "Stack '$STACK_NAME' not found in $AWS_REGION (stopped / never deployed)."
fi
