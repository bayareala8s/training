#!/usr/bin/env bash
# Shared AWS course platform helpers
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TF_DIR="${ROOT_DIR}/infrastructure/terraform"
export AWS_REGION="${AWS_REGION:-us-east-1}"
export PROJECT_NAME="${PROJECT_NAME:-ms-course}"
export ENVIRONMENT="${ENVIRONMENT:-dev}"

tf() {
  terraform -chdir="${TF_DIR}" "$@"
}

tf_output() {
  tf output -raw "$1" 2>/dev/null || true
}

require_tools() {
  for cmd in terraform aws docker; do
    command -v "$cmd" >/dev/null || { echo "Missing required command: $cmd"; exit 1; }
  done
}

ecr_login() {
  local account region registry
  account="$(aws sts get-caller-identity --query Account --output text)"
  region="${AWS_REGION}"
  registry="${account}.dkr.ecr.${region}.amazonaws.com"
  aws ecr get-login-password --region "$region" | \
    docker login --username AWS --password-stdin "$registry" >/dev/null
  echo "$registry"
}

build_and_push_images() {
  local registry prefix tag
  registry="$(ecr_login | tail -1)"
  prefix="${PROJECT_NAME}-${ENVIRONMENT}"
  tag="${IMAGE_TAG:-latest}"

  for svc in user-service product-service order-service notification-service; do
    local repo="${registry}/${prefix}-${svc}"
    echo "==> Building and pushing ${svc} -> ${repo}:${tag}"
    # ECS Fargate requires linux/amd64 (images built on Apple Silicon are arm64 by default)
    docker build --platform linux/amd64 -t "${repo}:${tag}" "${ROOT_DIR}/starters/python/${svc}"
    docker push "${repo}:${tag}"
  done
}

wait_for_ecs_steady() {
  local cluster max attempt running desired
  cluster="$(tf_output ecs_cluster_name)"
  max=40
  echo "==> Waiting for ECS services to stabilize in cluster ${cluster}..."
  for svc in user-service product-service order-service notification-service; do
    attempt=0
    while true; do
      read -r running desired <<< "$(aws ecs describe-services --cluster "$cluster" --services "$svc" \
        --region "$AWS_REGION" \
        --query 'services[0].[runningCount,desiredCount]' --output text)"
      if [[ "$running" == "$desired" && "$desired" -ge 1 ]]; then
        echo "    ${svc} ready (${running}/${desired})"
        break
      fi
      attempt=$((attempt + 1))
      if [[ $attempt -ge $max ]]; then
        echo "    WARN: ${svc} not stable (${running}/${desired}) — check CloudWatch /ecs/ms-course-dev"
        break
      fi
      sleep 15
    done
  done
}

wait_for_alb_healthy() {
  local url max attempts
  url="$(tf_output platform_url)"
  max=30
  attempts=0
  echo "==> Waiting for ALB at ${url}..."
  until curl -sf "${url}/products" >/dev/null 2>&1; do
    attempts=$((attempts + 1))
    if [[ $attempts -ge $max ]]; then
      echo "ALB not ready after ${max} attempts"
      return 1
    fi
    sleep 10
  done
  echo "==> ALB is serving traffic"
}
