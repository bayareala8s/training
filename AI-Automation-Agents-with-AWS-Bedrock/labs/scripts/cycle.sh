#!/usr/bin/env bash
# Full lab cycle: unit tests → deploy → integration verify → capstone verify → teardown.
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"

TEARDOWN_ON_EXIT=true
SKIP_INTEGRATION=false
SKIP_CAPSTONE=false

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

  Run all lab tests against AWS, then delete the stack to avoid ongoing charges.

Options:
  --keep-stack       Do not tear down after success (you pay for resources)
  --skip-aws         Run unit tests only (no deploy/verify/delete)
  --skip-capstone    Skip Week 8 capstone verification
  -h, --help         Show this help

Environment:
  AWS_REGION, PROJECT_PREFIX, BEDROCK_MODEL_ID

Examples:
  ./scripts/cycle.sh
  PROJECT_PREFIX=ba-la8s-ai-jane ./scripts/cycle.sh
  ./scripts/cycle.sh --keep-stack   # leave running for demos
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --keep-stack) TEARDOWN_ON_EXIT=false; shift ;;
    --skip-aws) SKIP_INTEGRATION=true; shift ;;
    --skip-capstone) SKIP_CAPSTONE=true; shift ;;
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

PYTHON="${LABS_ROOT}/.venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON=python3

echo "=============================================="
echo "  Course Labs — Full Start / Test / Stop Cycle"
echo "=============================================="
echo "Stack:  $STACK_NAME"
echo "Region: $AWS_REGION"
echo "Teardown after run: $TEARDOWN_ON_EXIT"
echo ""

# 1) Unit tests (always — free)
echo "=== Step 1/5: Unit tests (local, free) ==="
"$SCRIPTS_DIR/run-tests.sh"

if [[ "$SKIP_INTEGRATION" == "true" ]]; then
  echo "Skipping AWS steps (--skip-aws)."
  TEARDOWN_ON_EXIT=false
  exit 0
fi

# 2) Deploy
echo ""
echo "=== Step 2/5: Deploy stack (start) ==="
"$SCRIPTS_DIR/start.sh"

# 3) Integration tests — Weeks 2–7
echo ""
echo "=== Step 3/5: Integration tests (Weeks 2–7) ==="
"$PYTHON" "$SCRIPTS_DIR/verify_labs.py"

# 4) Capstone tests — Week 8
if [[ "$SKIP_CAPSTONE" != "true" ]]; then
  echo ""
  echo "=== Step 4/5: Capstone tests (Week 8) ==="
  "$PYTHON" "$SCRIPTS_DIR/verify_capstone.py"
else
  echo ""
  echo "=== Step 4/5: Capstone tests skipped (--skip-capstone) ==="
fi

echo ""
echo "=== Step 5/5: Teardown ==="
if [[ "$TEARDOWN_ON_EXIT" == "true" ]]; then
  echo "All checks passed — stack will be deleted (no ongoing cost)."
else
  echo "All checks passed — stack kept running (--keep-stack)."
  TEARDOWN_ON_EXIT=false  # prevent trap from double-running stop
fi

echo ""
echo "=============================================="
echo "  Cycle complete"
echo "=============================================="
