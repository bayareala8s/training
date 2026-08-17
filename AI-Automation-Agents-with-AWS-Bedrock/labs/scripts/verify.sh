#!/usr/bin/env bash
# Integration verification (requires deployed stack).
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"

if ! stack_is_active 2>/dev/null; then
  echo "ERROR: Stack '$STACK_NAME' is not deployed. Run: ./scripts/start.sh"
  exit 1
fi

[[ -f "$STACK_ENV_FILE" ]] || write_stack_env

PYTHON="${LABS_ROOT}/.venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON=python3

exec "$PYTHON" "$SCRIPTS_DIR/verify_labs.py"
