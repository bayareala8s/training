#!/usr/bin/env bash
# Deploy course platform and verify all labs are runnable (no teardown).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
PASS=0
FAIL=0

ok()   { echo -e "${GREEN}✓${NC} $*"; PASS=$((PASS + 1)); }
fail() { echo -e "${RED}✗${NC} $*"; FAIL=$((FAIL + 1)); }

echo "=== CNDE Ensure Labs Running ==="
echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

# Deploy if needed
BUCKET=$(terraform -chdir="${REPO_ROOT}/infrastructure/environments/dev" output -raw data_lake_bucket 2>/dev/null || echo "")
if [[ -z "$BUCKET" ]] || ! aws s3api head-bucket --bucket "$BUCKET" &>/dev/null; then
  echo "Deploying infrastructure..."
  "${SCRIPT_DIR}/start-labs.sh"
else
  echo "Infrastructure already deployed (${BUCKET})"
fi

# shellcheck source=/dev/null
source "${SCRIPT_DIR}/lab-env.sh"

echo
echo "=== Infrastructure verification ==="
"${SCRIPT_DIR}/verify-labs.sh" || true

echo
echo "=== Quick lab smoke tests (non-destructive) ==="

# M1 zones
for zone in raw cleaned curated quarantine metadata; do
  aws s3 ls "s3://${BUCKET}/${zone}/" &>/dev/null && ok "Lab 1.x: zone ${zone}/" || fail "Lab 1.x: zone ${zone}/"
done

# M2 Lambda
aws lambda invoke --function-name "$FN_FILE" \
  --payload '{"records":[{"record_id":"health-001","amount":1.00,"currency":"USD"}]}' \
  --cli-binary-format raw-in-base64-out /tmp/cnde-health.json &>/dev/null \
  && ok "Lab 2.1: Lambda file ingest" || fail "Lab 2.1: Lambda file ingest"

# M4 local
"$PYTHON" "${LAB41}/src/quality_runner.py" \
  --rules "${LAB41}/rules/orders_rules.json" \
  --input "${LAB41}/sample-data/orders_sample.json" \
  --output-dir /tmp/cnde-health-m4 &>/dev/null \
  && ok "Lab 4.1: Quality runner (local)" || fail "Lab 4.1: Quality runner"

# M4.2 Lambda
aws lambda invoke --function-name "$QV_LAMBDA" \
  --payload '{"dataset":"retail/orders","processing_date":"2024-01-15"}' \
  --cli-binary-format raw-in-base64-out /tmp/cnde-health-42.json &>/dev/null \
  && ok "Lab 4.2: Quality validation Lambda" || fail "Lab 4.2: Quality validation Lambda"

# M8 dashboard
aws cloudwatch get-dashboard --dashboard-name "$DASHBOARD" &>/dev/null \
  && ok "Lab 8.1: CloudWatch dashboard" || fail "Lab 8.1: CloudWatch dashboard"

# M9 local
rm -rf /tmp/cnde-health-m9
"$PYTHON" "${LAB91}/src/prepare_ml_dataset.py" --output /tmp/cnde-health-m9 &>/dev/null \
  && ok "Lab 9.1: ML dataset prep" || fail "Lab 9.1: ML dataset prep"
"$PYTHON" "${LAB93}/src/ai_quality_validator.py" \
  --data-dir /tmp/cnde-health-m9 --output /tmp/cnde-health-m9/out &>/dev/null \
  && ok "Lab 9.3: AI quality validator" || fail "Lab 9.3: AI quality validator"

echo
echo "=== Summary ==="
echo "PASS: ${PASS}  FAIL: ${FAIL}"
echo
echo "Platform is RUNNING. Tear down with: ./scripts/stop-labs.sh --yes"
echo "Demo guide: docs/LAB-DEMO-GUIDE.md"
echo "Load env:   source ./scripts/lab-env.sh"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
