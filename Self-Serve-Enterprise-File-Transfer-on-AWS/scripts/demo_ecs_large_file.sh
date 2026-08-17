#!/usr/bin/env bash
# Lab 9 demo: generate a large file, upload to large/inbound/, wait for Fargate processing.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

baylearn_require_tools
export AWS_REGION="$(baylearn_aws_region)"

BUCKET="$(baylearn_tf_raw landing_bucket)"
IN_PREFIX="$(baylearn_tf_raw large_file_inbound_prefix)"
PROC_PREFIX="$(baylearn_tf_raw large_file_processed_prefix)"
LOG_GROUP="$(baylearn_tf_raw ecs_worker_log_group)"
SIZE_MB="${LAB_LARGE_FILE_MB:-50}"

if [[ -z "$BUCKET" ]]; then
  echo "Stack not deployed. Run ./scripts/start_stack.sh --yes" >&2
  exit 1
fi

KEY_NAME="demo-large-$(date +%s).bin"
LOCAL="/tmp/${KEY_NAME}"
S3_KEY="${IN_PREFIX}${KEY_NAME}"

echo "==> Generating ${SIZE_MB}MB test file at ${LOCAL}"
dd if=/dev/urandom of="$LOCAL" bs=1m count="$SIZE_MB" 2>/dev/null

echo "==> Upload s3://${BUCKET}/${S3_KEY}"
aws s3 cp "$LOCAL" "s3://${BUCKET}/${S3_KEY}"

echo "==> Waiting for ECS worker (up to 10 min)..."
DEST="${PROC_PREFIX}${KEY_NAME}"
MANIFEST="${DEST}.manifest.json"
for i in $(seq 1 60); do
  if aws s3api head-object --bucket "$BUCKET" --key "$MANIFEST" 2>/dev/null; then
    echo "PASS: manifest found"
    aws s3 cp "s3://${BUCKET}/${MANIFEST}" - 
    rm -f "$LOCAL"
    exit 0
  fi
  sleep 10
done

echo "WARN: manifest not found yet. Check logs:"
echo "  aws logs tail ${LOG_GROUP} --since 15m --follow"
rm -f "$LOCAL"
exit 1
