#!/usr/bin/env bash
# Run all lab verification scripts (local + AWS if PLATFORM_URL set)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAILED=0

for i in 01 02 03 04 05 06 07 08 09; do
  script="${ROOT}/labs/module-${i}/verify.sh"
  if [[ -x "$script" ]]; then
    echo ""
    echo "##############################"
    echo "# Lab Module ${i}"
    echo "##############################"
    if ! "$script"; then
      FAILED=1
    fi
  else
    echo "WARN: missing ${script}"
    FAILED=1
  fi
done

if [[ $FAILED -eq 0 ]]; then
  echo ""
  echo "All lab verifications PASSED"
  exit 0
fi
echo "Some lab verifications FAILED"
exit 1
