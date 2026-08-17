#!/usr/bin/env bash
# Stop/start NAT Gateway is NOT supported (must destroy/recreate).
# This script finds EC2-based NAT instances (common in lab VPC modules).

nat_instance_stop() {
  aws ec2 describe-instances --region "$AWS_REGION" \
    --filters \
      "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
      "Name=tag:Role,Values=nat-instance" \
      "Name=instance-state-name,Values=running" \
    --query 'Reservations[].Instances[].InstanceId' --output text | \
  while read -r id; do
    [[ -n "$id" && "$id" != "None" ]] || continue
    log INFO "NAT instance: stopping $id"
    run_cmd aws ec2 stop-instances --region "$AWS_REGION" --instance-ids "$id"
  done
}

nat_instance_start() {
  aws ec2 describe-instances --region "$AWS_REGION" \
    --filters \
      "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
      "Name=tag:Role,Values=nat-instance" \
      "Name=instance-state-name,Values=stopped" \
    --query 'Reservations[].Instances[].InstanceId' --output text | \
  while read -r id; do
    [[ -n "$id" && "$id" != "None" ]] || continue
    log INFO "NAT instance: starting $id"
    run_cmd aws ec2 start-instances --region "$AWS_REGION" --instance-ids "$id"
  done
}
