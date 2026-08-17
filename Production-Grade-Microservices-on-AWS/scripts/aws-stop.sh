#!/usr/bin/env bash
# Stop course platform on AWS — scales ECS to 0, removes NAT and ALB (main cost drivers)
set -euo pipefail
source "$(dirname "$0")/aws/lib.sh"

require_tools

echo "=============================================="
echo "  AWS STOP — Minimizing idle cost"
echo "=============================================="
echo "Stops: ECS tasks, ALB, NAT Gateway"
echo "Keeps: VPC, ECR images, DynamoDB, EventBridge (low/no idle cost)"
echo ""

# Scale ECS immediately (stops Fargate billing before slow Terraform run)
cluster="$(terraform -chdir="${TF_DIR}" output -raw ecs_cluster_name 2>/dev/null || echo "ms-course-dev-cluster")"
echo "==> Scaling ECS services to 0..."
for svc in user-service product-service order-service notification-service; do
  aws ecs update-service --cluster "$cluster" --service "$svc" \
    --desired-count 0 --region "$AWS_REGION" >/dev/null 2>&1 || true
done
echo "    ECS tasks stopping (Fargate charges end when tasks stop)"

cd "${TF_DIR}"
terraform init -input=false

terraform apply -input=false -auto-approve \
  -var="platform_active=false" \
  -var="ecs_desired_count=0"

echo ""
echo "Platform STOPPED — idle cost minimized."
echo "  Restart: ./scripts/aws-start.sh"
echo "  Full teardown: ./scripts/aws-destroy.sh"
