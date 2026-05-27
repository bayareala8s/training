#!/usr/bin/env bash
# Local CI gate: unit tests + Terraform validate (no AWS deploy required).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

ROOT="$BAYLEARN_ROOT"
cd "$ROOT"

echo "==> Python unit tests"
VENV="$ROOT/.venv"
if [[ ! -d "$VENV" ]]; then
  python3 -m venv "$VENV"
fi
# shellcheck source=/dev/null
source "$VENV/bin/activate"
pip install -q -r tests/requirements.txt
pytest tests/unit -v --tb=short

echo "==> Terraform fmt check"
terraform -chdir="$ROOT/infra" fmt -check -recursive || {
  echo "Run: terraform -chdir=$ROOT/infra fmt -recursive" >&2
  exit 1
}

echo "==> Terraform init + validate"
terraform -chdir="$BAYLEARN_TF_DIR" init -input=false >/dev/null
terraform -chdir="$BAYLEARN_TF_DIR" validate

echo "OK: ci_verify.sh passed"
