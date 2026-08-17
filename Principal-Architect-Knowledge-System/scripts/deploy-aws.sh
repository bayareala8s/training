#!/usr/bin/env bash
# Build the site and sync to S3 + invalidate CloudFront cache.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${DEPLOY_ENV:-$ROOT/deploy/aws.env}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

: "${S3_BUCKET:?Set S3_BUCKET in deploy/aws.env (run: make aws-setup)}"
: "${CLOUDFRONT_DISTRIBUTION_ID:?Set CLOUDFRONT_DISTRIBUTION_ID in deploy/aws.env}"
: "${SITE_URL:?Set SITE_URL in deploy/aws.env}"

AWS_REGION="${AWS_REGION:-us-west-2}"

if ! command -v aws >/dev/null 2>&1; then
  echo "Error: AWS CLI is required." >&2
  exit 1
fi

echo "==> Building site for $SITE_URL"
cd "$ROOT"
export SITE_URL
npm run build:aws

echo "==> Syncing build/ to s3://$S3_BUCKET"
aws s3 sync "$ROOT/build/" "s3://$S3_BUCKET/" \
  --delete \
  --region "$AWS_REGION" \
  --cache-control "public,max-age=31536000,immutable" \
  --exclude "index.html" \
  --exclude "docs/**/index.html" \
  --exclude "404.html"

# HTML entry points: short cache so updates propagate quickly
aws s3 sync "$ROOT/build/" "s3://$S3_BUCKET/" \
  --region "$AWS_REGION" \
  --exclude "*" \
  --include "index.html" \
  --include "docs/**/index.html" \
  --include "404.html" \
  --cache-control "public,max-age=300,must-revalidate"

echo "==> Invalidating CloudFront cache"
INVALIDATION_ID="$(aws cloudfront create-invalidation \
  --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" \
  --paths "/*" \
  --query 'Invalidation.Id' \
  --output text)"

echo ""
echo "=========================================="
echo "  Deploy complete"
echo "=========================================="
echo "  Portal URL:      $SITE_URL"
echo "  Invalidation:    $INVALIDATION_ID"
echo "  (allow 1–2 min for cache to clear)"
echo "=========================================="
