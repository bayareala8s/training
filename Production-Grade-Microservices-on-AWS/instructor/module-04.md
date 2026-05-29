# Instructor Notes — Module 4

## Before lab

- `terraform apply` in shared demo account
- Prepare ALB Terraform extension OR demo with single public ECS task (simpler)

## Simplified path for tight budgets

- Deploy **one** service to ECS; others remain on Compose
- Still meets learning objectives if ALB + Fargate demonstrated

## Troubleshooting ECS

- Task stops immediately → check CloudWatch logs, execution role
- Health check failing → verify `/health` path and security group
