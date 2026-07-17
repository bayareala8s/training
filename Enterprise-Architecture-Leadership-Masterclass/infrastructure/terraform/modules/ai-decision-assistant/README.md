# Terraform module: ai-decision-assistant (BayLearn Module 08)

Governed incident decision assistant for NorthStar Financial Services (fictional).

## Components

- HTTP API (`POST /decisions`) protected by `x-lab-token`
- Step Functions orchestration
- Infer Lambda (Amazon Bedrock **or** mock classifier)
- Validate/route Lambda (schema + deterministic HITL rules)
- DynamoDB decisions table
- S3 artifacts + safe logs
- CloudWatch token/cost metrics
- Optional Bedrock Guardrails

## Mock vs live Bedrock

| Mode | `use_mock_bedrock` | Behavior |
| ---- | ------------------ | -------- |
| Mock (default) | `true` | Deterministic classifier; no model access required |
| Live | `false` | Calls Bedrock `converse` with `bedrock_model_id` |

### Enable Bedrock in your account

1. Open Amazon Bedrock in the lab region
2. Request/enable access for the configured model (default `amazon.nova-micro-v1:0`)
3. Wait until access is granted
4. Set `use_mock_bedrock = false` and `terraform apply`

If access cannot be granted, **keep mock mode**—architecture, HITL, validation, and evaluation learning still apply.

## Cost warning

Destroy after class. Live Bedrock charges by token. See `infrastructure/cost-estimates/lab-08.md`.
