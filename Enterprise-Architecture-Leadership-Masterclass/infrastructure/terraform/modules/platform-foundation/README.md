# Platform Foundation — reusable Terraform module

**Course:** Enterprise Architecture Leadership Masterclass (BayLearn)  
**Lab:** Lab 05 — Cloud Platform Foundation  
**Case study:** NorthStar Financial Services (fictional)

## What this module provisions

| Resource | Purpose |
| -------- | ------- |
| S3 audit bucket | CloudTrail + lab audit artifacts; 7-day lifecycle |
| CloudTrail (optional) | Simple single-region management events |
| IAM role + policy | Least-privilege Lambda execution |
| DynamoDB | Platform registry / health heartbeats (on-demand) |
| Lambda | Platform health API |
| API Gateway HTTP API | `GET /health` |
| SSM Parameter Store | Platform config parameters |
| CloudWatch Logs | Lambda logs (7-day retention) |
| AWS Budgets | Cost alert (~$5 default) |
| AWS Config (optional) | **Cost warning** — off by default |

## Intentionally avoided

NAT Gateway, always-on EC2, EKS, OpenSearch, multi-region trails by default.

## Required tags

`Project=BayLearn`, `Course=EnterpriseArchitectureLeadership`, `Module=05`, `Environment=Lab`, plus `Student`.

## Usage

See `environments/lab05/`.
