# Lab 07 environment — Security & Resilience

NorthStar Financial Services (fictional) settlement landing-zone lab.

## Deploy

```bash
cp terraform.tfvars.example terraform.tfvars
# edit student_id, expiration_date, optional alert_email / enable_replication
terraform init
terraform plan
terraform apply
```

## Cost warning

Default configuration (no CRR) is low cost. Set `enable_replication = true` only with a same-day cleanup plan. See `infrastructure/cost-estimates/lab-07.md`.

## Cleanup

```bash
../../../scripts/cleanup-lab07.sh
# or: terraform destroy
```
