# Lab 08 — Build NorthStar’s Governed AI Decision Assistant

**Module:** 08 — AI Strategy and Intelligent Enterprise Architecture  
**AWS lab:** Yes (Bedrock optional via mock fallback)  
**Estimated duration:** 90–120 minutes  
**Estimated cost:** Typically **under $5 USD** same-day; Bedrock tokens vary by model/volume  
**Recommended region:** `us-east-1`  
**Case study:** NorthStar Financial Services (fictional)

> **Fiction notice:** Use only synthetic incident text. Never paste real customer data.

## Cost and safety

- Serverless only — no NAT, always-on EC2, EKS, OpenSearch
- Tag all resources with BayLearn tags
- Budget alert before deploy
- Prefer `use_mock_bedrock = true` until Bedrock access is confirmed
- Cleanup: `infrastructure/terraform/scripts/cleanup-lab08.sh`

## Quick links

| Asset | Path |
| ----- | ---- |
| Student instructions | [`student-instructions.md`](student-instructions.md) |
| Dataset | [`datasets/incident-eval-set.csv`](datasets/incident-eval-set.csv) |
| Terraform | `infrastructure/terraform/environments/lab08/` |
| Cost estimate | `infrastructure/cost-estimates/lab-08.md` |

## Architecture summary

API Gateway → Step Functions → Lambda (infer) → validate/rules Lambda → DynamoDB; S3 for artifacts; CloudWatch for metrics. Inference is Amazon Bedrock **or** deterministic mock.
