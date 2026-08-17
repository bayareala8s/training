#!/usr/bin/env bash
# Demo: Kafka stream processing — produce, enrich, aggregate, DLT
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8094}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/orders (produce 3 orders)"
for i in 1 2 3; do
  curl -sS -X POST "$BASE_URL/v1/orders" \
    -H "Content-Type: application/json" \
    -d "{\"customer_id\": \"cust-42\", \"amount\": $((i * 25)).0, \"region\": \"us-west\", \"order_id\": \"ord-$i\"}" \
    | python3 -m json.tool
done

echo "==> GET /v1/topics/orders"
curl -sS "$BASE_URL/v1/topics/orders" | python3 -m json.tool

echo "==> POST /v1/enricher/run"
curl -sS -X POST "$BASE_URL/v1/enricher/run" | python3 -m json.tool

echo "==> POST /v1/aggregator/run"
curl -sS -X POST "$BASE_URL/v1/aggregator/run" | python3 -m json.tool

echo "==> GET /v1/metrics"
curl -sS "$BASE_URL/v1/metrics" | python3 -m json.tool

echo "==> POST /v1/poison/inject"
curl -sS -X POST "$BASE_URL/v1/poison/inject" | python3 -m json.tool

echo "==> POST /v1/enricher/run (poison → DLT)"
curl -sS -X POST "$BASE_URL/v1/enricher/run" | python3 -m json.tool

echo "==> GET /v1/dlt"
curl -sS "$BASE_URL/v1/dlt" | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — metrics windows >= 1; dlt_messages >= 1"
