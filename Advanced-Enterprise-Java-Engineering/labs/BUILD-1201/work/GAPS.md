# BUILD-1201 — starter vs ACCOUNT.md (before edit)

| Gap | Starter |
|---|---|
| `terraform { required_providers { aws } }` | **Missing** |
| `variable "region"` default `us-west-2` | **Missing** (only `repository_name`) |
| Provider `region = var.region` | Hardcoded **`us-east-1`** |
| Tags Course/Module/Lab/Environment/Expiration | **Missing** |
| `aws_ecr_repository` `baypay/payment-service` | `ecr.tf` empty |
| Outputs `repository_url` / `repository_arn` | `outputs.tf` empty |
| No ALB/ECS/NAT/RDS/EKS | Correct — keep |
| No access keys / `BAYPAY_DB_*` | Correct — keep |

Fixes in `work/` only. Starter left incomplete.
