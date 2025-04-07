Here's a **GitHub-friendly `README.md`** version of your **AWS Lambda S3 Bucket & Prefix Update Deployment Runbook**, formatted in markdown and ready to drop into your repo:

```markdown
# AWS Production Deployment Runbook  
**Update Target S3 Bucket Names and Prefixes for Python AWS Lambda Functions**

---

## Overview

This runbook describes the process for updating **S3 bucket names and prefixes** used by two AWS Lambda functions in the **Production** environment:

- `product_lambda`
- `signal_lambda`

---

## Scope of Change

| Lambda Function   | Current S3 Bucket         | Current Prefix           | New S3 Bucket              | New Prefix                     |
|-------------------|---------------------------|---------------------------|-----------------------------|--------------------------------|
| `product_lambda`  | `prod-bucket-001`         | `products/raw/`           | `prod-data-main`            | `products/incoming/`           |
| `signal_lambda`   | `prod-bucket-002`         | `signals/input/`          | `prod-signals-updated`      | `signals/incoming/2025/`       |

---

## 1. Pre-Deployment Checklist

- [ ] Change Request (CR) approved
- [ ] Confirm new buckets and prefixes exist
- [ ] Verify Lambda IAM roles have access to new paths
- [ ] Identify if S3 paths are set via env vars, IaC, or hardcoded
- [ ] Backup current function config and/or source code

---

## 2. Backup (Optional)

```bash
aws lambda get-function-configuration --function-name product_lambda > product_lambda_backup.json
aws lambda get-function-configuration --function-name signal_lambda > signal_lambda_backup.json
```

---

## 3. Deployment Options

### Option A: Update Environment Variables

```bash
aws lambda update-function-configuration \
  --function-name product_lambda \
  --environment "Variables={TARGET_BUCKET=prod-data-main,TARGET_PREFIX=products/incoming/}"

aws lambda update-function-configuration \
  --function-name signal_lambda \
  --environment "Variables={TARGET_BUCKET=prod-signals-updated,TARGET_PREFIX=signals/incoming/2025/}"
```

---

### Option B: Update Hardcoded Code and Deploy

Update Lambda source code:
```python
TARGET_BUCKET = os.getenv("TARGET_BUCKET", "prod-data-main")
TARGET_PREFIX = os.getenv("TARGET_PREFIX", "products/incoming/")
```

Package and deploy:
```bash
zip function.zip lambda_function.py
aws lambda update-function-code \
  --function-name product_lambda \
  --zip-file fileb://function.zip
```

---

### Option C: Use Terraform

Update your variables:
```hcl
module "product_lambda" {
  function_name  = "product_lambda"
  s3_bucket_name = "prod-data-main"
  s3_prefix_path = "products/incoming/"
}

module "signal_lambda" {
  function_name  = "signal_lambda"
  s3_bucket_name = "prod-signals-updated"
  s3_prefix_path = "signals/incoming/2025/"
}
```

Run Terraform:
```bash
terraform init
terraform plan
terraform apply
```

---

## 4. Post-Deployment Validation

- [ ] Run test event for each Lambda
- [ ] Check logs in CloudWatch
- [ ] Validate correct data access/output
- [ ] Notify stakeholders

---

## 5. Rollback Plan

### Environment Variable Rollback:
```bash
aws lambda update-function-configuration \
  --function-name product_lambda \
  --environment "Variables={TARGET_BUCKET=prod-bucket-001,TARGET_PREFIX=products/raw/}"
```

### Terraform Rollback:
```bash
git checkout previous.tf
terraform apply
```

---

## 6. Audit & Tagging

```bash
aws lambda publish-version --function-name product_lambda
aws lambda tag-resource \
  --resource arn:aws:lambda:<region>:<account-id>:function:product_lambda:<version> \
  --tags changeID=CR123456 changedBy=himanshu
```

---

## 7. Monitoring & Alerting

- CloudWatch alarms
- S3 event notifications (optional)
- Log subscriptions or alerting systems

---

## Contacts

| Role            | Name/Team        | Contact Info           |
|------------------|------------------|--------------------------|
| Change Owner     | Himanshu         | himanshu@company.com     |
| DevOps Lead      | DevOps Team      | devops@company.com       |
| Product Manager  | Product Team     | product@company.com      |
```

