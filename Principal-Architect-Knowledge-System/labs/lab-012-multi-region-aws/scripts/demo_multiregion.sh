#!/usr/bin/env bash
# Demo: multi-region AWS — config validation and failover simulation
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8102}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/config/validate (use_example)"
curl -sS -X POST "$BASE_URL/v1/config/validate" \
  -H "Content-Type: application/json" \
  -d '{"use_example": true}' | python3 -m json.tool

echo "==> POST /v1/failover/simulate (dry_run)"
curl -sS -X POST "$BASE_URL/v1/failover/simulate" \
  -H "Content-Type: application/json" \
  -d '{"dry_run": true}' | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — config valid; failover steps returned in dry-run mode"
