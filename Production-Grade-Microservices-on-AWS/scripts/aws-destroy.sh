#!/usr/bin/env bash
# Destroy ALL AWS resources for this course (run after aws-stop.sh or alone)
set -euo pipefail
source "$(dirname "$0")/aws/lib.sh"

require_tools

echo "=============================================="
echo "  AWS DESTROY — Full teardown"
echo "=============================================="
read -r -p "This will DELETE all course AWS resources. Type 'destroy' to confirm: " confirm
[[ "$confirm" == "destroy" ]] || { echo "Aborted."; exit 1; }

cd "${TF_DIR}"
terraform init -input=false

echo "==> Scaling down first..."
terraform apply -input=false -auto-approve \
  -var="platform_active=false" \
  -var="ecs_desired_count=0" || true

echo "==> Destroying all resources..."
terraform destroy -input=false -auto-approve \
  -var="platform_active=false"

echo "All course infrastructure destroyed."
