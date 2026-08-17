#!/usr/bin/env bash
# Run full automated validation for modules 1–9 (AWS-testable labs).
#
# Automated: Labs 2.1–2.3, 3.1–3.2, 4.1–4.3, 5.1–5.2, 6.1, 7.1–7.3, 9.1–9.3
# Manual/demo-only: Labs 3.3, 5.3, 6.2, 6.3 (see docs/LAB-DEMO-GUIDE.md)
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== CNDE Full Lab Validation (Modules 1–9) ==="
echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

FAIL=0
"${SCRIPT_DIR}/test-modules-1-6.sh" || FAIL=$((FAIL + 1))
echo
"${SCRIPT_DIR}/test-modules-7-9.sh" || FAIL=$((FAIL + 1))

echo
if [[ $FAIL -eq 0 ]]; then
  echo "=== All automated lab tests PASSED ==="
else
  echo "=== Some automated lab tests FAILED ($FAIL suite(s)) ==="
  exit 1
fi
