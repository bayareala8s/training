# Assignment 2: Event-Driven Ingestion Design (Banking)

**Due:** End of Week 2 · **Weight:** Part of Assignments (20%)

---

## Scenario

**FirstNational Bank** is modernizing its data platform. Current state:

- **Core banking** exports end-of-day transaction files (CSV, ~5 GB) to SFTP at 02:00 UTC
- **Card processor** sends authorization events via HTTPS webhook (~50K events/hour during peak)
- **CRM** exposes a REST API for customer profile updates (incremental, `updated_since`)
- **AML compliance** requires immutable raw retention for 7 years with full lineage
- **Fraud team** needs near-real-time access to card events (< 5 minute latency)
- **Finance** needs daily reconciled transaction snapshots by 06:00 UTC
- Regulators may audit any pipeline run; PII (account numbers, SSN) must be protected

The bank already deployed an S3 data lake (Module 1) with `raw/`, `cleaned/`, `curated/`, `quarantine/`, and `metadata/` zones.

---

## Your Task

Design an **event-driven ingestion architecture on AWS** that replaces ad-hoc scripts and supports all FirstNational sources. You are **not** required to implement code—focus on architecture, controls, and operational design.

---

## Deliverables

Submit a document (3–4 pages) plus diagrams containing:

### 1. Executive Summary (½ page)

- Current pain points
- Proposed ingestion approach (event-driven vs batch-only)
- Business outcomes (compliance, fraud latency, cost)

### 2. Architecture Diagram

Include:

- All data sources and ingestion paths
- Lambda, EventBridge, S3 events, API Gateway (where applicable)
- Landing vs raw vs quarantine flows
- Watermark / metadata storage
- Monitoring and alerting (CloudWatch, SNS)
- Security controls (IAM, encryption, Secrets Manager)

Use Mermaid, Draw.io, or Lucidchart.

### 3. Ingestion Pattern Matrix (1 page)

| Source | Pattern | AWS Services | Frequency | Raw Zone Path Example | Idempotency Strategy |
|--------|---------|--------------|-----------|----------------------|----------------------|
| Core banking SFTP | ? | ? | ? | ? | ? |
| Card webhooks | ? | ? | ? | ? | ? |
| CRM API | ? | ? | ? | ? | ? |

Fill every cell with specific, justified choices.

### 4. Incremental Load & Watermark Design (½ page)

- How CRM API ingestion avoids full reloads
- Where watermarks are stored (S3 vs DynamoDB) and why
- How you handle **late-arriving** transactions for finance reports

### 5. Failure Handling & Operations (1 page)

Address:

- What happens when the card webhook endpoint is flooded?
- How failed CSV files are quarantined without blocking the pipeline
- DLQ strategy for Lambda
- Runbook: ingestion lag alarm fires—first 5 investigation steps
- Proof of lineage for auditors (logs, object metadata, CloudTrail)

### 6. Security & Compliance (½ page)

- PII handling in raw zone (masking timing, KMS keys)
- IAM least-privilege examples (prefix-scoped policies)
- How idempotent processing supports regulatory reproducibility

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Architecture completeness (all sources) | 25 |
| Correct use of event-driven patterns | 20 |
| Idempotency and incremental design | 20 |
| Security, compliance, operations | 20 |
| Clarity, diagrams, professionalism | 15 |
| **Total** | **100** |

---

## Submission Format

- File: `assignment-02-{your-name}.md` or PDF
- Embed or attach architecture diagram
- Submit via your learning platform

---

## Reference Paths (Examples)

```text
s3://fnbank-prod-datalake/incoming/core/transactions/2024-01-15_eod.csv
s3://fnbank-prod-datalake/raw/core/transactions/year=2024/month=01/day=15/eod_2024-01-15.csv
s3://fnbank-prod-datalake/raw/cards/authorizations/year=2024/month=01/day=15/hour=14/event_id=abc123.json
s3://fnbank-prod-datalake/metadata/watermarks/crm/customers.json
s3://fnbank-prod-datalake/quarantine/core/transactions/20240115_invalid_schema.json
```

---

## Tips

- Reference [Week 2 Lecture](../lectures/week-02-lecture.md) pattern selection matrix
- Card events may need **Kinesis** for peak throughput—justify if you include or exclude it
- Separate **latency requirements** by consumer (fraud vs finance)
- Do not put secrets in S3 object keys or CloudWatch logs

---

## Connection to Labs

| Lab | Concept to Reference |
|-----|---------------------|
| Lab 2.1 | Idempotent Lambda writes to raw |
| Lab 2.2 | EventBridge schedule + API watermarks |
| Lab 2.3 | S3 events, promotion, quarantine |

---

**Next week:** [Module 3 – AWS Glue ETL Engineering](../../module-03-glue-etl/README.md)
