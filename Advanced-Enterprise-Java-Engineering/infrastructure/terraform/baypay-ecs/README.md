# baypay-ecs — healthy Terraform skeleton

Course-level example for Modules 11–12. This root is **provider + variables + one ECR repository**. It is not a live Fargate/ALB stack.

## Contracts

- `terraform { required_providers { aws } }`
- `variable "region" { default = "us-west-2" }`
- Tags: `Course=AEJE`, `Module`, `Lab`, `Environment=student`, `Expiration`
- Repository: `baypay/payment-service`, immutable tags, scan-on-push
- No access keys, no `BAYPAY_DB_*`, no ALB, no NAT, no RDS, no EKS

Student labs BUILD-1201 / BUILD-1202 teach the same skeleton and then modules. Optional live ECS remains BUILD-1101 and ACCOUNT.md cost rules.

## Validate (no AWS account)

```bash
cd infrastructure/terraform/baypay-ecs
terraform init -backend=false
terraform validate
```

## Cost

`validate` is $0. Optional `apply` creates one ECR repository in `us-west-2`. Destroy it. Do not add an ALB from this folder.
