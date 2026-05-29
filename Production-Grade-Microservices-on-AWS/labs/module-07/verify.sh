#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"
require_cmd curl
require_cmd jq

echo "Lab 07 verification — Security"

BASE="${BASE_USER:-http://localhost:8001}"
EMAIL="lab07-$(date +%s)@example.com"
curl -sf -X POST "${BASE}/users" -H "Content-Type: application/json" \
  -d "{\"email\":\"${EMAIL}\",\"name\":\"Sec\",\"password\":\"password123\"}" >/dev/null
pass "User registration"

TOKEN=$(curl -sf -X POST "${BASE}/auth/login" -H "Content-Type: application/json" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"password123\"}" | jq -r '.access_token')
[[ ${#TOKEN} -gt 20 ]] || fail "JWT missing"
pass "JWT issued"

[[ -f "${ROOT}/templates/security-checklist.md" ]] || fail "security checklist template missing"
pass "Security checklist template exists"

echo "Lab 07 PASSED"
