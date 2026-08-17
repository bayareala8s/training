# Architecture – Banking Regulatory Data Platform

**Author:** Capstone Reference Implementation  
**Last Updated:** 2024-01-15  
**Scenario:** Capstone Option 1 – Banking  
**Project key:** `cnde-cap-banking`

---

## 1. Executive Summary

### Problem Statement

Compliance and finance teams need a trusted daily settlement report across currencies and clearing statuses. Source extracts from core banking and clearing houses arrive with inconsistent identifiers, invalid amounts, and incomplete dates. Without automated quality gates and immutable lineage, bad records reach regulatory packs and create audit findings.

### Solution Overview

This platform implements a medallion lake on Amazon S3 (raw → cleaned → curated → quarantine) orchestrated for daily batch processing. Declarative validation (Lab 4.1 rule types: `not_null`, `range`, `enum`, `regex`) screens transactions, settlements, and accounts. Passed settlements are aggregated into **daily_settlement_summary** by `settlement_date`, `currency`, and `status`. Audit manifests under `metadata/` capture pass rates and run identity for SOX-style evidence.

Locally, `../../_shared/run_pipeline.py` executes the full path offline. In AWS, the same zones are populated via the course lab stack and an optional Glue PySpark job (`src/etl/glue_job.py`).

### Success Criteria

| Criterion | Target |
|-----------|--------|
| Daily pipeline completion | By 06:00 UTC |
| Transaction quality pass rate | ≥ 85% on sample; ≥ 98% production SLO |
| Curated settlement summary freshness | ≤ 4 hours after file drop |
| Monthly AWS cost (student / lab) | ≤ $25 |

---

## 2. Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Ingest transactions, settlements, and accounts | Must |
| FR-2 | Validate with quarantine for failing records | Must |
| FR-3 | Publish curated daily_settlement_summary | Must |
| FR-4 | Retain run manifests for audit trail | Must |
| FR-5 | Support Athena queries on curated CSV/Parquet | Should |
| FR-6 | Encrypt data at rest (SSE-S3 / KMS) in AWS | Must |

### Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Scalability** | 10× sample volume without redesign |
| **Availability** | Pipeline success ≥ 99% over 30 days |
| **Security** | Encryption at rest/in transit; least-privilege IAM |
| **Compliance** | SOX-oriented controls; immutable raw zone |
| **Cost** | Lifecycle on raw; tagged `Project=capstone-option-1` |
| **Observability** | Quality reports + CloudWatch when deployed |

---

## 3. Architecture Diagrams

See Mermaid diagrams in [architecture/diagrams/architecture.md](../architecture/diagrams/architecture.md).

### Data Flow

| Stage | Input | Process | Output | Service |
|-------|-------|---------|--------|---------|
| Ingest | CSV/JSON sample or S3 drop | Copy immutable | `raw/...` | Local runner / Lambda |
| Quality | Raw records | RuleEngine | `cleaned/` + `quarantine/` | Local / Glue |
| Curate | Cleaned settlements | Aggregate by date/currency/status | `curated/settlements/` | Local / Glue |
| Audit | Run metrics | Manifest JSON | `metadata/pipeline-runs/` | Local / S3 |

---

## 4. AWS Service Selection

| Layer | Service | Justification | Alternatives Considered |
|-------|---------|---------------|-------------------------|
| Storage | Amazon S3 | Durable lake, cheap retention | EFS (ops + cost) |
| ETL | AWS Glue | Managed Spark, catalog | EMR (ops overhead) |
| Local runner | Python 3 | Offline student path | — |
| Analytics | Amazon Athena | Serverless SQL on curated | Redshift (overkill for lab) |
| Catalog | Glue Data Catalog | Native Athena | Hive metastore |
| Security | IAM + KMS | Standard banking baseline | — |
| Monitoring | CloudWatch + SNS | Job + quality alerts | Third-party APM |

---

## 5. Data Zone Design

| Zone | Purpose | Retention | Format | Consumers |
|------|---------|-----------|--------|-----------|
| **raw/** | Immutable source copies | 7 years (regulatory) | CSV/JSON | ETL only |
| **cleaned/** | Validated records | 24 months | JSON | ETL |
| **curated/** | Settlement summary + enriched sets | 36 months | CSV/Parquet | Analysts, auditors |
| **quarantine/** | Failed validation | 90 days | JSON | Data stewards |
| **metadata/** | Quality + lineage | 7 years | JSON | Compliance |

### S3 Path Conventions

```text
s3://$BUCKET/raw/{dataset}/year=YYYY/month=MM/day=DD/
s3://$BUCKET/cleaned/{dataset}/year=YYYY/month=MM/day=DD/
s3://$BUCKET/curated/{dataset}/year=YYYY/month=MM/day=DD/
s3://$BUCKET/quarantine/{dataset}/year=YYYY/month=MM/day=DD/
s3://$BUCKET/metadata/quality-reports/{dataset}_report.json
s3://$BUCKET/capstone/cnde-cap-banking/...   # optional upload prefix
```

### Curated Model: daily_settlement_summary

| Column | Description |
|--------|-------------|
| settlement_date | Business settlement date |
| currency | ISO currency |
| status | completed / pending / failed / reconciled |
| settlement_count | Count of settlements in bucket |
| gross_amount_sum / net_amount_sum / fee_amount_sum | Aggregates |
| avg_net_amount | Mean net amount |
| processing_date | Pipeline run date |
| report_name | Constant `daily_settlement_summary` |

---

## 6. ETL Design

### Job: `cnde-cap-banking-glue`

| Attribute | Value |
|-----------|-------|
| Trigger | Daily EventBridge / manual lab run |
| Input | `s3://$BUCKET/raw/...` |
| Output | cleaned, quarantine, curated |
| Worker type | G.1X |
| DPU | 2 (lab) |
| Job bookmark | Enabled for incremental days |

### Idempotency

Partition overwrite for `year=/month=/day=` ensures reruns replace the same processing date without duplicates.

---

## 7. Orchestration

```text
Start → Copy raw → Validate each dataset
                 ├─ Pass → Curated transforms → Write curated
                 └─ Fail → Quarantine + quality report
       → Write pipeline-run manifest → Notify success/failure
```

---

## 8. Design Decisions & Trade-offs

### Decision 1: Aggregate at settlement grain

- **Context:** Regulators want daily totals by currency and status, not every transaction line.
- **Decision:** Curate settlements into `daily_settlement_summary`; keep transaction detail separately.
- **Trade-off:** Cross-currency FX conversion deferred to a later semantic layer.

### Decision 2: Quarantine over silent drop

- **Context:** Silent filtering hides operational issues.
- **Decision:** Persist failed rows with rule violation payloads.
- **Trade-off:** Stewards must triage quarantine; storage cost is negligible.

### Decision 3: Reuse course lab stack

- **Context:** Students already deploy Module labs via `lab-cycle.sh`.
- **Decision:** Capstone reuses that bucket/roles; tags `Project=capstone-option-1`.
- **Trade-off:** Shared stack rather than dedicated Terraform module for the course setting.

---

## 9. Future Enhancements

| Enhancement | Priority | Effort |
|-------------|----------|--------|
| Lake Formation column filters on account PII | High | Medium |
| Step Functions orchestration with retries | High | Medium |
| FX normalization table | Medium | Medium |
| Real-time ACH via Kinesis | Low | High |

---

## 10. References

- Course Module 4 – Data Quality Framework (Lab 4.1)
- Course Module 6 – Orchestration patterns
- Capstone rubric – Architecture & Design (25%)
