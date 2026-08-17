#!/usr/bin/env bash
# Demo: client retry — same Idempotency-Key, no double charge
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8091}"
KEY="demo-$(date +%s)"
BODY='{"amount": 49.99, "currency": "USD"}'

echo "==> POST payment (Idempotency-Key: $KEY)"
curl -sS -X POST "$BASE_URL/v1/payments" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $KEY" \
  -H "X-Tenant-Id: demo" \
  -d "$BODY" | python3 -m json.tool

echo "==> Retry same key"
curl -sS -X POST "$BASE_URL/v1/payments" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $KEY" \
  -H "X-Tenant-Id: demo" \
  -d "$BODY" | python3 -m json.tool

echo "==> Ledger count (via health)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — payment_id should match; ledger_entries should be 1"
