#!/usr/bin/env bash
# Capstone Option C — Approval Workflow demo
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source .stack.env 2>/dev/null || { echo "Run ./scripts/start.sh && source .stack.env first"; exit 1; }

API="${API_ENDPOINT:?}"
echo "=== Option C: Low risk → auto execute ==="
curl -sS -X POST "$API/capstone/approval/request" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/approval_low_risk.json" | python3 -m json.tool

echo
echo "=== Option C: High risk → pending ==="
RESP=$(curl -sS -X POST "$API/capstone/approval/request" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/approval_high_risk.json")
echo "$RESP" | python3 -m json.tool
APPROVAL_ID=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('approval_id',''))")

if [[ -n "$APPROVAL_ID" ]]; then
  echo
  echo "=== Option C: Decide approve ($APPROVAL_ID) ==="
  curl -sS -X POST "$API/capstone/approval/decide" \
    -H "Content-Type: application/json" \
    -d "{\"approval_id\":\"$APPROVAL_ID\",\"decision\":\"approve\",\"correlation_id\":\"capstone-approval-high\",\"approver_id\":\"instructor\"}" \
    | python3 -m json.tool
fi

if [[ -n "${CAPSTONE_APPROVAL_SM_ARN:-}" ]]; then
  echo
  echo "=== Option C: Step Functions ==="
  aws stepfunctions start-execution \
    --state-machine-arn "$CAPSTONE_APPROVAL_SM_ARN" \
    --input '{"action_text":"Rotate production API keys","correlation_id":"capstone-c-sfn-demo"}' \
    --query executionArn --output text
fi
