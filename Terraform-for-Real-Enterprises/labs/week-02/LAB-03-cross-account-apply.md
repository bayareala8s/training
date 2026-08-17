# Lab 2.3 — Cross-Account Terraform Apply

**Duration:** 2 hours · **Week 2**

## Objectives

- Run `terraform plan` using assumed role credentials
- Document session naming and external ID pattern

## Steps

### 1. Export assumed credentials

```bash
CREDS=$(aws sts assume-role \
  --role-arn arn:aws:iam::ACCOUNT_ID:role/bal8s-terraform-runner \
  --role-session-name tf-lab \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text)

export AWS_ACCESS_KEY_ID=$(echo $CREDS | awk '{print $1}')
export AWS_SECRET_ACCESS_KEY=$(echo $CREDS | awk '{print $2}')
export AWS_SESSION_TOKEN=$(echo $CREDS | awk '{print $3}')
```

### 2. Plan dev environment

```bash
make plan ENV=dev
```

### 3. Document workflow

Add section to your fork README:

- Who can assume the role
- External ID (if used)
- How CI will replace manual export (Week 4)

## Deliverable

PR section: cross-account workflow documented with diagram update.

## Next

[Week 3 — Modules](../week-03/LAB-01-vpc-module.md)
