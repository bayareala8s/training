#!/usr/bin/env bash
# Lab 7.1 — Apply KMS default encryption to data lake bucket
set -euo pipefail

BUCKET="${BUCKET:?Set BUCKET}"
KMS_ALIAS="${KMS_ALIAS:-alias/cnde-dev-datalake-key}"
REGION="${AWS_REGION:-us-east-1}"

echo "Creating KMS key if not exists..."
KEY_ID=$(aws kms describe-key --key-id "$KMS_ALIAS" --query 'KeyMetadata.KeyId' --output text 2>/dev/null || true)
if [ -z "$KEY_ID" ] || [ "$KEY_ID" = "None" ]; then
  KEY_ID=$(aws kms create-key \
    --description "CNDE Module 7 data lake encryption key" \
    --query 'KeyMetadata.KeyId' --output text)
  aws kms create-alias --alias-name "$KMS_ALIAS" --target-key-id "$KEY_ID"
  echo "Created key $KEY_ID with alias $KMS_ALIAS"
fi

KMS_ARN=$(aws kms describe-key --key-id "$KMS_ALIAS" --query 'KeyMetadata.Arn' --output text)

TMP=$(mktemp)
sed "s|alias/cnde-dev-datalake-key|${KMS_ARN}|g" policies/bucket-encryption.json > "$TMP"

aws s3api put-bucket-encryption \
  --bucket "$BUCKET" \
  --server-side-encryption-configuration "file://${TMP}"

rm -f "$TMP"
echo "Default encryption applied to s3://${BUCKET} with ${KMS_ARN}"

echo "Verify:"
aws s3api get-bucket-encryption --bucket "$BUCKET"
