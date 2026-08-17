#!/usr/bin/env bash
# One-time local setup (no AWS cost).
set -euo pipefail

source "$(dirname "$0")/lib/common.sh"
cd "$LABS_ROOT"

echo "=== SETUP: Local lab environment ==="

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  echo "Created .venv"
fi

# shellcheck source=/dev/null
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "=== SETUP complete ==="
echo "Activate:  source .venv/bin/activate"
echo "Configure: export AWS_REGION=us-east-1"
echo "           export PROJECT_PREFIX=ba-la8s-ai-yourname"
echo "           export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0"
echo ""
echo "Next:      ./scripts/labs.sh start    # deploy to AWS (incurs cost while running)"
echo "           ./scripts/labs.sh cycle    # test + deploy + verify + auto-stop (recommended first run)"
