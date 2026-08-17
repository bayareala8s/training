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

nat_gateway_status() {
  local count
  count=$(aws ec2 describe-nat-gateways --region "$AWS_REGION" \
    --filter "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
             "Name=state,Values=available,pending,deleting" \
    --query 'length(NatGateways)' --output text 2>/dev/null || echo "0")

  if [[ "$count" == "0" || "$count" == "None" ]]; then
    echo "NAT Gateway: none (no hourly NAT GW charge)"
    return 0
  fi

  aws ec2 describe-nat-gateways --region "$AWS_REGION" \
    --filter "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
             "Name=state,Values=available,pending,deleting" \
    --query 'NatGateways[].[NatGatewayId,State,Tags[?Key==`Environment`].Value|[0],Tags[?Key==`Name`].Value|[0]]' \
    --output table 2>/dev/null || echo "NAT Gateway: query failed"
}

nat_gateway_hourly_cost_warning() {
  local count
  count=$(aws ec2 describe-nat-gateways --region "$AWS_REGION" \
    --filter "Name=tag:${LAB_TAG_KEY},Values=${LAB_TAG_VALUE}" \
             "Name=state,Values=available,pending" \
    --query 'length(NatGateways)' --output text 2>/dev/null || echo "0")
  if [[ "$count" != "0" && "$count" != "None" ]]; then
    echo "WARNING: $count NAT Gateway(s) billing ~\$0.045/hr each. Run pause-labs.sh to remove."
  fi
}
