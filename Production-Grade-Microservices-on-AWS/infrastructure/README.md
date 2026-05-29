# Infrastructure as Code

Terraform modules for the course platform. Deploy order:

1. `network/` — VPC, subnets, security groups
2. `ecr/` — Container repositories
3. `ecs/` — Fargate cluster, services, ALB
4. `data/` — DynamoDB tables, RDS (optional)
5. `events/` — EventBridge buses and rules
6. `observability/` — CloudWatch dashboards, X-Ray

## Conventions

- Use workspaces or `-var-file` per environment (`dev`, `staging`, `prod`)
- Never commit `*.tfvars` with secrets
- Tag all resources: `Project`, `Environment`, `Owner`

## Prerequisites

- Terraform ≥ 1.5
- AWS CLI configured
- Appropriate IAM permissions for instructors/students (scoped policies recommended)
