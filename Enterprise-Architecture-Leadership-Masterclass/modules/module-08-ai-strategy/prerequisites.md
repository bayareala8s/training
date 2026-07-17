# Prerequisites — Module 08

## Required prior learning

| Prerequisite | Why |
| ------------ | --- |
| Module 07 security/resilience | AI systems inherit trust boundaries, logging, and evidence needs |
| Module 05–06 cloud/integration | Serverless orchestration patterns |
| Templates 12 and 19 | Scorecard and AI governance checklist |

## Technical prerequisites

| Tool | Minimum |
| ---- | ------- |
| AWS account | Lambda, API Gateway, Step Functions, DynamoDB, S3, CloudWatch; Bedrock optional |
| Terraform | 1.5+ |
| AWS CLI | v2.x |
| Bedrock model access | Optional — enable Amazon Bedrock model access in console if using live mode |
| Python | 3.11+ helpful for local eval scoring scripts (optional) |

## Bedrock enablement (when using live mode)

1. Open Amazon Bedrock console in your lab region (recommended `us-east-1`)
2. Request/enable access to the model configured in Terraform (default: Amazon Nova Micro or Anthropic Claude Haiku-class model ID set in tfvars)
3. Wait until status is Access granted
4. Set `use_mock_bedrock = false` in `terraform.tfvars`
5. If access cannot be granted in class time, keep **mock mode** (`use_mock_bedrock = true`)—architecture learning still counts

## Cost and safety

- Budget alert recommended ($10–$25 week)
- No production incident text containing real customer PII
- Cleanup: `infrastructure/terraform/scripts/cleanup-lab08.sh`
