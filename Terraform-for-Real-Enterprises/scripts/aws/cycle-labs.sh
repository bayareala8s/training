#!/usr/bin/env bash
# Test full pause → resume cycle (instructor smoke test for cost scripts).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Cycle test: pause → status → resume → status ==="
"${SCRIPT_DIR}/pause-labs.sh"
echo ""
echo "--- Waiting 10s ---"
sleep 10
echo ""
"${SCRIPT_DIR}/resume-labs.sh"
echo ""
log() { echo "[cycle] $*"; }
log "Cycle complete. Verify EC2 running and NAT GW available (prod)."
