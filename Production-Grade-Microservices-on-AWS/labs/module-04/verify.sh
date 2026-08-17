#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"
require_cmd aws
require_cmd jq

echo "Lab 04 verification — AWS ECS deployment"

TF_DIR="${ROOT}/infrastructure/terraform"
ACTIVE=$(terraform -chdir="$TF_DIR" output -raw platform_active 2>/dev/null || echo "false")

if [[ "$ACTIVE" != "true" ]]; then
  fail "Platform not active. Run: ./scripts/aws-start.sh"
fi

URL=$(terraform -chdir="$TF_DIR" output -raw platform_url)
CLUSTER=$(terraform -chdir="$TF_DIR" output -raw ecs_cluster_name)

curl -sf "${URL}/products" | jq -e 'length >= 1' >/dev/null || fail "ALB /products"
pass "ALB routing to product-service"

for svc in user-service product-service order-service notification-service; do
  COUNT=$(aws ecs describe-services --cluster "$CLUSTER" --services "$svc" \
    --query 'services[0].runningCount' --output text --region "${AWS_REGION:-us-east-1}")
  [[ "$COUNT" -ge 1 ]] || fail "${svc} running count=${COUNT}"
  pass "${svc} running (${COUNT} task)"
done

echo "Lab 04 PASSED"
