#!/usr/bin/env bash
# Capstone Option A — Incident Triage demo
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source .stack.env 2>/dev/null || { echo "Run ./scripts/start.sh && source .stack.env first"; exit 1; }

API="${API_ENDPOINT:?}"
echo "=== Option A: Happy path ==="
curl -sS -X POST "$API/capstone/incident" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/incident_happy.json" | python3 -m json.tool

echo
echo "=== Option A: Critical path (expect severity=critical + notification stub) ==="
curl -sS -X POST "$API/capstone/incident" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/incident_critical.json" | python3 -m json.tool

echo
echo "=== Option A: Ambiguous (expect needs_review or human_review) ==="
curl -sS -X POST "$API/capstone/incident" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/incident_ambiguous.json" | python3 -m json.tool

if [[ -n "${CAPSTONE_INCIDENT_SM_ARN:-}" ]]; then
  echo
  echo "=== Option A: Step Functions ==="
  EXEC=$(aws stepfunctions start-execution \
    --state-machine-arn "$CAPSTONE_INCIDENT_SM_ARN" \
    --input '{"text":"API 503 in production","correlation_id":"capstone-a-sfn-demo"}' \
    --query executionArn --output text)
  echo "Started: $EXEC"
fi

echo
echo "Audit tip: python week06/query_audit.py capstone-incident-001"
