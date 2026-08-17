#!/usr/bin/env bash
# Demo: distributed rate limiter — check, throttle, redis-down chaos
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8101}"

echo "==> Health"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/check (tenant-1 /api) x3"
for i in 1 2 3; do
  echo "--- check $i ---"
  curl -sS -X POST "$BASE_URL/v1/check" \
    -H "Content-Type: application/json" \
    -d '{"tenant_id": "tenant-1", "route": "/api"}' -w "\nHTTP %{http_code}\n" | python3 -m json.tool || true
done

echo "==> POST /v1/chaos/redis-down (fail-closed)"
curl -sS -X POST "$BASE_URL/v1/chaos/redis-down" \
  -H "Content-Type: application/json" \
  -d '{"enabled": true, "mode": "fail-closed"}' | python3 -m json.tool

echo "==> POST /v1/check during redis-down"
curl -sS -X POST "$BASE_URL/v1/check" \
  -H "Content-Type: application/json" \
  -d '{"tenant_id": "tenant-1", "route": "/api"}' -w "\nHTTP %{http_code}\n" | python3 -m json.tool || true

echo "==> Restore redis"
curl -sS -X POST "$BASE_URL/v1/chaos/redis-down" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false, "mode": "fail-closed"}' | python3 -m json.tool

echo "Done — observe 429 when over limit; fail-closed denies during redis-down"
