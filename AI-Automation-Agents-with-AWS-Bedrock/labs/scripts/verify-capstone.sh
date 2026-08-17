#!/usr/bin/env bash
# Verify Week 8 capstone endpoints against live AWS stack.
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
PYTHON="${LABS_ROOT}/.venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON=python3
"$PYTHON" "$SCRIPTS_DIR/verify_capstone.py"
