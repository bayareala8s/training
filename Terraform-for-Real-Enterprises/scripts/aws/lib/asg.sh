#!/usr/bin/env bash

asg_set_lab_capacity() {
  local min="$1" max="$2" desired="$3"
  local asg_names
  asg_names=$(aws autoscaling describe-auto-scaling-groups --region "$AWS_REGION" \
    --query "AutoScalingGroups[?contains(Tags[?Key=='${LAB_TAG_KEY}'].Value | [0], '${LAB_TAG_VALUE}')].AutoScalingGroupName" \
    --output text 2>/dev/null || true)

  if [[ -z "$asg_names" || "$asg_names" == "None" ]]; then
    # Tag filter via describe tags
    asg_names=$(aws autoscaling describe-auto-scaling-groups --region "$AWS_REGION" \
      --query 'AutoScalingGroups[].AutoScalingGroupName' --output text 2>/dev/null || true)
    local filtered=""
    for name in $asg_names; do
      local tags
      tags=$(aws autoscaling describe-tags --region "$AWS_REGION" \
        --filters "Name=auto-scaling-group,Values=$name" "Name=key,Values=${LAB_TAG_KEY}" \
        --query 'Tags[?Value==`'"${LAB_TAG_VALUE}"'`].Value' --output text 2>/dev/null || true)
      [[ -n "$tags" ]] && filtered="$filtered $name"
    done
    asg_names=$filtered
  fi

  if [[ -z "$asg_names" ]]; then
    log INFO "ASG: no lab auto scaling groups found"
    return 0
  fi

  for name in $asg_names; do
    log INFO "ASG: $name -> min=$min max=$max desired=$desired"
    run_cmd aws autoscaling update-auto-scaling-group --region "$AWS_REGION" \
      --auto-scaling-group-name "$name" \
      --min-size "$min" --max-size "$max" --desired-capacity "$desired"
  done
}

asg_stop_lab() {
  asg_set_lab_capacity 0 0 0
}

asg_start_lab() {
  local desired="${ASG_LAB_DESIRED_COUNT:-1}"
  asg_set_lab_capacity 0 2 "$desired"
}
