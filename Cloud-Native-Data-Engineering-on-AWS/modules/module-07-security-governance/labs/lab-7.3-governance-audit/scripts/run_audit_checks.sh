#!/usr/bin/env bash
# Lab 7.3 — Automated governance pre-checks (evidence collection)
set -euo pipefail

BUCKET="${BUCKET:?Set BUCKET}"
REPORT_DIR="${REPORT_DIR:-./audit-evidence}"
mkdir -p "$REPORT_DIR"

echo "=== S3 Public Access Block ===" | tee "$REPORT_DIR/s3-public-access.txt"
aws s3api get-public-access-block --bucket "$BUCKET" 2>&1 | tee -a "$REPORT_DIR/s3-public-access.txt" || true

echo "=== Bucket Encryption ===" | tee "$REPORT_DIR/s3-encryption.txt"
aws s3api get-bucket-encryption --bucket "$BUCKET" 2>&1 | tee -a "$REPORT_DIR/s3-encryption.txt" || true

echo "=== IAM Roles (CNDE dev) ===" | tee "$REPORT_DIR/iam-roles.txt"
for ROLE in cnde-dev-analyst-curated cnde-dev-engineer-pipeline cnde-dev-steward-quarantine; do
  echo "--- $ROLE ---" >> "$REPORT_DIR/iam-roles.txt"
  aws iam get-role --role-name "$ROLE" --query 'Role.{Name:RoleName,Arn:Arn,Created:CreateDate}' 2>&1 >> "$REPORT_DIR/iam-roles.txt" || echo "Role not found: $ROLE" >> "$REPORT_DIR/iam-roles.txt"
done

echo "=== CloudTrail Trails ===" | tee "$REPORT_DIR/cloudtrail.txt"
aws cloudtrail describe-trails --query 'trailList[*].{Name:Name,S3:S3BucketName,Multi:IsMultiRegionTrail,LogValidation:LogFileValidationEnabled}' \
  --output table 2>&1 | tee -a "$REPORT_DIR/cloudtrail.txt" || true

echo "Evidence written to $REPORT_DIR/"
echo "Complete templates/audit-report-template.md using these files."
