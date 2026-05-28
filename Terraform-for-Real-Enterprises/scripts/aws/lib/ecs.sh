#!/usr/bin/env bash

ecs_scale_lab_services() {
  local desired="$1"
  local clusters
  clusters=$(aws ecs list-clusters --region "$AWS_REGION" --query 'clusterArns[]' --output text 2>/dev/null || true)

  for cluster_arn in $clusters; do
    local cluster
    cluster=$(basename "$cluster_arn")
    local services
    services=$(aws ecs list-services --region "$AWS_REGION" --cluster "$cluster" \
      --query 'serviceArns[]' --output text 2>/dev/null || true)

    for svc_arn in $services; do
      local svc
      svc=$(basename "$svc_arn")
      local tags
      tags=$(aws ecs list-tags-for-resource --region "$AWS_REGION" \
        --resource-arn "$svc_arn" --query 'tags' --output json 2>/dev/null || echo "[]")

      if echo "$tags" | grep -q "\"key\": \"${LAB_TAG_KEY}\"" && \
         echo "$tags" | grep -q "\"value\": \"${LAB_TAG_VALUE}\""; then
        log INFO "ECS: scaling $cluster/$svc desiredCount=$desired"
        run_cmd aws ecs update-service --region "$AWS_REGION" \
          --cluster "$cluster" --service "$svc" --desired-count "$desired" \
          --no-cli-pager >/dev/null
      fi
    done
  done
}

ecs_stop_lab_services() {
  ecs_scale_lab_services 0
}

ecs_start_lab_services() {
  local count="${ECS_LAB_DESIRED_COUNT:-1}"
  ecs_scale_lab_services "$count"
}

ecs_lab_status() {
  log INFO "ECS: check services tagged ${LAB_TAG_KEY}=${LAB_TAG_VALUE} in console or use aws ecs describe-services"
}
