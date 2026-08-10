#!/usr/bin/env bash
# Start course platform on AWS (creates NAT/ALB/ECS, builds and deploys images)
set -euo pipefail
source "$(dirname "$0")/aws/lib.sh"

require_tools

echo "=============================================="
echo "  AWS START — Production Microservices Course"
echo "=============================================="

cd "${TF_DIR}"
terraform init -input=false

echo "==> Phase 1: Ensure base infrastructure + ECR exist"
CURRENT_ACTIVE="$(terraform output -raw platform_active 2>/dev/null || echo "false")"
if [[ "$CURRENT_ACTIVE" == "true" ]]; then
  echo "    Platform currently active — scaling down before image push"
  for svc in user-service product-service order-service notification-service; do
    cluster="$(terraform output -raw ecs_cluster_name 2>/dev/null || echo "ms-course-dev-cluster")"
    aws ecs update-service --cluster "$cluster" --service "$svc" \
      --desired-count 0 --region "$AWS_REGION" >/dev/null 2>&1 || true
  done
fi
terraform apply -input=false -auto-approve \
  -var="platform_active=false" \
  -var="ecs_desired_count=0"

echo "==> Phase 2: Build and push container images"
build_and_push_images

echo "==> Phase 3: Activate platform (NAT, ALB, ECS tasks)"
terraform apply -input=false -auto-approve \
  -var="platform_active=true" \
  -var="ecs_desired_count=1"

wait_for_ecs_steady
wait_for_alb_healthy

PLATFORM_URL="$(tf_output platform_url)"
echo ""
echo "Platform STARTED"
echo "  URL: ${PLATFORM_URL}"
echo "  Products: ${PLATFORM_URL}/products"
echo "  Run demo: PLATFORM_URL=${PLATFORM_URL} ./scripts/demo-platform.sh"
echo ""
echo "To stop billing for compute/NAT/ALB: ./scripts/aws-stop.sh"
