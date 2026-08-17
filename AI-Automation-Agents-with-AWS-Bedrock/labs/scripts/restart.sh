#!/usr/bin/env bash
# Full restart: delete stack, then redeploy fresh.
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"

echo "=== RESTART: Stop then start ==="
"$SCRIPTS_DIR/stop.sh"
echo ""
"$SCRIPTS_DIR/start.sh"
