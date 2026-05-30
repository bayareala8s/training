# Capstone Project – [Your Project Name]

**Student:** [Your Name]  
**Scenario:** Option [1–4] – [Banking | Healthcare | E-Commerce | Enterprise]  
**Course:** Cloud-Native Data Engineering on AWS

---

## Overview

[2–3 sentences describing the business problem and your solution. Example: "This project implements a cloud-native data lake for RetailCo e-commerce analytics, ingesting daily orders and clickstream events, validating data quality, and serving curated datasets via Athena."]

## Architecture Summary

```text
[Optional ASCII diagram or link to architecture/diagrams/]
Sources → Ingestion → S3 (raw/cleaned/curated) → Glue ETL → Athena / ML
                              ↓
                    Quality · Governance · Monitoring
```

## Prerequisites

- AWS account with admin or PowerUser access
- Terraform 1.5+
- AWS CLI configured (`aws sts get-caller-identity`)
- Python 3.10+ (for validation scripts)
- See [course setup](../../../setup/SETUP.md)

## Quick Start

### 1. Clone and Configure

```bash
cd capstone/my-project
cp infrastructure/terraform/terraform.tfvars.example infrastructure/terraform/terraform.tfvars
# Edit terraform.tfvars: region, student name, alert email
```

### 2. Deploy Infrastructure

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

Save outputs:

```bash
terraform output -json > ../../deploy-outputs.json
```

### 3. Upload Sample Data

```bash
export BUCKET=$(terraform output -raw data_lake_bucket)
aws s3 sync ../../sample-data/raw/ s3://$BUCKET/raw/
```

### 4. Run ETL Pipeline

```bash
# Option A: Trigger Glue job
aws glue start-job-run --job-name $(terraform output -raw glue_job_name)

# Option B: Run local validation
python3 ../../src/validation/quality_runner.py --input ../../sample-data/cleaned/
```

### 5. Verify

```bash
# Check curated zone
aws s3 ls s3://$BUCKET/curated/ --recursive | head

# Athena query (replace workgroup/database)
aws athena start-query-execution \
  --query-string "SELECT count(*) FROM curated_db.fact_orders LIMIT 10" \
  --work-group primary
```

### 6. View Monitoring

Open CloudWatch dashboard: `[dashboard-name from terraform output]`

## Project Structure

```text
my-project/
├── README.md                 # This file
├── docs/
│   ├── ARCHITECTURE.md       # Design decisions
│   ├── GOVERNANCE.md         # Security and compliance
│   └── COST-ANALYSIS.md      # Cost breakdown
├── infrastructure/
│   └── terraform/            # IaC deployment
├── src/
│   ├── ingestion/            # Lambda handlers
│   ├── etl/                  # Glue scripts
│   └── validation/           # Quality framework
├── sample-data/              # Test datasets
├── architecture/
│   └── diagrams/             # PNG/SVG exports
└── presentation/
    └── slides/               # Final deck
```

## Key AWS Resources

| Resource | Name Pattern | Purpose |
|----------|--------------|---------|
| S3 Data Lake | `{project}-capstone-datalake-{account}` | Storage |
| Glue Job | `{project}-capstone-etl-*` | ETL processing |
| CloudWatch Dashboard | `{project}-capstone-etl-pipeline` | Monitoring |
| SNS Topic | `{project}-capstone-alerts-*` | Alerting |

## Documentation

- [Architecture & Design Decisions](docs/ARCHITECTURE.md)
- [Governance & Security](docs/GOVERNANCE.md)
- [Cost Analysis](docs/COST-ANALYSIS.md)

## Testing

```bash
# Run validation unit tests (if present)
python3 -m pytest src/validation/tests/ -v

# Generate quality report
python3 src/validation/quality_runner.py \
  --rules src/validation/rules/orders_rules.json \
  --input sample-data/cleaned/orders.json \
  --output reports/
```

## Cleanup

**Important:** Destroy resources to avoid ongoing AWS charges.

```bash
cd infrastructure/terraform
terraform destroy
```

Verify bucket empty before destroy if required.

## Tags

All resources tagged:

```text
Project=capstone
Student=[your-name]
Environment=dev
Course=cloud-native-data-engineering
```

## Author

[Your Name] – [LinkedIn URL optional]  
Completed: [Date]

## License

Course project – [Your Institution / Personal Portfolio Use]
