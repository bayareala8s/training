#!/usr/bin/env bash
# Unified start / stop / status / restart for course labs (zero ongoing cost when stopped).
#
# Usage:
#   ./scripts/lab-cycle.sh start              Deploy all labs + seed data
#   ./scripts/lab-cycle.sh stop [--yes]       Destroy everything + cleanup extras
#   ./scripts/lab-cycle.sh status             Show what is running
#   ./scripts/lab-cycle.sh restart [--yes]    stop then start
#   ./scripts/lab-cycle.sh verify             Health-check (requires running stack)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
  cat <<EOF
CNDE Lab Cycle — start and stop all AWS lab resources with zero ongoing cost when stopped.

Commands:
  start              Deploy Terraform stack, seed sample data, smoke-test
  stop [--yes]       Destroy Terraform stack + cleanup Lab 7 KMS/IAM/logs
  status             Show running resources and cost risk
  restart [--yes]    stop then start (fresh environment)
  verify             Verify deployed resources (stack must be running)

Examples:
  ./scripts/lab-cycle.sh start
  ./scripts/lab-cycle.sh stop --yes
  source ./scripts/lab-env.sh          # after start — load \$BUCKET, \$GLUE_JOB, etc.

When stopped:
  - No S3, Lambda, Glue, Step Functions, SNS, or dashboard charges
  - KMS keys (if created in Lab 7.1) scheduled for deletion (7-day AWS minimum)
  - CloudWatch log groups removed

Docs: docs/LAB-DEMO-GUIDE.md
EOF
}

cmd_start() {
  echo -e "${GREEN}=== START: Deploying lab environment ===${NC}"
  "${SCRIPT_DIR}/start-labs.sh"
  echo
  echo -e "${GREEN}=== Lab environment STARTED ===${NC}"
  echo "Next steps:"
  echo "  source ./scripts/lab-env.sh"
  echo "  ./scripts/lab-cycle.sh verify"
  echo "  docs/LAB-DEMO-GUIDE.md"
  echo
  echo -e "${YELLOW}When finished: ./scripts/lab-cycle.sh stop --yes${NC}"
}

cmd_stop() {
  echo -e "${YELLOW}=== STOP: Tearing down lab environment ===${NC}"
  # Cleanup extras that reference the bucket before destroy
  "${SCRIPT_DIR}/cleanup-lab-extras.sh" || true
  "${SCRIPT_DIR}/stop-labs.sh" "$@"
  # Cleanup extras left after destroy (log groups, KMS, IAM)
  "${SCRIPT_DIR}/cleanup-lab-extras.sh" || true
  echo
  echo -e "${GREEN}=== Lab environment STOPPED ===${NC}"
  "${SCRIPT_DIR}/status-labs.sh"
}

cmd_status() {
  "${SCRIPT_DIR}/status-labs.sh"
}

cmd_verify() {
  echo -e "${GREEN}=== VERIFY: Health check ===${NC}"
  "${SCRIPT_DIR}/verify-labs.sh"
}

cmd_restart() {
  echo -e "${YELLOW}=== RESTART: stop → start ===${NC}"
  cmd_stop "$@"
  echo
  cmd_start
}

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    start)   cmd_start ;;
    stop)    cmd_stop "$@" ;;
    status)  cmd_status ;;
    restart) cmd_restart "$@" ;;
    verify)  cmd_verify ;;
    -h|--help|help|"")
      usage
      [[ -z "$cmd" ]] && exit 0 || exit 0
      ;;
    *)
      echo -e "${RED}Unknown command: ${cmd}${NC}" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
