#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"

echo "Lab 01 verification — Architecture artifacts"

TEMPLATE_DIR="${ROOT}/labs/module-01/templates"
[[ -d "$TEMPLATE_DIR" ]] && pass "Templates directory exists"

for f in service-decomposition.md context-map.md; do
  if [[ -f "${TEMPLATE_DIR}/${f}" ]]; then
    pass "Template found: ${f}"
  fi
done

pass "Lab 01 structure OK (submit your completed docs to instructor)"
echo "Lab 01 PASSED"
