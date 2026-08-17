#!/usr/bin/env bash
# Demo: consistent hashing — lookup, balance, churn, node failure
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8096}"

echo "==> Health"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> GET /v1/lookup/user:42"
curl -sS "$BASE_URL/v1/lookup/user:42" | python3 -m json.tool

echo "==> POST /v1/nodes (add node-d)"
curl -sS -X POST "$BASE_URL/v1/nodes" \
  -H "Content-Type: application/json" \
  -d '{"node_id": "node-d", "vnode_count": 128}' | python3 -m json.tool

echo "==> POST /v1/simulate/balance"
curl -sS -X POST "$BASE_URL/v1/simulate/balance" \
  -H "Content-Type: application/json" \
  -d '{"key_count": 100000}' | python3 -m json.tool

echo "==> POST /v1/simulate/churn (consistent vs modulo)"
curl -sS -X POST "$BASE_URL/v1/simulate/churn" \
  -H "Content-Type: application/json" \
  -d '{"key_count": 5000}' | python3 -m json.tool

echo "==> POST /v1/simulate/node-failure (node-b)"
curl -sS -X POST "$BASE_URL/v1/simulate/node-failure" \
  -H "Content-Type: application/json" \
  -d '{"node_id": "node-b", "key_count": 10000}' | python3 -m json.tool

echo "Done — consistent_hashing_churn should be much lower than modulo_hashing_churn"
