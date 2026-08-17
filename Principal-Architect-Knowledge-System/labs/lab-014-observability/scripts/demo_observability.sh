#!/usr/bin/env bash
# Demo: observability — simulate requests, scrape metrics, view traces
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8104}"

echo "==> Health"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/requests/simulate (3 routes)"
for route in /health /api /orders; do
  curl -sS -X POST "$BASE_URL/v1/requests/simulate" \
    -H "Content-Type: application/json" \
    -d "{\"route\": \"$route\"}" | python3 -m json.tool
done

echo "==> GET /metrics (Prometheus text)"
curl -sS "$BASE_URL/metrics"

echo ""
echo "==> GET /v1/traces"
curl -sS "$BASE_URL/v1/traces?limit=5" | python3 -m json.tool

echo "==> POST /v1/chaos/inject (error spike 50%)"
curl -sS -X POST "$BASE_URL/v1/chaos/inject" \
  -H "Content-Type: application/json" \
  -d '{"inject": "error-spike", "rate": 0.5}' | python3 -m json.tool

echo "Done — metrics at /metrics, traces at /v1/traces, Grafana at :3000"
