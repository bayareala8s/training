#!/usr/bin/env bash
# Full lab cycle: ci_verify → start → test_all_labs → optional stop.
#
# Usage:
#   ./scripts/lab_cycle.sh --yes              # start + verify, leave stack running
#   ./scripts/lab_cycle.sh --yes --destroy    # start + verify + destroy

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YES=false
DESTROY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -y | --yes) YES=true; shift ;;
    --destroy) DESTROY=true; shift ;;
    -h | --help)
      echo "Usage: $0 [--yes] [--destroy]" >&2
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

ARGS=()
$YES && ARGS+=(--yes)

echo "==> Phase 1: local CI (unit tests + terraform validate)"
"$SCRIPT_DIR/ci_verify.sh"

echo "==> Phase 2: provision AWS lab stack"
"$SCRIPT_DIR/start_stack.sh" "${ARGS[@]}"

echo "==> Phase 3: integration tests (all labs)"
"$SCRIPT_DIR/test_all_labs.sh"

if $DESTROY; then
  echo "==> lab_cycle: destroying stack"
  "$SCRIPT_DIR/stop_stack.sh" "${ARGS[@]}"
else
  echo "==> lab_cycle: stack left running. Run ./scripts/stop_stack.sh --yes when finished."
fi
