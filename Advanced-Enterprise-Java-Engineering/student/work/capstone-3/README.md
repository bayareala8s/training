# CAPSTONE-3 working tree

Paper + `terraform validate`. **No apply.**

- Modules: BUILD-1202 (`modules/ecr`, `modules/ecs_service`).
- ALB / Fargate 256/512 / public+IGW contract: `local.alb_contract` here; live HCL in `labs/BUILD-1101/work/` (also validate-only).
- IAM / secrets paper: `iam/` (teaching account `123456789012`). No `changeme`, no `AKIA`.
- Pipeline pin: BUILD-1204 `${{ github.sha }}` (or another immutable tag) becomes `var.container_image`. Never `:latest`.
- Refused apply: NAT Gateway, EKS, RDS Multi-AZ.

```bash
terraform init -backend=false
terraform validate
```
