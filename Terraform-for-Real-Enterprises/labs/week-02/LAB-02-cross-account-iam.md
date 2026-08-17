# Lab 2.2 — Cross-Account IAM Roles

**Duration:** 2–3 hours · **Week 2**

## Objectives

- Create trust policy for Terraform runner role
- Scope permissions with least privilege
- Configure provider `assume_role` (or document for CI)

## Steps

### 1. Review templates

Open [iam/terraform-runner-trust.json](iam/terraform-runner-trust.json) and [iam/terraform-runner-policy.json](iam/terraform-runner-policy.json).

### 2. Create role in workload account (or same account for lab)

**Trust policy** — allow tooling account root or GitHub OIDC role:

```bash
aws iam create-role \
  --role-name bal8s-terraform-runner \
  --assume-role-policy-document file://iam/terraform-runner-trust.json
```

Update `terraform-runner-trust.json` with your tooling account ID or OIDC provider ARN.

### 3. Attach scoped policy

```bash
aws iam put-role-policy \
  --role-name bal8s-terraform-runner \
  --policy-name bal8s-terraform-lab \
  --policy-document file://iam/terraform-runner-policy.json
```

### 4. Test assume role

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::WORKLOAD_ACCOUNT:role/bal8s-terraform-runner \
  --role-session-name lab-test
```

### 5. Optional: provider alias

Add to `labs/shared/environments/dev/main.tf`:

```hcl
provider "aws" {
  alias  = "workload"
  region = var.aws_region
  assume_role {
    role_arn = var.terraform_role_arn
  }
}
```

## Deliverable

- IAM role created (or documented if org admin required)
- Successful `sts assume-role` output (redacted)

## Next

[Lab 2.3 — Cross-Account Apply](LAB-03-cross-account-apply.md)
