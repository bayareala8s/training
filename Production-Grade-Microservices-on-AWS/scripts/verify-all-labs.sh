#!/usr/bin/env bash
# Run all lab verification scripts (local + AWS if platform is active)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TF_DIR="${ROOT}/infrastructure/terraform"
FAILED=0

platform_active() {
  terraform -chdir="$TF_DIR" output -raw platform_active 2>/dev/null || echo "false"
}

for i in 01 02 03 05 06 07 09; do
  script="${ROOT}/labs/module-${i}/verify.sh"
  if [[ -x "$script" ]]; then
    echo ""
    echo "##############################"
    echo "# Lab Module ${i} (local)"
    echo "##############################"
    if ! "$script"; then
      FAILED=1
    fi
  else
    echo "WARN: missing ${script}"
    FAILED=1
  fi
done

ACTIVE="$(platform_active)"
if [[ "$ACTIVE" == "true" ]]; then
  echo ""
  echo "##############################"
  echo "# AWS labs (04, 08) — platform active"
  echo "##############################"
  export PLATFORM_URL="$(terraform -chdir="$TF_DIR" output -raw platform_url 2>/dev/null || true)"
  for i in 04 08; do
    script="${ROOT}/labs/module-${i}/verify.sh"
    if ! "$script"; then
      FAILED=1
    fi
  done
else
  echo ""
  echo "SKIP: Labs 04 and 08 require AWS platform. Run: ./scripts/aws-start.sh && ./scripts/verify-aws-labs.sh"
fi

if [[ $FAILED -eq 0 ]]; then
  echo ""
  echo "All applicable lab verifications PASSED"
  exit 0
fi
echo "Some lab verifications FAILED"
exit 1
