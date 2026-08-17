#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"
require_cmd curl
require_cmd jq

echo "Lab 05 verification — Event-driven order flow"

export PLATFORM_URL="${PLATFORM_URL:-}"
if [[ -z "$PLATFORM_URL" ]]; then
  export BASE_URL_USER="http://localhost:8001"
  export BASE_URL_PRODUCT="http://localhost:8002"
  export BASE_URL_ORDER="http://localhost:8003"
  export BASE_URL_NOTIFY="http://localhost:8004"
  "${ROOT}/scripts/demo-platform.sh"
  EVENTS=$(curl -sf "http://localhost:8004/events")
else
  PLATFORM_URL="$PLATFORM_URL" "${ROOT}/scripts/demo-platform.sh"
  sleep 2
  EVENTS=$(curl -sf "${PLATFORM_URL}/events")
fi

echo "$EVENTS" | jq -e '.events | map(select(.detail_type == "OrderPlaced")) | length >= 1' >/dev/null \
  || fail "OrderPlaced event not found"
pass "OrderPlaced event received by notification-service"

if [[ -f "${ROOT}/contracts/events/order-placed.json" ]]; then
  pass "Event schema contract exists"
fi

echo "Lab 05 PASSED"
