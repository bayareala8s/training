#!/usr/bin/env bash
# Attach a custom domain (e.g. paks.bayareala8s.com) to the existing CloudFront stack.
# Mirrors the BayLearn pattern: subdomain on bayareala8s.com → CloudFront + ACM.
#
# Usage:
#   CUSTOM_DOMAIN=paks.bayareala8s.com \
#   HOSTED_ZONE_NAME=bayareala8s.com \
#   ./scripts/setup-custom-domain.sh
#
# Or with explicit zone ID:
#   CUSTOM_DOMAIN=paks.bayareala8s.com \
#   ROUTE53_HOSTED_ZONE_ID=Z0123456789ABC \
#   ./scripts/setup-custom-domain.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${DEPLOY_ENV:-$ROOT/deploy/aws.env}"
STACK_NAME="${AWS_STACK_NAME:-principal-architect-ks-prod}"
AWS_REGION="${AWS_REGION:-us-west-2}"
ACM_REGION="${ACM_REGION:-us-east-1}"
TEMPLATE="$ROOT/infrastructure/cloudfront-static-site.yaml"
PROJECT_NAME="${PROJECT_NAME:-principal-architect-ks}"
ENVIRONMENT="${ENVIRONMENT:-prod}"

CUSTOM_DOMAIN="${CUSTOM_DOMAIN:-}"
HOSTED_ZONE_NAME="${HOSTED_ZONE_NAME:-}"
ROUTE53_HOSTED_ZONE_ID="${ROUTE53_HOSTED_ZONE_ID:-}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

usage() {
  cat <<EOF
Usage: CUSTOM_DOMAIN=paks.bayareala8s.com HOSTED_ZONE_NAME=bayareala8s.com $0

Required:
  CUSTOM_DOMAIN          Full hostname (e.g. paks.bayareala8s.com, knowledge.bayareala8s.com)

Optional:
  HOSTED_ZONE_NAME       Parent zone (default: derived from CUSTOM_DOMAIN)
  ROUTE53_HOSTED_ZONE_ID Route 53 hosted zone ID (auto-looked up if omitted)
  ACM_CERTIFICATE_ARN    Existing ACM cert in us-east-1 (skip request if set)
  ACM_REGION             us-east-1 (required for CloudFront — do not change)

After success, run: make aws-deploy
EOF
  exit 1
}

[[ -n "$CUSTOM_DOMAIN" ]] || usage

if [[ -z "$HOSTED_ZONE_NAME" ]]; then
  HOSTED_ZONE_NAME="$(echo "$CUSTOM_DOMAIN" | awk -F. '{print $(NF-1)"."$NF}')"
fi

if [[ -z "$ROUTE53_HOSTED_ZONE_ID" ]]; then
  echo "==> Looking up hosted zone: $HOSTED_ZONE_NAME"
  ROUTE53_HOSTED_ZONE_ID="$(aws route53 list-hosted-zones-by-name \
    --dns-name "$HOSTED_ZONE_NAME" \
    --query "HostedZones[?Name=='${HOSTED_ZONE_NAME}.'].Id" \
    --output text | sed 's|/hostedzone/||')"
  if [[ -z "$ROUTE53_HOSTED_ZONE_ID" || "$ROUTE53_HOSTED_ZONE_ID" == "None" ]]; then
    echo "Error: Could not find Route 53 hosted zone for $HOSTED_ZONE_NAME" >&2
    echo "Create the zone or set ROUTE53_HOSTED_ZONE_ID manually." >&2
    exit 1
  fi
  echo "    Zone ID: $ROUTE53_HOSTED_ZONE_ID"
fi

# Warn if Route 53 zone is not authoritative (e.g. bayareala8s.com uses Wix DNS)
PUBLIC_NS="$(dig +short NS "$HOSTED_ZONE_NAME" 2>/dev/null | sort | tr '\n' ' ' || true)"
R53_NS="$(aws route53 get-hosted-zone --id "$ROUTE53_HOSTED_ZONE_ID" \
  --query 'DelegationSet.NameServers' --output text 2>/dev/null | tr '\t' '\n' | sort | tr '\n' ' ' || true)"
USE_MANUAL_DNS=false
if [[ -n "$PUBLIC_NS" && -n "$R53_NS" ]]; then
  if ! echo "$PUBLIC_NS" | grep -q "awsdns"; then
    echo ""
    echo "⚠️  DNS mismatch: $HOSTED_ZONE_NAME uses external nameservers (not Route 53)."
    echo "    Public NS: $PUBLIC_NS"
    echo "    You must add DNS records in Wix (or your DNS provider), not only Route 53."
    USE_MANUAL_DNS=true
    ROUTE53_HOSTED_ZONE_ID=""  # skip auto alias — record goes in Wix
  fi
fi

