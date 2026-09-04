# Rubric — BUILD-1201 Terraform AWS environment

**Type:** BUILD  
**awsLab:** yes  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. `terraform apply` absence must not fail the lab. A root left on `us-east-1` without `required_providers` is not a high Technical score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `required_providers.aws`; `variable "region"` default `us-west-2`; provider uses `var.region`; ECR `baypay/payment-service`; URL/ARN outputs; `terraform validate` | ECR present; region still hardcoded or tags missing | Starter unchanged or validate fails |
| Diagnostic method | 20% | Listed starter gaps (`us-east-1`, no providers, empty `ecr.tf`) before editing | Edited until it “looked like” a blog root | Opened `solutions/` first |
| Production awareness | 15% | ACCOUNT.md tags; immutable tags or scan-on-push; refused ALB/ECS/NAT | Repository works on paper; no tags | Added ALB/NAT “for realism” |
| Trade-off analysis | 15% | Skeleton vs full ECS; validate vs apply; local state vs backend | States a preference with little why | No trade-off |
| Security / reliability | 10% | No keys; no `BAYPAY_DB_*`; least-privilege ECR named | Keys absent; mutability ignored | Access key or `changeme` in `.tf` |
| Communication | 10% | Checklist complete; PF-iac root section readable | Incomplete excerpt | Empty worksheet |
| Efficiency | 5% | Validate only; no required apply | Finished in session | Applied ALB/EKS or left resources running |

**Pass guideline:** weighted score ≥ 70, `terraform validate` green on the student copy, region contract held, no secrets. Optional apply neither raises nor lowers the score if destroyed.
