# Lab 08 environment — AI Decision Assistant

NorthStar Financial Services (fictional) governed incident decision assistant.

## Deploy

```bash
cp terraform.tfvars.example terraform.tfvars
# Keep use_mock_bedrock = true unless Bedrock model access is enabled
terraform init
terraform plan
terraform apply
terraform output
terraform output -raw api_token
```

## Invoke

```bash
API=$(terraform output -raw api_endpoint)
TOKEN=$(terraform output -raw api_token)
curl -s -X POST "$API/decisions" \
  -H "content-type: application/json" \
  -H "x-lab-token: $TOKEN" \
  -d '{"incident_id":"INC-001","incident_text":"Payment authorization API p95 latency above 2s for 15 minutes in us-east-1"}'
```

## Bedrock enablement

See module README and `bedrock_enablement_notes` output. Mock mode is first-class for instruction.

## Cleanup

```bash
../../../scripts/cleanup-lab08.sh
```
