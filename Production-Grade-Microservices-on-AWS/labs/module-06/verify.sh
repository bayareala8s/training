#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"
require_cmd aws

echo "Lab 06 verification — Data layer"

[[ -f "${ROOT}/contracts/events/order-placed.json" ]] || fail "missing event schema"
pass "Event schema present"

TABLE=$(aws dynamodb list-tables --query "TableNames[?contains(@, 'ms-course') && contains(@, 'orders')]" \
  --output text --region "${AWS_REGION:-us-east-1}" 2>/dev/null || true)
if [[ -n "$TABLE" ]]; then
  pass "DynamoDB orders table: ${TABLE}"
else
  skip "DynamoDB table not found (optional until extended implementation)"
fi

echo "Lab 06 PASSED"
