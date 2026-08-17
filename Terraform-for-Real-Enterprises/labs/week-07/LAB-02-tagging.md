# Lab 7.2 — Tagging Policies

**Duration:** 1–2 hours · **Week 7**

## Objectives

- Enforce required tags via variables and validation blocks
- Align with start/stop script tags

## Steps

### 1. Required tags (course standard)

```hcl
Course      = "terraform-enterprise"
Project     = "bayareala8s-tf-course"
ManagedBy   = "terraform"
Environment = var.environment
Owner       = var.owner
```

### 2. Add variable validation

In environment `variables.tf`:

```hcl
variable "owner" {
  type = string
  validation {
    condition     = length(var.owner) > 0
    error_message = "Owner tag required for cost allocation."
  }
}
```

### 3. Verify tags in AWS

```bash
aws ec2 describe-instances --filters "Name=tag:Course,Values=terraform-enterprise" \
  --query 'Reservations[].Instances[].Tags' --output table
```

## Deliverable

All lab resources show required tags in console.

## Next

[Lab 7.3 — Compliance checks](LAB-03-compliance.md)
