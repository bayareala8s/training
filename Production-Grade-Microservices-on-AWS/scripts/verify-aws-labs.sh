#!/usr/bin/env bash
# Verify all labs against AWS (requires ./scripts/aws-start.sh first)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TF_DIR="${ROOT}/infrastructure/terraform"

export PLATFORM_URL="$(terraform -chdir="$TF_DIR" output -raw platform_url 2>/dev/null || true)"
export AWS_REGION="${AWS_REGION:-us-east-1}"

if [[ -z "$PLATFORM_URL" ]]; then
  echo "Platform URL not available. Run: ./scripts/aws-start.sh"
  exit 1
fi

echo "Verifying AWS platform at ${PLATFORM_URL}"
echo ""

FAILED=0
for i in 04 05 06 07 08; do
  script="${ROOT}/labs/module-${i}/verify.sh"
  echo "##############################"
  echo "# Lab Module ${i} (AWS)"
  echo "##############################"
  if ! "$script"; then
    FAILED=1
  fi
done

PLATFORM_URL="$PLATFORM_URL" "${ROOT}/scripts/demo-platform.sh"

if [[ $FAILED -eq 0 ]]; then
  echo ""
  echo "AWS lab verifications PASSED"
  exit 0
fi
echo "Some AWS lab verifications FAILED"
exit 1
