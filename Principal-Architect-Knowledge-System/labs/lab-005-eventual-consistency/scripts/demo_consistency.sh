#!/usr/bin/env bash
# Demo: eventual consistency — write, stale read, replicate, converge, partition
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8099}"

echo "==> Health"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/keys/user:1 (write on r1)"
curl -sS -X POST "$BASE_URL/v1/keys/user:1" \
  -H "Content-Type: application/json" \
  -d '{"value": "alice", "replica_id": "r1"}' | python3 -m json.tool

echo "==> GET /v1/keys/user:1?replica=r2 (stale before replication)"
curl -sS "$BASE_URL/v1/keys/user:1?replica=r2" | python3 -m json.tool

echo "==> POST /v1/replicate/run"
curl -sS -X POST "$BASE_URL/v1/replicate/run" | python3 -m json.tool

echo "==> GET /v1/keys/user:1?replica=r2 (after replication)"
curl -sS "$BASE_URL/v1/keys/user:1?replica=r2" | python3 -m json.tool

echo "==> POST /v1/chaos/partition (isolate r3)"
curl -sS -X POST "$BASE_URL/v1/chaos/partition" \
  -H "Content-Type: application/json" \
  -d '{"replicas": ["r3"], "enabled": true}' | python3 -m json.tool

echo "==> POST /v1/keys/user:2 on r1 + replicate (r3 should lag)"
curl -sS -X POST "$BASE_URL/v1/keys/user:2" \
  -H "Content-Type: application/json" \
  -d '{"value": "bob", "replica_id": "r1"}' | python3 -m json.tool
curl -sS -X POST "$BASE_URL/v1/replicate/run" | python3 -m json.tool

echo "==> POST /v1/keys/user:2/repair (read repair)"
curl -sS -X POST "$BASE_URL/v1/keys/user:2/repair" | python3 -m json.tool

echo "Done — r2 should show user:1 and user:2 after replication/repair"