if [[ -z "${ACM_CERTIFICATE_ARN:-}" ]]; then
  echo "==> Requesting ACM certificate in $ACM_REGION for $CUSTOM_DOMAIN"
  ACM_CERTIFICATE_ARN="$(aws acm request-certificate \
    --domain-name "$CUSTOM_DOMAIN" \
    --validation-method DNS \
    --region "$ACM_REGION" \
    --query CertificateArn \
    --output text)"
  echo "    Certificate ARN: $ACM_CERTIFICATE_ARN"

  echo "==> Fetching DNS validation record"
  sleep 5
  VALIDATION_JSON="$(aws acm describe-certificate \
    --certificate-arn "$ACM_CERTIFICATE_ARN" \
    --region "$ACM_REGION" \
    --query 'Certificate.DomainValidationOptions[0].ResourceRecord' \
    --output json)"

  VAL_NAME="$(echo "$VALIDATION_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['Name'])")"
  VAL_VALUE="$(echo "$VALIDATION_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['Value'])")"

  if [[ "$USE_MANUAL_DNS" == "true" ]]; then
    echo ""
    echo "=========================================="
    echo "  MANUAL DNS REQUIRED (Wix / external DNS)"
    echo "=========================================="
    echo "Add this CNAME in your DNS provider (Wix → Domains → DNS):"
    echo ""
    echo "  Host:  ${VAL_NAME%.}"
    echo "  Type:  CNAME"
    echo "  Value: ${VAL_VALUE%.}"
    echo ""
    echo "Then re-run with:"
    echo "  ACM_CERTIFICATE_ARN=$ACM_CERTIFICATE_ARN \\"
    echo "  CUSTOM_DOMAIN=$CUSTOM_DOMAIN \\"
    echo "  ./scripts/setup-custom-domain.sh"
    echo "=========================================="
    echo ""
    if [[ -t 0 ]]; then
      read -r -p "Press Enter after adding the CNAME in Wix (or Ctrl+C to exit)..."
    else
      echo "Re-run this script after adding the CNAME (non-interactive mode)."
      exit 0
    fi
  else
    echo "==> Creating ACM validation CNAME in Route 53"
    aws route53 change-resource-record-sets \
      --hosted-zone-id "$ROUTE53_HOSTED_ZONE_ID" \
      --change-batch "$(cat <<EOF
{
  "Changes": [{
    "Action": "UPSERT",
    "ResourceRecordSet": {
      "Name": "$VAL_NAME",
      "Type": "CNAME",
      "TTL": 300,
      "ResourceRecords": [{"Value": "$VAL_VALUE"}]
    }
  }]
}
EOF
)"
  fi

  echo "==> Waiting for certificate validation (may take 5–30 minutes)..."
  aws acm wait certificate-validated \
    --certificate-arn "$ACM_CERTIFICATE_ARN" \
    --region "$ACM_REGION"
  echo "    Certificate issued."
else
  echo "==> Using existing ACM certificate: $ACM_CERTIFICATE_ARN"
fi

echo "==> Updating CloudFormation stack with custom domain"
aws cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file "$TEMPLATE" \
  --parameter-overrides \
    "ProjectName=$PROJECT_NAME" \
    "Environment=$ENVIRONMENT" \
    "CustomDomainName=$CUSTOM_DOMAIN" \
    "AcmCertificateArn=$ACM_CERTIFICATE_ARN" \
    "Route53HostedZoneId=$ROUTE53_HOSTED_ZONE_ID" \
  --capabilities CAPABILITY_IAM \
  --region "$AWS_REGION" \
  --no-fail-on-empty-changeset

echo "==> Waiting for CloudFront distribution update (may take 10–20 minutes)..."
aws cloudformation wait stack-update-complete \
  --stack-name "$STACK_NAME" \
  --region "$AWS_REGION" 2>/dev/null \
  || aws cloudformation wait stack-create-complete \
    --stack-name "$STACK_NAME" \
    --region "$AWS_REGION"

get_output() {
  aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$AWS_REGION" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" \
    --output text
}

S3_BUCKET="$(get_output BucketName)"
CLOUDFRONT_DISTRIBUTION_ID="$(get_output DistributionId)"
SITE_URL="$(get_output WebsiteURL)"
CLOUDFRONT_URL="$(get_output CloudFrontURL)"

mkdir -p "$ROOT/deploy"
cat > "$ENV_FILE" <<EOF
# Auto-generated — do not commit
AWS_REGION=$AWS_REGION
AWS_STACK_NAME=$STACK_NAME
S3_BUCKET=$S3_BUCKET
CLOUDFRONT_DISTRIBUTION_ID=$CLOUDFRONT_DISTRIBUTION_ID
SITE_URL=$SITE_URL
CLOUDFRONT_URL=$CLOUDFRONT_URL
CUSTOM_DOMAIN=$CUSTOM_DOMAIN
ACM_CERTIFICATE_ARN=$ACM_CERTIFICATE_ARN
ROUTE53_HOSTED_ZONE_ID=$ROUTE53_HOSTED_ZONE_ID
EOF

echo ""
echo "=========================================="
echo "  Custom domain ready"
echo "=========================================="
echo "  Portal URL:     $SITE_URL"
echo "  CloudFront URL: $CLOUDFRONT_URL (still works)"
echo "  Config:         deploy/aws.env"
echo ""
if [[ "$USE_MANUAL_DNS" == "true" || -z "${ROUTE53_HOSTED_ZONE_ID:-}" ]]; then
  CF_DOMAIN="$(aws cloudfront get-distribution --id "$CLOUDFRONT_DISTRIBUTION_ID" \
    --query 'Distribution.DomainName' --output text 2>/dev/null || echo '<distribution>.cloudfront.net')"
  echo "  Wix DNS — add CNAME:"
  echo "    Host:  $CUSTOM_DOMAIN"
  echo "    Type:  CNAME"
  echo "    Value: $CF_DOMAIN"
  echo ""
fi
echo "Next: make aws-deploy"
echo "Share $SITE_URL with students (BayLearn-style branded URL)."
echo "=========================================="
