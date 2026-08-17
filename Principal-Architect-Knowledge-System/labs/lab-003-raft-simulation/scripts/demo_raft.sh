#!/usr/bin/env bash
# Demo: Raft simulation — leader election, log replication, peer inspection
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8098}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/cluster/elect-leader"
curl -sS -X POST "$BASE_URL/v1/cluster/elect-leader" | python3 -m json.tool

echo "==> GET /v1/peers"
curl -sS "$BASE_URL/v1/peers" | python3 -m json.tool

echo "==> POST /v1/log/append (set x=1)"
curl -sS -X POST "$BASE_URL/v1/log/append" \
  -H "Content-Type: application/json" \
  -d '{"command": "set x=1"}' | python3 -m json.tool

echo "==> POST /v1/log/append (set y=2)"
curl -sS -X POST "$BASE_URL/v1/log/append" \
  -H "Content-Type: application/json" \
  -d '{"command": "set y=2"}' | python3 -m json.tool

echo "==> POST /v1/cluster/elect-leader (new term — committed entries survive)"
curl -sS -X POST "$BASE_URL/v1/cluster/elect-leader" | python3 -m json.tool

echo "==> GET /v1/peers (commit_index should reflect replicated entries)"
curl -sS "$BASE_URL/v1/peers" | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — append_total should be 2 and commit_index >= 1 on peers"
