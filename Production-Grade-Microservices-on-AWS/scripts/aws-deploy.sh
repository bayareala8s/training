#!/usr/bin/env bash
# Rebuild linux/amd64 images, push to ECR, force ECS redeploy
set -euo pipefail
source "$(dirname "$0")/aws/lib.sh"

require_tools

echo "==> Rebuilding images for ECS Fargate (linux/amd64)..."
build_and_push_images

cluster="$(tf_output ecs_cluster_name)"
for svc in user-service product-service order-service notification-service; do
  echo "==> Forcing new deployment: ${svc}"
  aws ecs update-service --cluster "$cluster" --service "$svc" \
    --force-new-deployment --region "$AWS_REGION" >/dev/null
done

wait_for_ecs_steady
wait_for_alb_healthy

echo ""
echo "Redeploy complete: $(tf_output platform_url)"
