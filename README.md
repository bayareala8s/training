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
