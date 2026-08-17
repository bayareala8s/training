#!/usr/bin/env bash
# Unified lab control — start, stop, status, and full test cycles.
#
# Cost model:
#   STOPPED  = stack deleted → no Lambda/API/DynamoDB/Step Functions charges
#   RUNNING  = stack deployed → pay only while up + per Bedrock invoke
#
# Recommended workflow:
#   ./scripts/labs.sh setup     # once (local)
#   ./scripts/labs.sh cycle     # first validation (auto-stops)
#   ./scripts/labs.sh start     # when recording demos / doing labs
#   ./scripts/labs.sh stop      # when done for the day
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"

usage() {
  cat <<EOF
Usage: $(basename "$0") <command> [options]

Commands:
  setup       One-time local setup (venv + pip) — FREE
  start       Deploy / update AWS stack — COST while running
  stop        Delete entire stack — STOP charges
  restart     stop + start (clean redeploy)
  status      Show stack state and endpoints
  test        Run local unit tests only — FREE
  verify      Run integration tests (stack must be up) — Bedrock invoke cost
  verify-capstone  Verify Week 8 capstone endpoints — Bedrock invoke cost
  cycle       test → start → verify → verify-capstone → stop — recommended
  help        Show this help

Environment (set before start):
  AWS_REGION         Default: us-east-1
  PROJECT_PREFIX     Default: ba-la8s-ai  (use your name: ba-la8s-ai-jane)
  BEDROCK_MODEL_ID   Default: amazon.nova-lite-v1:0

Examples:
  export PROJECT_PREFIX=ba-la8s-ai-demo
  ./scripts/labs.sh start
  source .stack.env && curl "\$API_ENDPOINT/classify" ...
  ./scripts/labs.sh stop

  # Safe first run (auto-teardown):
  ./scripts/labs.sh cycle

Options for cycle (pass after 'cycle'):
  --keep-stack     Leave stack running after cycle
  --skip-aws       Unit tests only
  --skip-capstone  Skip capstone verification

See labs/COST_CONTROL.md for billing details.
EOF
}

cmd="${1:-}"
shift || true

case "$cmd" in
  setup)     exec "$SCRIPTS_DIR/setup.sh" "$@" ;;
  start)     exec "$SCRIPTS_DIR/start.sh" "$@" ;;
  stop|down) exec "$SCRIPTS_DIR/stop.sh" "$@" ;;
  restart)   exec "$SCRIPTS_DIR/restart.sh" "$@" ;;
  status)    exec "$SCRIPTS_DIR/status.sh" "$@" ;;
  test)      exec "$SCRIPTS_DIR/run-tests.sh" "$@" ;;
  verify)    exec "$SCRIPTS_DIR/verify.sh" "$@" ;;
  verify-capstone) exec "$SCRIPTS_DIR/verify-capstone.sh" "$@" ;;
  cycle)     exec "$SCRIPTS_DIR/cycle.sh" "$@" ;;
  help|-h|--help|"")
    usage
    ;;
  *)
    echo "Unknown command: $cmd"
    usage
    exit 1
    ;;
esac
