# Lab Architecture Diagrams

Visual guides for every hands-on lab in **Cloud-Native Data Engineering on AWS**.

Each diagram is available in four formats:

| Format | Location | Best for |
|--------|----------|----------|
| **Mermaid** | `diagram.md` in each lab folder | GitHub, VS Code preview, LMS |
| **Draw.io (AWS stencils)** | [`drawio/`](drawio/) | Editing in [diagrams.net](https://app.diagrams.net) with official AWS icons |
| **PNG** | [`png/`](png/) | Slides, PDFs, printed handouts |
| **SVG** | [`svg/`](svg/) | Scalable embeds, web pages |

Regenerate Draw.io sources and export PNG/SVG:

```bash
./scripts/export-drawio.sh              # requires draw.io desktop
DRAWIO_DOCKER=1 ./scripts/export-drawio.sh   # headless via Docker
```

---

## Platform Overview

| Diagram | Mermaid | Draw.io | PNG | SVG |
|---------|---------|---------|-----|-----|
| Course Platform Overview | [MD](course-platform-overview.md) | [drawio](drawio/course-platform-overview.drawio) | [png](png/course-platform-overview.png) | [svg](svg/course-platform-overview.svg) |
| Capstone — Banking | [MD](capstone-architectures.md) | [drawio](drawio/capstone-banking.drawio) | [png](png/capstone-banking.png) | [svg](svg/capstone-banking.svg) |
| Capstone — Healthcare | [MD](capstone-architectures.md) | [drawio](drawio/capstone-healthcare.drawio) | [png](png/capstone-healthcare.png) | [svg](svg/capstone-healthcare.svg) |
| Capstone — E-Commerce | [MD](capstone-architectures.md) | [drawio](drawio/capstone-ecommerce.drawio) | [png](png/capstone-ecommerce.png) | [svg](svg/capstone-ecommerce.svg) |
| Capstone — Enterprise | [MD](capstone-architectures.md) | [drawio](drawio/capstone-enterprise.drawio) | [png](png/capstone-enterprise.png) | [svg](svg/capstone-enterprise.svg) |

---

## Module 1 — Modern Data Engineering Foundations

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 1.1 | [Build S3 Data Lake](../../modules/module-01-foundations/labs/lab-1.1-build-s3-data-lake/diagram.md) | [drawio](drawio/lab-1.1-build-s3-data-lake.drawio) | [png](png/lab-1.1-build-s3-data-lake.png) | [svg](svg/lab-1.1-build-s3-data-lake.svg) | Terraform → S3 bucket, encryption, lifecycle, zones |
| Lab 1.2 | [Data Lake Zones](../../modules/module-01-foundations/labs/lab-1.2-data-lake-zones/diagram.md) | [drawio](drawio/lab-1.2-data-lake-zones.drawio) | [png](png/lab-1.2-data-lake-zones.png) | [svg](svg/lab-1.2-data-lake-zones.svg) | Medallion layout, Hive partitioning, metadata manifests |

## Module 2 — Data Ingestion Patterns

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 2.1 | [Lambda Ingestion](../../modules/module-02-ingestion/labs/lab-2.1-lambda-ingestion/diagram.md) | [drawio](drawio/lab-2.1-lambda-ingestion.drawio) | [png](png/lab-2.1-lambda-ingestion.png) | [svg](svg/lab-2.1-lambda-ingestion.svg) | JSON → Lambda → S3 raw zone (idempotent keys) |
| Lab 2.2 | [EventBridge Automation](../../modules/module-02-ingestion/labs/lab-2.2-eventbridge-automation/diagram.md) | [drawio](drawio/lab-2.2-eventbridge-automation.drawio) | [png](png/lab-2.2-eventbridge-automation.png) | [svg](svg/lab-2.2-eventbridge-automation.svg) | Scheduled API pull, watermarks, incremental loads |
| Lab 2.3 | [S3 Event Processing](../../modules/module-02-ingestion/labs/lab-2.3-s3-event-processing/diagram.md) | [drawio](drawio/lab-2.3-s3-event-processing.drawio) | [png](png/lab-2.3-s3-event-processing.png) | [svg](svg/lab-2.3-s3-event-processing.svg) | `incoming/` → promote to raw or quarantine |

## Module 3 — AWS Glue ETL Engineering

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 3.1 | [Raw → Cleaned ETL](../../modules/module-03-glue-etl/labs/lab-3.1-etl-raw-to-cleaned/diagram.md) | [drawio](drawio/lab-3.1-etl-raw-to-cleaned.drawio) | [png](png/lab-3.1-etl-raw-to-cleaned.png) | [svg](svg/lab-3.1-etl-raw-to-cleaned.svg) | Glue PySpark job, CSV → Parquet transformation |
| Lab 3.2 | [Glue Crawlers](../../modules/module-03-glue-etl/labs/lab-3.2-glue-crawlers/diagram.md) | [drawio](drawio/lab-3.2-glue-crawlers.drawio) | [png](png/lab-3.2-glue-crawlers.png) | [svg](svg/lab-3.2-glue-crawlers.svg) | Crawler → Data Catalog → Athena |
| Lab 3.3 | [ETL Optimization](../../modules/module-03-glue-etl/labs/lab-3.3-etl-optimization/diagram.md) | [drawio](drawio/lab-3.3-etl-optimization.drawio) | [png](png/lab-3.3-etl-optimization.png) | [svg](svg/lab-3.3-etl-optimization.svg) | Partitioning, coalesce, before/after performance |

## Module 4 — Data Quality & Reliability

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 4.1 | [Quality Framework](../../modules/module-04-data-quality/labs/lab-4.1-quality-framework/diagram.md) | [drawio](drawio/lab-4.1-quality-framework.drawio) | [png](png/lab-4.1-quality-framework.png) | [svg](svg/lab-4.1-quality-framework.svg) | Rule engine, pass/quarantine routing |
| Lab 4.2 | [Validation Automation](../../modules/module-04-data-quality/labs/lab-4.2-validation-automation/diagram.md) | [drawio](drawio/lab-4.2-validation-automation.drawio) | [png](png/lab-4.2-validation-automation.png) | [svg](svg/lab-4.2-validation-automation.svg) | Lambda/Glue integration, CloudWatch metrics |
| Lab 4.3 | [Quarantine Zone](../../modules/module-04-data-quality/labs/lab-4.3-quarantine-zone/diagram.md) | [drawio](drawio/lab-4.3-quarantine-zone.drawio) | [png](png/lab-4.3-quarantine-zone.png) | [svg](svg/lab-4.3-quarantine-zone.svg) | Bad record isolation, steward replay workflow |

## Module 5 — Data Modeling & Analytics

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 5.1 | [Star Schema](../../modules/module-05-modeling-analytics/labs/lab-5.1-star-schema/diagram.md) | [drawio](drawio/lab-5.1-star-schema.drawio) | [png](png/lab-5.1-star-schema.png) | [svg](svg/lab-5.1-star-schema.svg) | dim_customer, dim_product, fact_orders ER diagram |
| Lab 5.2 | [Athena Optimization](../../modules/module-05-modeling-analytics/labs/lab-5.2-athena-optimization/diagram.md) | [drawio](drawio/lab-5.2-athena-optimization.drawio) | [png](png/lab-5.2-athena-optimization.png) | [svg](svg/lab-5.2-athena-optimization.svg) | Partition pruning, column projection, query plans |
| Lab 5.3 | [Cost-Efficient Queries](../../modules/module-05-modeling-analytics/labs/lab-5.3-cost-efficient-queries/diagram.md) | [drawio](drawio/lab-5.3-cost-efficient-queries.drawio) | [png](png/lab-5.3-cost-efficient-queries.png) | [svg](svg/lab-5.3-cost-efficient-queries.svg) | Summary tables, analyst views, workgroup limits |

## Module 6 — Orchestration & Workflow Automation

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 6.1 | [Step Functions ETL](../../modules/module-06-orchestration/labs/lab-6.1-step-functions-etl/diagram.md) | [drawio](drawio/lab-6.1-step-functions-etl.drawio) | [png](png/lab-6.1-step-functions-etl.png) | [svg](svg/lab-6.1-step-functions-etl.svg) | Multi-stage pipeline: Glue → quality → success |
| Lab 6.2 | [Retry & Error Branching](../../modules/module-06-orchestration/labs/lab-6.2-retry-error-branching/diagram.md) | [drawio](drawio/lab-6.2-retry-error-branching.drawio) | [png](png/lab-6.2-retry-error-branching.png) | [svg](svg/lab-6.2-retry-error-branching.svg) | Retry policies, Catch states, error paths |
| Lab 6.3 | [SNS Failure Handling](../../modules/module-06-orchestration/labs/lab-6.3-sns-failure-handling/diagram.md) | [drawio](drawio/lab-6.3-sns-failure-handling.drawio) | [png](png/lab-6.3-sns-failure-handling.png) | [svg](svg/lab-6.3-sns-failure-handling.svg) | Alert routing, sanitized notifications |

## Module 7 — Security, Governance & Compliance

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 7.1 | [KMS & Bucket Policies](../../modules/module-07-security-governance/labs/lab-7.1-kms-bucket-policies/diagram.md) | [drawio](drawio/lab-7.1-kms-bucket-policies.drawio) | [png](png/lab-7.1-kms-bucket-policies.png) | [svg](svg/lab-7.1-kms-bucket-policies.svg) | Encryption at rest, bucket policy enforcement |
| Lab 7.2 | [IAM RBAC Data Zones](../../modules/module-07-security-governance/labs/lab-7.2-iam-rbac-data-zones/diagram.md) | [drawio](drawio/lab-7.2-iam-rbac-data-zones.drawio) | [png](png/lab-7.2-iam-rbac-data-zones.png) | [svg](svg/lab-7.2-iam-rbac-data-zones.svg) | Role-based access per medallion zone |
| Lab 7.3 | [Governance Audit](../../modules/module-07-security-governance/labs/lab-7.3-governance-audit/diagram.md) | [drawio](drawio/lab-7.3-governance-audit.drawio) | [png](png/lab-7.3-governance-audit.png) | [svg](svg/lab-7.3-governance-audit.svg) | Audit trail, compliance validation checklist |

## Module 8 — Monitoring, Cost Optimization & Operations

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 8.1 | [CloudWatch Dashboards](../../modules/module-08-monitoring-ops/labs/lab-8.1-cloudwatch-dashboards/diagram.md) | [drawio](drawio/lab-8.1-cloudwatch-dashboards.drawio) | [png](png/lab-8.1-cloudwatch-dashboards.png) | [svg](svg/lab-8.1-cloudwatch-dashboards.svg) | ETL pipeline observability widgets |
| Lab 8.2 | [SNS Alerts](../../modules/module-08-monitoring-ops/labs/lab-8.2-sns-alerts/diagram.md) | [drawio](drawio/lab-8.2-sns-alerts.drawio) | [png](png/lab-8.2-sns-alerts.png) | [svg](svg/lab-8.2-sns-alerts.svg) | Alarm → SNS → email/Slack routing |
| Lab 8.3 | [Cost Reporting](../../modules/module-08-monitoring-ops/labs/lab-8.3-cost-reporting/diagram.md) | [drawio](drawio/lab-8.3-cost-reporting.drawio) | [png](png/lab-8.3-cost-reporting.png) | [svg](svg/lab-8.3-cost-reporting.svg) | Cost allocation tags, Cost Explorer views |

## Module 9 — Data Engineering for AI & ML

| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |
|-----|---------|---------|-----|-----|---------------|
| Lab 9.1 | [ML Dataset Prep](../../modules/module-09-ai-ml-data/labs/lab-9.1-ml-dataset-prep/diagram.md) | [drawio](drawio/lab-9.1-ml-dataset-prep.drawio) | [png](png/lab-9.1-ml-dataset-prep.png) | [svg](svg/lab-9.1-ml-dataset-prep.svg) | Point-in-time features, train/val/test splits |
| Lab 9.2 | [Feature Store Pipeline](../../modules/module-09-ai-ml-data/labs/lab-9.2-feature-store-pipeline/diagram.md) | [drawio](drawio/lab-9.2-feature-store-pipeline.drawio) | [png](png/lab-9.2-feature-store-pipeline.png) | [svg](svg/lab-9.2-feature-store-pipeline.svg) | Feature registry, offline feature pipeline |
| Lab 9.3 | [AI Data Quality](../../modules/module-09-ai-ml-data/labs/lab-9.3-ai-data-quality/diagram.md) | [drawio](drawio/lab-9.3-ai-data-quality.drawio) | [png](png/lab-9.3-ai-data-quality.png) | [svg](svg/lab-9.3-ai-data-quality.svg) | PSI drift, label leakage, class balance checks |

## How Students Should Use These Diagrams

1. **Before each lab** — Review the diagram to understand what you are building
2. **During the lab** — Compare your AWS console to the diagram components
3. **After the lab** — Use the diagram in your `LAB-REPORT.md` and portfolio

## Viewing Tips

- **GitHub:** Open any `diagram.md` file — Mermaid renders automatically
- **VS Code:** Install "Markdown Preview Mermaid Support" extension
- **Draw.io:** Open any `.drawio` file from [`drawio/`](drawio/) in [diagrams.net](https://app.diagrams.net) — uses official AWS Architecture Icons (`mxgraph.aws4.*`)
- **Slides & docs:** Use pre-exported files in [`png/`](png/) or [`svg/`](svg/)
- **Regenerate:** Run `./scripts/export-drawio.sh` (or `DRAWIO_DOCKER=1 ./scripts/export-drawio.sh`)

---

## Diagram Count

| Category | Count | Formats |
|----------|-------|---------|
| Lab diagrams | 26 | Mermaid + Draw.io + PNG + SVG |
| Platform overview | 1 | Mermaid + Draw.io + PNG + SVG |
| Capstone options | 4 | Mermaid + Draw.io + PNG + SVG |
| **Total** | **31** | **124 files** (31 × 4 formats) |
