# Infrastructure

Terraform modules and IaC templates for the course data platform.

## Structure

```text
infrastructure/
├── README.md
├── modules/
│   ├── s3-data-lake/         # S3 buckets with zone structure
│   ├── lambda-ingestion/     # Lambda functions for ingestion
│   ├── glue-etl/             # Glue jobs, crawlers, catalog
│   ├── quality-validation/   # Lab 4.2 validation Lambda
│   ├── step-functions/       # Orchestration workflows
│   └── monitoring/           # CloudWatch dashboards and alarms
└── environments/
    └── dev/                  # Development environment (labs)
```

## Getting Started

### Prerequisites

- [Terraform](https://www.terraform.io/downloads) >= 1.5
- AWS CLI configured with appropriate credentials
- S3 bucket for Terraform state (recommended for teams)

### Deploy Development Environment

**Recommended** — use the lab cycle script from the repo root:

```bash
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh
```

Or deploy manually:

```bash
cd infrastructure/environments/dev
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
terraform init
terraform plan
terraform apply
```

### Tear Down

```bash
./scripts/lab-cycle.sh stop --yes
```

## Module Overview

| Module | Description | Used In |
|--------|-------------|---------|
| `s3-data-lake` | Raw/Cleaned/Curated S3 buckets with lifecycle policies | Module 1 |
| `lambda-ingestion` | Lambda + EventBridge ingestion pipeline | Module 2 |
| `glue-etl` | Glue crawlers, jobs, and data catalog | Module 3 |
| `quality-validation` | Lab 4.1 RuleEngine packaged as Lambda | Module 4 |
| `step-functions` | Multi-stage ETL orchestration | Module 6 |
| `monitoring` | CloudWatch dashboards and SNS alerts | Module 8 |

## Tagging Convention

All resources are tagged consistently:

```hcl
tags = {
  Project     = "cnde"                        # from var.project in terraform.tfvars
  Environment = "dev"
  ManagedBy   = "terraform"
  Course      = "cloud-native-data-engineering"
  Student     = "your-name"
}
```

Use `Project=cnde` and `Course=cloud-native-data-engineering` for cost reporting (Lab 8.3).

## Cost Management

- Use `dev` environment for labs; destroy resources when not in use
- Run `./scripts/lab-cycle.sh stop --yes` at end of each lab session
- Set AWS Budget alerts (recommended: $20/month for lab work)
- Keep `enable_schedules = false` in `terraform.tfvars` unless testing automation

## Security Notes

- Never commit `terraform.tfvars` with real credentials
- Use IAM roles with least-privilege permissions
- Enable S3 bucket encryption and block public access (enabled by default in modules)
