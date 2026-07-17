# Lab 06 Environment — Integration Platform

**Module:** 06 — Integration, Application, and Data Architecture  
**Case study:** NorthStar Financial Services (fictional)  
**Cost target:** ~<$5 when cleaned up promptly

## Prerequisites

- AWS permissions for API Gateway, Lambda, EventBridge, SQS, Step Functions, S3, DynamoDB, SNS, IAM, CloudWatch Logs
- Terraform >= 1.5
- AWS CLI configured

## Deploy

```bash
cd infrastructure/terraform/environments/lab06
cp terraform.tfvars.example terraform.tfvars
# Edit student_id, notification_email, expiration_date

terraform init
terraform plan
terraform apply
```

Confirm the SNS email subscription before expecting notifications.

## Validate (quick)

```bash
# Create account
curl -s -X POST "$(terraform output -raw create_account_url)" \
  -H 'content-type: application/json' \
  -d '{"customer_name":"Ada Lovelace","status":"ACTIVE"}'

# Publish payment event
aws events put-events --entries "[{
  \"Source\": \"northstar.payments\",
  \"DetailType\": \"PaymentSubmitted\",
  \"EventBusName\": \"$(terraform output -raw event_bus_name)\",
  \"Detail\": \"{\\\"payment_id\\\":\\\"pay-1\\\",\\\"account_id\\\":\\\"acc-1\\\",\\\"amount\\\":100.50}\"
}]"

# Simulate partner SFTP file
echo "partner,txn,100" | aws s3 cp - "s3://$(terraform output -raw partner_bucket_name)/incoming/file1.csv"

# Regulatory batch
aws stepfunctions start-execution \
  --state-machine-arn "$(terraform output -raw state_machine_arn)" \
  --input '{"batch_id":"reg-001","source":"lab"}'
```

## Transfer Family note

AWS Transfer Family is **conceptual / optional only**. Continuous SFTP endpoints incur cost. This lab uses S3 uploads to simulate partner file arrival.

## Cleanup

```bash
../../../scripts/cleanup-lab06.sh
```
