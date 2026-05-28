# AWS Lab Start / Stop Scripts

Cost-control scripts for **BayAreaLa8s – Terraform for Real Enterprises**. They start and stop (or scale to zero) AWS resources tagged for the course.

## Required tags

All lab Terraform in this course applies:

```hcl
tags = {
  Course    = "terraform-enterprise"
  Project   = "bayareala8s-tf-course"
  ManagedBy = "terraform"
  Environment = var.environment
}
```

Only resources with `Course = terraform-enterprise` are affected.

## Prerequisites

- [AWS CLI v2](https://aws.amazon.com/cli/) configured (`aws sts get-caller-identity`)
- IAM permissions: `ec2:*`, `rds:*`, `ecs:UpdateService`, `autoscaling:UpdateAutoScalingGroup`, `resourcegroupstaggingapi:GetResources`

## Quick start

```bash
cd scripts/aws
chmod +x *.sh lib/*.sh

# Before lab session
./start-lab.sh

# After lab session (save money)
./stop-lab.sh

# Check state
./status-lab.sh
```

## Options

| Script | Purpose |
|--------|---------|
| `start-lab.sh` | Start EC2, RDS, scale ASG/ECS up |
| `stop-lab.sh` | Stop EC2/RDS, scale ASG/ECS to 0 |
| `status-lab.sh` | Show EC2/RDS status |
| `destroy-lab-sandbox.sh` | `terraform destroy` for dev (interactive) |

### Flags

```bash
./stop-lab.sh --ec2-only
./stop-lab.sh --rds-only
./start-lab.sh --all
DRY_RUN=1 ./stop-lab.sh    # preview only
AWS_REGION=us-east-1 ./start-lab.sh
```

## What is NOT stopped

| Resource | Reason |
|----------|--------|
| **NAT Gateway** | AWS does not support stop; destroy with Terraform |
| **S3 / DynamoDB state** | Must remain for Terraform |
| **VPC, subnets, IGW** | No hourly charge for empty VPC (NAT/EIP cost remains) |

For weekends, run `terraform destroy` in `labs/shared/environments/dev` or use `destroy-lab-sandbox.sh`.

## Makefile (repo root)

```bash
make lab-start
make lab-stop
make lab-status
```
