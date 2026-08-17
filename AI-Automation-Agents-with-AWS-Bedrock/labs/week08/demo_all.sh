#!/usr/bin/env bash
# Run all four Capstone demos in order (A → B → C → D)
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source .stack.env 2>/dev/null || { echo "Run ./scripts/start.sh && source .stack.env first"; exit 1; }

bash "$DIR/option_a_incident_triage/demo.sh"
echo
bash "$DIR/option_b_doc_classification/demo.sh"
echo
bash "$DIR/option_c_approval_workflow/demo.sh"
echo
bash "$DIR/option_d_enterprise_agent/demo.sh"
echo
echo "=== All Capstone demos complete ==="
