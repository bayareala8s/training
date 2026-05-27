#!/usr/bin/env bash
# Destroy the BayLearn MFT lab stack (terraform destroy) — stops ongoing AWS charges.
#
# Usage:
#   ./scripts/stop_stack.sh
#   ./scripts/stop_stack.sh --yes
#
# Prod guard: if environment=prod in tfvars, set BAYLEARN_CONFIRM_PROD_DESTROY=1

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

AUTO_APPROVE=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    -y | --yes) AUTO_APPROVE=true; shift ;;
    -h | --help)
      echo "Usage: $0 [--yes]" >&2
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

baylearn_require_tools

ENV_HINT="$(baylearn_stack_env_name)"
if [[ "$ENV_HINT" == "prod" && "${BAYLEARN_CONFIRM_PROD_DESTROY:-}" != "1" ]]; then
  echo "Refusing destroy: environment looks like prod. Set BAYLEARN_CONFIRM_PROD_DESTROY=1 to override." >&2
  exit 2
fi

if ! $AUTO_APPROVE; then
  echo "About to destroy ALL lab resources in: $BAYLEARN_TF_DIR"
  read -r -p "Type yes to destroy: " confirm
  if [[ "$confirm" != "yes" ]]; then
    echo "Aborted."
    exit 1
  fi
fi

terraform -chdir="$BAYLEARN_TF_DIR" init -input=false >/dev/null

echo "==> terraform destroy ($BAYLEARN_TF_DIR)"
terraform -chdir="$BAYLEARN_TF_DIR" destroy -auto-approve

echo "OK: lab stack destroyed."
