#!/usr/bin/env bash
# Run all local unit tests (no AWS required).
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"
cd "$LABS_ROOT"

echo "=== Unit tests (pytest) ==="

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/pip install -q -r requirements.txt
.venv/bin/python -m pytest tests/ -v --tb=short "$@"

echo "=== All unit tests passed ==="
