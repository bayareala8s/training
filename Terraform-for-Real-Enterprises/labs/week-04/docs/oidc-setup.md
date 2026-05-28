# GitHub OIDC for Terraform (Week 4)

## 1. Create OIDC provider in AWS IAM

Provider URL: `https://token.actions.githubusercontent.com`  
Audience: `sts.amazonaws.com`

## 2. Trust policy for `github-terraform` role

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      },
      "StringLike": {
        "token.actions.githubusercontent.com:sub": "repo:bayareala8s/training:*"
      }
    }
  }]
}
```

## 3. GitHub secret

Add repository secret: `AWS_ROLE_ARN` = role ARN.

## 4. Workflow

Uncomment `configure-aws-credentials` in `terraform-ci.yml`.
