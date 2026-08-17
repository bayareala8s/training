#!/usr/bin/env bash
# Demo: saga orchestration — happy path, compensation, crash recovery
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8093}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/sagas (happy path)"
HAPPY=$(curl -sS -X POST "$BASE_URL/v1/sagas" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PROD-100", "idempotency_key": "demo-happy"}')
echo "$HAPPY" | python3 -m json.tool
SAGA_ID=$(echo "$HAPPY" | python3 -c "import sys,json; print(json.load(sys.stdin)['saga']['id'])")

echo "==> GET /v1/sagas/$SAGA_ID"
curl -sS "$BASE_URL/v1/sagas/$SAGA_ID" | python3 -m json.tool

echo "==> POST /v1/chaos/inventory-fail"
curl -sS -X POST "$BASE_URL/v1/chaos/inventory-fail" | python3 -m json.tool

echo "==> POST /v1/sagas (inventory fails → compensate payment)"
curl -sS -X POST "$BASE_URL/v1/sagas" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PROD-200", "idempotency_key": "demo-fail"}' | python3 -m json.tool

echo "==> POST /v1/chaos/reset"
curl -sS -X POST "$BASE_URL/v1/chaos/reset" | python3 -m json.tool

echo "==> POST /v1/sagas (idempotent retry — same key)"
curl -sS -X POST "$BASE_URL/v1/sagas" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PROD-100", "idempotency_key": "demo-happy"}' | python3 -m json.tool

echo "==> POST /v1/sagas/$SAGA_ID/crash (simulate crash after payment)"
curl -sS -X POST "$BASE_URL/v1/sagas/$SAGA_ID/crash" \
  -H "Content-Type: application/json" \
  -d '{"state": "payment_reserved"}' | python3 -m json.tool

echo "==> POST /v1/sagas/$SAGA_ID/recover"
curl -sS -X POST "$BASE_URL/v1/sagas/$SAGA_ID/recover" | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — sagas_completed and sagas_compensated should both be >= 1"
