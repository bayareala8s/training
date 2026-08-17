#!/usr/bin/env bash
# Demo: transactional outbox — atomic write, relay, idempotent consumer
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8092}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/orders (atomic order + outbox)"
curl -sS -X POST "$BASE_URL/v1/orders" \
  -H "Content-Type: application/json" \
  -d '{"sku": "SKU-100", "quantity": 2}' | python3 -m json.tool

echo "==> GET /v1/outbox?pending=true"
curl -sS "$BASE_URL/v1/outbox?pending=true" | python3 -m json.tool

echo "==> POST /v1/relay/run"
curl -sS -X POST "$BASE_URL/v1/relay/run" | python3 -m json.tool

echo "==> POST /v1/consumer/run (first time)"
curl -sS -X POST "$BASE_URL/v1/consumer/run" | python3 -m json.tool

echo "==> POST /v1/consumer/run (duplicate — should dedupe)"
curl -sS -X POST "$BASE_URL/v1/consumer/run" | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — outbox_pending should be 0; consumer duplicates on second run"
