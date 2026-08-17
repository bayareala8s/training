#!/usr/bin/env bash
# Demo: replicated KV — put, quorum read, replica view, chaos, read repair
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8095}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> PUT /v1/keys/user:42"
curl -sS -X PUT "$BASE_URL/v1/keys/user:42" \
  -H "Content-Type: application/json" \
  -d '{"value": "alice"}' | python3 -m json.tool

echo "==> GET /v1/keys/user:42"
curl -sS "$BASE_URL/v1/keys/user:42" | python3 -m json.tool

echo "==> GET /v1/keys/user:42/replicas"
curl -sS "$BASE_URL/v1/keys/user:42/replicas" | python3 -m json.tool

SHARD=$(curl -sS "$BASE_URL/v1/keys/user:42" | python3 -c "import sys,json; print(json.load(sys.stdin)['shard'])")

echo "==> POST /v1/chaos/replica-down (shard=$SHARD replica=2)"
curl -sS -X POST "$BASE_URL/v1/chaos/replica-down" \
  -H "Content-Type: application/json" \
  -d "{\"shard\": $SHARD, \"replica\": 2}" | python3 -m json.tool

echo "==> PUT /v1/keys/user:99 (still works with W=2, 1 replica down)"
curl -sS -X PUT "$BASE_URL/v1/keys/user:99" \
  -H "Content-Type: application/json" \
  -d '{"value": "bob"}' | python3 -m json.tool

echo "==> GET /v1/keys/user:42?repair=true"
curl -sS "$BASE_URL/v1/keys/user:42?repair=true" | python3 -m json.tool

echo "==> POST /v1/chaos/reset"
curl -sS -X POST "$BASE_URL/v1/chaos/reset" | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — read_repairs should be >= 0; quorum writes succeed with 1 replica down"
