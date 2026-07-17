# Integration Platform — reusable Terraform module

**Course:** Enterprise Architecture Leadership Masterclass (BayLearn)  
**Lab:** Lab 06 — Integration Reference Architecture  
**Case study:** NorthStar Financial Services (fictional)

## Patterns demonstrated

| Pattern | AWS implementation |
| ------- | ------------------ |
| Real-time account APIs | API Gateway HTTP API → Lambda → DynamoDB + EventBridge |
| Payment events | EventBridge → SQS (+ DLQ) → Lambda |
| Partner SFTP files | **S3 simulation** (not Transfer Family — cost control) |
| Regulatory batches | Step Functions → analytics Lambda → SNS |
| Notifications | SNS email |

## Intentionally avoided / optional

- **AWS Transfer Family:** conceptual only in lab docs; continuous endpoints cost money. Use S3 `incoming/` uploads to simulate partner file arrival.
- NAT Gateway, always-on EC2, EKS, OpenSearch.

## Tags

`Project=BayLearn`, `Course=EnterpriseArchitectureLeadership`, `Module=06`, `Environment=Lab`.
