#!/usr/bin/env bash
set -euo pipefail

# Single ALB URL (AWS) or per-service localhost ports (docker compose)
AWS_MODE=false
if [[ -n "${PLATFORM_URL:-}" ]]; then
  AWS_MODE=true
  BASE_URL_USER="${PLATFORM_URL}"
  BASE_URL_PRODUCT="${PLATFORM_URL}"
  BASE_URL_ORDER="${PLATFORM_URL}"
  BASE_URL_NOTIFY="${PLATFORM_URL}"
else
  BASE_URL_USER="${BASE_URL_USER:-http://localhost:8001}"
  BASE_URL_PRODUCT="${BASE_URL_PRODUCT:-http://localhost:8002}"
  BASE_URL_ORDER="${BASE_URL_ORDER:-http://localhost:8003}"
  BASE_URL_NOTIFY="${BASE_URL_NOTIFY:-http://localhost:8004}"
fi

echo "=== Health / smoke checks ==="
if $AWS_MODE; then
  curl -sf "$BASE_URL_PRODUCT/products" | jq -e 'length >= 1' >/dev/null
  echo "  product-service OK (GET /products)"
  curl -sf "$BASE_URL_NOTIFY/events" | jq -e '.events' >/dev/null
  echo "  notification-service OK (GET /events)"
else
  curl -sf "$BASE_URL_USER/health" | jq .
  curl -sf "$BASE_URL_PRODUCT/health" | jq .
  curl -sf "$BASE_URL_ORDER/health" | jq .
  curl -sf "$BASE_URL_NOTIFY/health" | jq .
fi

echo "=== Create user ==="
DEMO_EMAIL="demo-$(date +%s)@example.com"
USER_JSON=$(curl -sf -X POST "$BASE_URL_USER/users" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${DEMO_EMAIL}\",\"name\":\"Demo Student\",\"password\":\"learn12345\"}")
echo "$USER_JSON" | jq .
USER_ID=$(echo "$USER_JSON" | jq -r .id)
[[ -n "$USER_ID" && "$USER_ID" != "null" ]] || { echo "Failed to create user"; exit 1; }

echo "=== List products ==="
PRODUCTS=$(curl -sf "$BASE_URL_PRODUCT/products")
echo "$PRODUCTS" | jq .
PRODUCT_ID=$(echo "$PRODUCTS" | jq -r '.[0].id')

echo "=== Place order ==="
ORDER_JSON=$(curl -sf -X POST "$BASE_URL_ORDER/orders" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"$USER_ID\",\"items\":[{\"product_id\":\"$PRODUCT_ID\",\"quantity\":1}]}")
echo "$ORDER_JSON" | jq .

echo "=== Notification events ==="
sleep 1
curl -sf "$BASE_URL_NOTIFY/events" | jq .

echo "=== Demo complete ==="
