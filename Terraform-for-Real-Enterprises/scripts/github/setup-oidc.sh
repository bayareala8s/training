#!/usr/bin/env bash
# Create GitHub Actions OIDC provider + github-terraform IAM role (Week 4 lab)
set -euo pipefail

GITHUB_ORG="${GITHUB_ORG:-bayareala8s}"
GITHUB_REPO="${GITHUB_REPO:-training}"
ROLE_NAME="${ROLE_NAME:-github-terraform}"
AWS_REGION="${AWS_REGION:-us-west-2}"
OIDC_URL="https://token.actions.githubusercontent.com"
OIDC_THUMBPRINT="${OIDC_THUMBPRINT:-6938fd4e38b475638f7a048c297b32b10e760584}"

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
OIDC_ARN="arn:aws:iam::${ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com"
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

log() { echo "[setup-oidc] $*"; }

create_oidc_provider() {
  if aws iam get-open-id-connect-provider --open-id-connect-provider-arn "$OIDC_ARN" >/dev/null 2>&1; then
    log "OIDC provider already exists: $OIDC_ARN"
  else
    log "Creating OIDC provider..."
    aws iam create-open-id-connect-provider \
      --url "$OIDC_URL" \
      --client-id-list sts.amazonaws.com \
      --thumbprint-list "$OIDC_THUMBPRINT"
    log "Created OIDC provider"
  fi
}

TRUST_POLICY=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "${OIDC_ARN}"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      },
      "StringLike": {
        "token.actions.githubusercontent.com:sub": "repo:${GITHUB_ORG}/${GITHUB_REPO}:*"
      }
    }
  }]
}
EOF
)

create_role() {
  if aws iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1; then
    log "Role already exists: $ROLE_NAME — updating trust policy"
    aws iam update-assume-role-policy --role-name "$ROLE_NAME" --policy-document "$TRUST_POLICY"
  else
    log "Creating role $ROLE_NAME..."
    aws iam create-role \
      --role-name "$ROLE_NAME" \
      --assume-role-policy-document "$TRUST_POLICY" \
      --description "GitHub Actions OIDC for Terraform CI (course lab)"
  fi
}

# Plan-only policy — sufficient for CI plan job; widen for apply in prod with care
PLAN_POLICY=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "s3:GetObject",
        "s3:ListBucket",
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:DeleteItem",
        "dynamodb:DescribeTable",
        "logs:DescribeLogGroups",
        "iam:GetRole",
        "iam:GetRolePolicy",
        "iam:ListRolePolicies"
      ],
      "Resource": "*"
    }
  ]
}
EOF
)

attach_plan_policy() {
  aws iam put-role-policy \
    --role-name "$ROLE_NAME" \
    --policy-name "${ROLE_NAME}-plan" \
    --policy-document "$PLAN_POLICY"
  log "Attached plan policy to role"
}

main() {
  aws sts get-caller-identity
  create_oidc_provider
  create_role
  attach_plan_policy

  echo ""
  echo "=============================================="
  echo " GitHub OIDC setup complete"
  echo "=============================================="
  echo "AWS_ROLE_ARN (add as GitHub repository secret):"
  echo "  $ROLE_ARN"
  echo ""
  echo "GitHub: Settings → Secrets → Actions → New secret"
  echo "  Name: AWS_ROLE_ARN"
  echo "  Value: $ROLE_ARN"
  echo ""
  echo "Then uncomment configure-aws-credentials in:"
  echo "  .github/workflows/terraform-ci.yml"
  echo "=============================================="
}

main "$@"
