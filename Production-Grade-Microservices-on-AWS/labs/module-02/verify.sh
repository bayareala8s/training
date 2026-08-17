#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"
require_cmd curl
require_cmd jq

echo "Lab 02 verification — User & Product APIs"

if $LOCAL_MODE; then
  curl -sf "${BASE_USER}/health" | jq -e '.service == "user-service"' >/dev/null || fail "user health"
  curl -sf "${BASE_PRODUCT}/health" | jq -e '.service == "product-service"' >/dev/null || fail "product health"
else
  curl -sf "${BASE_PRODUCT}/products" | jq -e 'length >= 1' >/dev/null || fail "products list via ALB"
fi

EMAIL="lab02-$(date +%s)@example.com"
USER_JSON=$(curl -sf -X POST "${BASE_USER}/users" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${EMAIL}\",\"name\":\"Lab02\",\"password\":\"password123\"}")
echo "$USER_JSON" | jq -e '.id' >/dev/null || fail "create user"
pass "POST /users"

TOKEN=$(curl -sf -X POST "${BASE_USER}/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"password123\"}" | jq -r '.access_token')
[[ -n "$TOKEN" && "$TOKEN" != "null" ]] || fail "login"
pass "POST /auth/login"

curl -sf "${BASE_PRODUCT}/products" | jq -e 'length >= 1' >/dev/null || fail "list products"
pass "GET /products"

echo "Lab 02 PASSED"
