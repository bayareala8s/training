# Lab 05 Environment — Platform Foundation

**Module:** 05 — Cloud and Platform Strategy  
**Case study:** NorthStar Financial Services (fictional)  
**Cost target:** ~<$5 when cleaned up promptly

## Prerequisites

- AWS account with permissions for IAM, S3, CloudTrail, DynamoDB, Lambda, API Gateway, SSM, Budgets, CloudWatch Logs
- Terraform >= 1.5
- AWS CLI configured (`aws sts get-caller-identity` succeeds)

## Deploy

```bash
cd infrastructure/terraform/environments/lab05
cp terraform.tfvars.example terraform.tfvars
# Edit student_id, budget_notification_email, expiration_date

terraform init
terraform plan
terraform apply
```

## Validate

```bash
curl "$(terraform output -raw api_health_url)"
aws dynamodb scan --table-name "$(terraform output -raw dynamodb_table_name)" --max-items 3
aws ssm get-parameters-by-path --path "$(terraform output -raw ssm_parameter_prefix)" --recursive
```

## Cleanup

```bash
../../../scripts/cleanup-lab05.sh
# or: terraform destroy -auto-approve
```

## Security notes

- Do not use production data
- Public `GET /health` is intentional for the lab; do not attach write routes without auth
- Destroy resources the same day; confirm budget alerts

## Optional AWS Config

Set `enable_config = true` only for stretch work. Config incurs ongoing charges — destroy promptly.
