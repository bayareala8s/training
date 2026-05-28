#!/usr/bin/env bash
# Full lab cycle: unit tests → deploy → integration verify → teardown (no leftover cost).
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"

TEARDOWN_ON_EXIT=true
SKIP_INTEGRATION=false

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

  Run all lab tests against AWS, then delete the stack to avoid ongoing charges.

Options:
  --keep-stack     Do not tear down after success (you pay for resources)
  --skip-aws       Run unit tests only (no deploy/verify/delete)
  -h, --help       Show this help

Environment:
  AWS_REGION, PROJECT_PREFIX, BEDROCK_MODEL_ID

Examples:
  ./scripts/cycle.sh
  PROJECT_PREFIX=ba-la8s-ai-jane ./scripts/cycle.sh
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --keep-stack) TEARDOWN_ON_EXIT=false; shift ;;
    --skip-aws) SKIP_INTEGRATION=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
done

cleanup() {
  if [[ "$TEARDOWN_ON_EXIT" == "true" && "$SKIP_INTEGRATION" != "true" ]]; then
    echo ""
    echo "=== CYCLE cleanup: tearing down AWS resources ==="
    "$SCRIPTS_DIR/stop.sh" || true
  fi
}
trap cleanup EXIT

echo "=============================================="
echo "  Course Labs — Start / Test / Stop Cycle"
echo "=============================================="
echo ""

# 1) Unit tests (always)
"$SCRIPTS_DIR/run-tests.sh"

if [[ "$SKIP_INTEGRATION" == "true" ]]; then
  echo "Skipping AWS integration (--skip-aws)."
  TEARDOWN_ON_EXIT=false
  exit 0
fi

# 2) Deploy
"$SCRIPTS_DIR/start.sh"

# 3) Integration tests against live AWS
echo ""
echo "=== Integration tests (live AWS) ==="
PYTHON="${LABS_ROOT}/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
  PYTHON=python3
fi
"$PYTHON" "$SCRIPTS_DIR/verify_labs.py"

echo ""
echo "=============================================="
echo "  Cycle complete — stack will be torn down"
echo "=============================================="
