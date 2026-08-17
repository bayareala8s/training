#!/usr/bin/env bash

rds_stop_lab_instances() {
  local arns
  arns=$(aws rds describe-db-instances \
    --region "$AWS_REGION" \
    --query "DBInstances[?contains(TagList[?Key=='${LAB_TAG_KEY}'].Value | [0], '${LAB_TAG_VALUE}') || Tags[?Key=='${LAB_TAG_KEY}' && Value=='${LAB_TAG_VALUE}']].DBInstanceArn" \
    --output text 2>/dev/null || true)

  # Fallback: list by tag API
  local ids
  ids=$(aws resourcegroupstaggingapi get-resources \
    --region "$AWS_REGION" \
    --resource-type-filters "rds:db" \
    --tag-filters "Key=${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
    --query 'ResourceTagMappingList[].ResourceARN' \
    --output text 2>/dev/null || true)

  if [[ -z "$ids" || "$ids" == "None" ]]; then
    log INFO "RDS: no lab DB instances found"
    return 0
  fi

  for arn in $ids; do
    local db_id
    db_id=$(basename "$arn")
    log INFO "RDS: stopping $db_id"
    run_cmd aws rds stop-db-instance --region "$AWS_REGION" --db-instance-identifier "$db_id" 2>/dev/null || \
      log INFO "RDS: $db_id already stopped or not stoppable (check engine)"
  done
}

rds_start_lab_instances() {
  local ids
  ids=$(aws resourcegroupstaggingapi get-resources \
    --region "$AWS_REGION" \
    --resource-type-filters "rds:db" \
    --tag-filters "Key=${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
    --query 'ResourceTagMappingList[].ResourceARN' \
    --output text 2>/dev/null || true)

  if [[ -z "$ids" || "$ids" == "None" ]]; then
    log INFO "RDS: no lab DB instances found"
    return 0
  fi

  for arn in $ids; do
    local db_id
    db_id=$(basename "$arn")
    log INFO "RDS: starting $db_id"
    run_cmd aws rds start-db-instance --region "$AWS_REGION" --db-instance-identifier "$db_id" 2>/dev/null || \
      log INFO "RDS: $db_id already running"
  done
}

rds_lab_status() {
  aws resourcegroupstaggingapi get-resources \
    --region "$AWS_REGION" \
    --resource-type-filters "rds:db" \
    --tag-filters "Key=${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
    --query 'ResourceTagMappingList[].[ResourceARN,Tags]' \
    --output table 2>/dev/null || echo "RDS: none"
}
