#!/usr/bin/env bash

ec2_stop_lab_instances() {
  local ids
  ids=$(aws ec2 describe-instances \
    --region "$AWS_REGION" \
    --filters \
      "Name=instance-state-name,Values=running,pending" \
      "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
    --query 'Reservations[].Instances[].InstanceId' \
    --output text 2>/dev/null || true)
  ids=$(echo "$ids" | tr '\t\n' ' ' | xargs)

  if [[ -z "$ids" || "$ids" == "None" ]]; then
    log INFO "EC2: no running lab instances found"
    return 0
  fi

  log INFO "EC2: stopping instances: $ids"
  # shellcheck disable=SC2086
  run_cmd aws ec2 stop-instances --region "$AWS_REGION" --instance-ids ${ids}
}

ec2_start_lab_instances() {
  local ids
  ids=$(aws ec2 describe-instances \
    --region "$AWS_REGION" \
    --filters \
      "Name=instance-state-name,Values=stopped,stopping" \
      "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
    --query 'Reservations[].Instances[].InstanceId' \
    --output text 2>/dev/null || true)
  ids=$(echo "$ids" | tr '\t\n' ' ' | xargs)

  if [[ -z "$ids" || "$ids" == "None" ]]; then
    log INFO "EC2: no stopped lab instances found"
    return 0
  fi

  log INFO "EC2: starting instances: $ids"
  # shellcheck disable=SC2086
  run_cmd aws ec2 start-instances --region "$AWS_REGION" --instance-ids ${ids}
}

ec2_lab_status() {
  aws ec2 describe-instances \
    --region "$AWS_REGION" \
    --filters "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
    --query 'Reservations[].Instances[].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' \
    --output table 2>/dev/null || echo "EC2: none"
}
