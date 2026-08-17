# Infrastructure

Terraform modules and IaC templates for the course data platform.

## Structure

```text
infrastructure/
├── README.md
├── modules/
│   ├── s3-data-lake/       # S3 buckets with zone structure
│   ├── glue-etl/           # Glue jobs, crawlers, catalog
│   ├── lambda-ingestion/   # Lambda functions for ingestion
│   ├── step-functions/     # Orchestration workflows
│   └── monitoring/         # CloudWatch dashboards and alarms
└── environments/
    ├── dev/                # Development environment
    └── prod/               # Production environment (capstone)
```

## Getting Started

### Prerequisites

- [Terraform](https://www.terraform.io/downloads) >= 1.5
- AWS CLI configured with appropriate credentials
- S3 bucket for Terraform state (recommended)

### Deploy Development Environment

```bash
cd infrastructure/environments/dev
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
terraform init
terraform plan
terraform apply
```

### Tagging Convention

All resources must be tagged:

```hcl
tags = {
  Project     = "cloud-native-data-engineering"
  Environment = "dev"
  ManagedBy   = "terraform"
  Student     = "your-name"   # for lab/capstone work
}
```

## Module Overview

| Module | Description | Used In |
|--------|-------------|---------|
| `s3-data-lake` | Raw/Cleaned/Curated S3 buckets with lifecycle policies | Module 1 |
| `lambda-ingestion` | Lambda + EventBridge ingestion pipeline | Module 2 |
| `glue-etl` | Glue crawlers, jobs, and data catalog | Module 3 |
| `step-functions` | Multi-stage ETL orchestration | Module 6 |
| `monitoring` | CloudWatch dashboards and SNS alerts | Module 8 |

## Cost Management

- Use `dev` environment for labs; destroy resources when not in use
- Run `terraform destroy` at end of each lab session
- Set AWS Budget alerts (recommended: $20/month for lab work)

```bash
terraform destroy   # Always run when finished with labs
```

## Security Notes

- Never commit `terraform.tfvars` with real credentials
- Use IAM roles with least-privilege permissions
- Enable S3 bucket encryption and block public access (enabled by default in modules)
