# Architecture – [Project Name]

**Author:** [Your Name]  
**Last Updated:** [Date]  
**Scenario:** Capstone Option [1–4]

---

## 1. Executive Summary

### Problem Statement

[Describe the business problem. Example: RetailCo needs a unified analytics platform to replace siloed databases and support daily sales reporting, customer segmentation, and future ML use cases.]

### Solution Overview

[2–3 paragraphs describing your cloud-native data platform on AWS. Mention medallion architecture, key AWS services, and primary outcomes.]

### Success Criteria

| Criterion | Target |
|-----------|--------|
| Daily pipeline completion | By [time] UTC |
| Data quality pass rate | ≥ [X]% |
| Curated data freshness | ≤ [N] hours |
| Monthly AWS cost (dev) | ≤ $[amount] |

---

## 2. Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Ingest [dataset] from [source] | Must |
| FR-2 | Transform Raw → Cleaned → Curated | Must |
| FR-3 | Validate data quality with quarantine | Must |
| FR-4 | Expose curated data via Athena | Must |
| FR-5 | [Add scenario-specific requirements] | Should |

### Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Scalability** | Handle [N]× current volume without architecture change |
| **Availability** | Pipeline success rate ≥ [X]% |
| **Security** | Encryption at rest and in transit; least-privilege IAM |
| **Compliance** | [HIPAA / SOX / PCI / internal policy – as applicable] |
| **Cost** | Tagged resources; lifecycle policies on raw zone |
| **Observability** | Dashboard + alerts for job failures and quality SLOs |

---

## 3. Architecture Diagrams

### Context Diagram

[Insert diagram or describe: external systems, users, and your platform boundary]

```text
┌─────────────┐     ┌─────────────┐
│ Source A    │     │ Source B    │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └─────────┬─────────┘
                 ▼
        ┌─────────────────┐
        │  Data Platform  │──────→ Analysts / BI
        │  (Your Design)  │──────→ ML Team
        └─────────────────┘
```

### Component Diagram

[Insert detailed diagram: S3 zones, Glue, Lambda, Step Functions, Athena, CloudWatch]

Store exported diagrams in `architecture/diagrams/`:
- `context-diagram.png`
- `component-diagram.png`
- `data-flow-diagram.png`

### Data Flow

| Stage | Input | Process | Output | Service |
|-------|-------|---------|--------|---------|
| Ingest | [source] | [how] | `raw/...` | Lambda / EventBridge |
| Clean | `raw/...` | Validate, type | `cleaned/...` | Glue |
| Curate | `cleaned/...` | Model, aggregate | `curated/...` | Glue |
| Quality fail | `cleaned/...` | Quarantine | `quarantine/...` | Validation Lambda |

---

## 4. AWS Service Selection

| Layer | Service | Justification | Alternatives Considered |
|-------|---------|---------------|-------------------------|
| Storage | Amazon S3 | Durable, cost-effective lake storage | EFS (rejected: cost for analytics) |
| ETL | AWS Glue | Managed Spark, catalog integration | EMR (rejected: ops overhead) |
| Ingestion | AWS Lambda | Event-driven, serverless | EC2 cron (rejected) |
| Orchestration | Step Functions | Visual workflows, retries | Airflow on MWAA (optional upgrade) |
| Analytics | Amazon Athena | Serverless SQL on S3 | Redshift (future scale) |
| Catalog | Glue Data Catalog | Native integration | Hive external (rejected) |
| Monitoring | CloudWatch + SNS | Native metrics and alerts | Third-party APM (optional) |
| Security | IAM + KMS | Standard AWS governance | — |

---

## 5. Data Zone Design

### Zone Definitions

| Zone | Purpose | Retention | Format | Consumers |
|------|---------|-----------|--------|-----------|
| **raw/** | Immutable source copies | [N] years | JSON/CSV/Parquet | ETL only |
| **cleaned/** | Validated, typed | [N] months | Parquet | ETL, quality |
| **curated/** | Business-ready | [N] months | Parquet | Athena, BI, ML |
| **quarantine/** | Failed validation | 90 days | JSON | Data stewards |
| **metadata/** | Schemas, lineage, reports | 1 year | JSON | All teams |

### S3 Path Conventions

```text
s3://[bucket]/raw/[domain]/[dataset]/year=YYYY/month=MM/day=DD/
s3://[bucket]/cleaned/[domain]/[dataset]/year=YYYY/month=MM/day=DD/
s3://[bucket]/curated/[domain]/[entity]/year=YYYY/month=MM/
s3://[bucket]/quarantine/[domain]/[dataset]/run_id=[uuid]/
s3://[bucket]/metadata/quality-reports/[dataset]/YYYY-MM-DD_report.json
```

### Example: [Primary Dataset]

[Describe schema, partition keys, and curated model (star schema table names)]

---

## 6. ETL Design

### Job: [job-name]

| Attribute | Value |
|-----------|-------|
| Trigger | [Schedule / Event / Step Functions] |
| Input | `s3://[bucket]/raw/...` |
| Output | `s3://[bucket]/cleaned/...`, `curated/...` |
| Worker type | G.1X |
| DPU | [N] |
| Job bookmark | Enabled / Disabled |

### Schema Evolution Strategy

[How you handle new columns, type changes, breaking changes]

### Idempotency

[How re-runs produce consistent results—partition overwrite, merge keys]

---

## 7. Orchestration

[Describe Step Functions workflow or scheduled jobs]

```text
Start → Ingest → Validate → [Pass] → ETL → Catalog → Notify Success
                      │
                      └── [Fail] → Quarantine → SNS Alert → End
```

---

## 8. Design Decisions & Trade-offs

### Decision 1: [Title]

- **Context:** [What problem needed a decision]
- **Decision:** [What you chose]
- **Rationale:** [Why]
- **Trade-off:** [What you gave up]

### Decision 2: Batch vs Streaming

[Your choice and justification for the scenario]

### Decision 3: [Scenario-specific]

[Example: PII masking in cleaned vs curated for healthcare]

---

## 9. Future Enhancements

| Enhancement | Priority | Effort |
|-------------|----------|--------|
| Real-time ingestion (Kinesis) | Medium | High |
| Lake Formation fine-grained access | High | Medium |
| dbt/Athena views for semantic layer | Medium | Medium |
| SageMaker Feature Store integration | Low | Medium |
| Multi-region disaster recovery | Low | High |

---

## 10. References

- Course Module [N] – [topic]
- [AWS whitepaper or doc link]
- Assignment [N] – [relevant design work]
