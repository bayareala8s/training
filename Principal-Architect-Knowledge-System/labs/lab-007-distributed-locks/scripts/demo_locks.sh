#!/usr/bin/env bash
# Demo: distributed locks — acquire, fence, write, stale rejection
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8100}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/locks/acquire"
ACQUIRE=$(curl -sS -X POST "$BASE_URL/v1/locks/acquire" \
  -H "Content-Type: application/json" \
  -d '{"resource_id": "blob-1", "ttl_ms": 5000}')
echo "$ACQUIRE" | python3 -m json.tool
TOKEN=$(echo "$ACQUIRE" | python3 -c "import sys,json; print(json.load(sys.stdin)['lock']['Token'])")

echo "==> POST /v1/fencing/issue"
FENCE=$(curl -sS -X POST "$BASE_URL/v1/fencing/issue" \
  -H "Content-Type: application/json" \
  -d '{"resource_id": "blob-1"}')
echo "$FENCE" | python3 -m json.tool
FENCE_ID=$(echo "$FENCE" | python3 -c "import sys,json; print(json.load(sys.stdin)['fence_id'])")

echo "==> POST /v1/resource/write (valid fence)"
curl -sS -X POST "$BASE_URL/v1/resource/write" \
  -H "Content-Type: application/json" \
  -d "{\"resource_id\": \"blob-1\", \"fence_id\": $FENCE_ID, \"data\": \"payload\"}" | python3 -m json.tool

echo "==> POST /v1/locks/release"
curl -sS -X POST "$BASE_URL/v1/locks/release" \
  -H "Content-Type: application/json" \
  -d "{\"resource_id\": \"blob-1\", \"token\": \"$TOKEN\"}" | python3 -m json.tool

echo "==> POST /v1/locks/acquire (new holder)"
curl -sS -X POST "$BASE_URL/v1/locks/acquire" \
  -H "Content-Type: application/json" \
  -d '{"resource_id": "blob-1", "ttl_ms": 5000}' | python3 -m json.tool

echo "==> POST /v1/resource/write (stale fence — should reject)"
curl -sS -X POST "$BASE_URL/v1/resource/write" \
  -H "Content-Type: application/json" \
  -d "{\"resource_id\": \"blob-1\", \"fence_id\": $FENCE_ID, \"data\": \"stale\"}" | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — fencing_rejects should be >= 1"
