#!/usr/bin/env python3
"""Regenerate lab rows in docs/diagrams/README.md with all format links."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
README = REPO / "docs/diagrams/README.md"

MODULES = [
    ("Module 1 — Modern Data Engineering Foundations", [
        ("Lab 1.1", "Build S3 Data Lake", "lab-1.1-build-s3-data-lake",
         "../../modules/module-01-foundations/labs/lab-1.1-build-s3-data-lake/diagram.md",
         "Terraform → S3 bucket, encryption, lifecycle, zones"),
        ("Lab 1.2", "Data Lake Zones", "lab-1.2-data-lake-zones",
         "../../modules/module-01-foundations/labs/lab-1.2-data-lake-zones/diagram.md",
         "Medallion layout, Hive partitioning, metadata manifests"),
    ]),
    ("Module 2 — Data Ingestion Patterns", [
        ("Lab 2.1", "Lambda Ingestion", "lab-2.1-lambda-ingestion",
         "../../modules/module-02-ingestion/labs/lab-2.1-lambda-ingestion/diagram.md",
         "JSON → Lambda → S3 raw zone (idempotent keys)"),
        ("Lab 2.2", "EventBridge Automation", "lab-2.2-eventbridge-automation",
         "../../modules/module-02-ingestion/labs/lab-2.2-eventbridge-automation/diagram.md",
         "Scheduled API pull, watermarks, incremental loads"),
        ("Lab 2.3", "S3 Event Processing", "lab-2.3-s3-event-processing",
         "../../modules/module-02-ingestion/labs/lab-2.3-s3-event-processing/diagram.md",
         "`incoming/` → promote to raw or quarantine"),
    ]),
    ("Module 3 — AWS Glue ETL Engineering", [
        ("Lab 3.1", "Raw → Cleaned ETL", "lab-3.1-etl-raw-to-cleaned",
         "../../modules/module-03-glue-etl/labs/lab-3.1-etl-raw-to-cleaned/diagram.md",
         "Glue PySpark job, CSV → Parquet transformation"),
        ("Lab 3.2", "Glue Crawlers", "lab-3.2-glue-crawlers",
         "../../modules/module-03-glue-etl/labs/lab-3.2-glue-crawlers/diagram.md",
         "Crawler → Data Catalog → Athena"),
        ("Lab 3.3", "ETL Optimization", "lab-3.3-etl-optimization",
         "../../modules/module-03-glue-etl/labs/lab-3.3-etl-optimization/diagram.md",
         "Partitioning, coalesce, before/after performance"),
    ]),
    ("Module 4 — Data Quality & Reliability", [
        ("Lab 4.1", "Quality Framework", "lab-4.1-quality-framework",
         "../../modules/module-04-data-quality/labs/lab-4.1-quality-framework/diagram.md",
         "Rule engine, pass/quarantine routing"),
        ("Lab 4.2", "Validation Automation", "lab-4.2-validation-automation",
         "../../modules/module-04-data-quality/labs/lab-4.2-validation-automation/diagram.md",
         "Lambda/Glue integration, CloudWatch metrics"),
        ("Lab 4.3", "Quarantine Zone", "lab-4.3-quarantine-zone",
         "../../modules/module-04-data-quality/labs/lab-4.3-quarantine-zone/diagram.md",
         "Bad record isolation, steward replay workflow"),
    ]),
    ("Module 5 — Data Modeling & Analytics", [
        ("Lab 5.1", "Star Schema", "lab-5.1-star-schema",
         "../../modules/module-05-modeling-analytics/labs/lab-5.1-star-schema/diagram.md",
         "dim_customer, dim_product, fact_orders ER diagram"),
        ("Lab 5.2", "Athena Optimization", "lab-5.2-athena-optimization",
         "../../modules/module-05-modeling-analytics/labs/lab-5.2-athena-optimization/diagram.md",
         "Partition pruning, column projection, query plans"),
        ("Lab 5.3", "Cost-Efficient Queries", "lab-5.3-cost-efficient-queries",
         "../../modules/module-05-modeling-analytics/labs/lab-5.3-cost-efficient-queries/diagram.md",
         "Summary tables, analyst views, workgroup limits"),
    ]),
    ("Module 6 — Orchestration & Workflow Automation", [
        ("Lab 6.1", "Step Functions ETL", "lab-6.1-step-functions-etl",
         "../../modules/module-06-orchestration/labs/lab-6.1-step-functions-etl/diagram.md",
         "Multi-stage pipeline: Glue → quality → success"),
        ("Lab 6.2", "Retry & Error Branching", "lab-6.2-retry-error-branching",
         "../../modules/module-06-orchestration/labs/lab-6.2-retry-error-branching/diagram.md",
         "Retry policies, Catch states, error paths"),
        ("Lab 6.3", "SNS Failure Handling", "lab-6.3-sns-failure-handling",
         "../../modules/module-06-orchestration/labs/lab-6.3-sns-failure-handling/diagram.md",
         "Alert routing, sanitized notifications"),
    ]),
    ("Module 7 — Security, Governance & Compliance", [
        ("Lab 7.1", "KMS & Bucket Policies", "lab-7.1-kms-bucket-policies",
         "../../modules/module-07-security-governance/labs/lab-7.1-kms-bucket-policies/diagram.md",
         "Encryption at rest, bucket policy enforcement"),
        ("Lab 7.2", "IAM RBAC Data Zones", "lab-7.2-iam-rbac-data-zones",
         "../../modules/module-07-security-governance/labs/lab-7.2-iam-rbac-data-zones/diagram.md",
         "Role-based access per medallion zone"),
        ("Lab 7.3", "Governance Audit", "lab-7.3-governance-audit",
         "../../modules/module-07-security-governance/labs/lab-7.3-governance-audit/diagram.md",
         "Audit trail, compliance validation checklist"),
    ]),
    ("Module 8 — Monitoring, Cost Optimization & Operations", [
        ("Lab 8.1", "CloudWatch Dashboards", "lab-8.1-cloudwatch-dashboards",
         "../../modules/module-08-monitoring-ops/labs/lab-8.1-cloudwatch-dashboards/diagram.md",
         "ETL pipeline observability widgets"),
        ("Lab 8.2", "SNS Alerts", "lab-8.2-sns-alerts",
         "../../modules/module-08-monitoring-ops/labs/lab-8.2-sns-alerts/diagram.md",
         "Alarm → SNS → email/Slack routing"),
        ("Lab 8.3", "Cost Reporting", "lab-8.3-cost-reporting",
         "../../modules/module-08-monitoring-ops/labs/lab-8.3-cost-reporting/diagram.md",
         "Cost allocation tags, Cost Explorer views"),
    ]),
    ("Module 9 — Data Engineering for AI & ML", [
        ("Lab 9.1", "ML Dataset Prep", "lab-9.1-ml-dataset-prep",
         "../../modules/module-09-ai-ml-data/labs/lab-9.1-ml-dataset-prep/diagram.md",
         "Point-in-time features, train/val/test splits"),
        ("Lab 9.2", "Feature Store Pipeline", "lab-9.2-feature-store-pipeline",
         "../../modules/module-09-ai-ml-data/labs/lab-9.2-feature-store-pipeline/diagram.md",
         "Feature registry, offline feature pipeline"),
        ("Lab 9.3", "AI Data Quality", "lab-9.3-ai-data-quality",
         "../../modules/module-09-ai-ml-data/labs/lab-9.3-ai-data-quality/diagram.md",
         "PSI drift, label leakage, class balance checks"),
    ]),
]


def lab_row(lab_id, title, slug, mermaid_path, description):
    return (
        f"| {lab_id} | [{title}]({mermaid_path}) | "
        f"[drawio](drawio/{slug}.drawio) | "
        f"[png](png/{slug}.png) | "
        f"[svg](svg/{slug}.svg) | {description} |"
    )


def module_section(title, labs):
    lines = [
        f"## {title}",
        "",
        "| Lab | Mermaid | Draw.io | PNG | SVG | What It Shows |",
        "|-----|---------|---------|-----|-----|---------------|",
    ]
    for lab in labs:
        lines.append(lab_row(*lab))
    lines.append("")
    return "\n".join(lines)


def main():
    text = README.read_text()
    start = text.index("## Module 1")
    end = text.index("## How Students Should Use These Diagrams")
    modules_block = "\n".join(module_section(t, labs) for t, labs in MODULES)
    new_text = text[:start] + modules_block + "\n" + text[end:]
    README.write_text(new_text)
    print("Updated module tables in docs/diagrams/README.md")


if __name__ == "__main__":
    main()
