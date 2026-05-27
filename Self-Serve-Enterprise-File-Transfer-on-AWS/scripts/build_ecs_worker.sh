#!/usr/bin/env bash
# Build and push the Lab 9 Fargate worker image to ECR.
# Run after: terraform apply (ECR repo must exist)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

baylearn_require_tools
command -v docker >/dev/null 2>&1 || { echo "docker required" >&2; exit 1; }

export AWS_REGION="$(baylearn_aws_region)"
REPO="$(baylearn_tf_raw ecr_repository_url)"
TAG="${ECS_IMAGE_TAG:-latest}"

if [[ -z "$REPO" || "$REPO" == "null" ]]; then
  echo "ecr_repository_url not found. Set enable_ecs_worker=true and run terraform apply first." >&2
  exit 1
fi

# Fargate tasks run linux/amd64; build for that arch on Apple Silicon hosts too.
PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"
echo "==> docker build --platform ${PLATFORM} ${REPO}:${TAG}"
docker build --platform "$PLATFORM" -t "${REPO}:${TAG}" "$BAYLEARN_ROOT/app/workers/fargate"

echo "==> ECR login"
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "${REPO%%/*}"

echo "==> docker push"
docker push "${REPO}:${TAG}"

echo "OK: pushed ${REPO}:${TAG}"
