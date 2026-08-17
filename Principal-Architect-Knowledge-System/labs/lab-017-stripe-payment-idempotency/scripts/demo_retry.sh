#!/usr/bin/env bash
# Demo: client retry after ambiguous timeout — no double charge
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8080}"
KEY="demo-$(date +%s)"
BODY='{"amount_cents": 4999, "currency": "usd"}'

echo "==> POST charge (Idempotency-Key: $KEY)"
curl -sS -X POST "$BASE_URL/v1/charges" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $KEY" \
  -H "X-Tenant-Id: demo" \
  -d "$BODY" | jq .

echo "==> Retry same key (simulates client timeout retry)"
curl -sS -X POST "$BASE_URL/v1/charges" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $KEY" \
  -H "X-Tenant-Id: demo" \
  -d "$BODY" | jq .

echo "Done — verify identical payment_intent_id in both responses"
