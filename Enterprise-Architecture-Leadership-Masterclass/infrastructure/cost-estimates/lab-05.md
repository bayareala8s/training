# Cost Estimate — Lab 05 Cloud Platform Foundation

**Module:** 05 — Cloud and Platform Strategy  
**Case study:** NorthStar Financial Services (fictional)  
**Region assumed:** us-east-1  
**Target:** **~<$5** when cleaned up the same day

---

## Cost drivers (typical 2–4 hour lab)

| Service | Usage assumption | Approx. cost |
| ------- | ---------------- | ------------ |
| API Gateway HTTP API | <1,000 requests | <$0.01 |
| Lambda | <1,000 invocations, 128 MB | Free tier / pennies |
| DynamoDB on-demand | <1,000 WRU/RRU | <$0.01 |
| S3 | <100 MB, short-lived | <$0.01 |
| CloudTrail | Single-region management events, hours | Typically <$0.50–$1 for short labs* |
| CloudWatch Logs | 7-day retention, small volume | <$0.10 |
| SSM Parameter Store | Standard parameters | Free / negligible |
| AWS Budgets | 1 budget | Free (first 2 budgets) |
| IAM | — | Free |
| **AWS Config (optional)** | Recorder on | **$0.003/config item + delivery — avoid unless stretch** |

\*CloudTrail has free allotments for management events in many accounts; charges vary. Keep trail short-lived.

## What keeps cost low

- Serverless only (no NAT, EC2, EKS, OpenSearch)
- On-demand DynamoDB
- S3 lifecycle expiration (7 days)
- Log retention 7 days
- `enable_config = false` by default
- Same-day `terraform destroy` / `cleanup-lab05.sh`

## What inflates cost

| Anti-pattern | Impact |
| ------------ | ------ |
| Leaving CloudTrail + Config running for weeks | Continuous charges |
| Enabling AWS Config in production-like all-resources mode | Significant |
| Multi-region trail | Higher |
| Forgetting destroy overnight/weekend | Budget risk |

## FinOps teaching point

The **budget alert at $5** is part of the curriculum: platform strategy without cost guardrails is incomplete architecture.

## Cleanup verification

After destroy, confirm no residual resources tagged `Project=BayLearn` + `Module=05`.
