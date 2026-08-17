# Lab 4.2: Validation Automation in ETL Pipelines — Architecture Diagram

## Purpose

Integrate the Lab 4.1 validation framework into production AWS pipelines at two stages: lightweight **Lambda** validation at ingestion time and **Glue ETL** batch validation at scale. Publish quality metrics to **CloudWatch**, trigger **SNS** alerts when pass rate falls below the 99.9% SLO, and store versioned rules in S3 for decoupled policy management.

---

## Architecture Overview

```mermaid
flowchart TB
    subgraph Triggers["Event Sources"]
        EB["EventBridge Schedule"]
        S3E["S3 Event Notification"]
    end

    subgraph Compute["Validation Compute"]
        LAMB["Lambda: cnde-dev-order-validation<br/>handler.py + validators.py"]
        GLUE["Glue ETL: orders_quality_etl.py<br/>Spark batch validation"]
    end

    subgraph Rules["Shared Rule Engine (Lab 4.1)"]
        RE["RuleEngine"]
        RULES["s3://{bucket}/metadata/rules/retail/orders_rules.json"]
    end

    EB --> LAMB
    S3E --> LAMB
    RULES --> LAMB
    RULES --> GLUE
    RE --> LAMB
    RE --> GLUE

    subgraph Zones["S3 Data Lake Zones"]
        RAW["raw/retail/orders/<br/>year=/month=/day=/lambda-{request_id}/passed.json"]
        CLEAN["cleaned/retail/orders/<br/>year=/month=/day=/*.parquet"]
        QUAR["quarantine/retail/orders/<br/>year=/month=/day=/failed.json"]
        META["metadata/quality-reports/"]
        SCRIPTS["scripts/orders_quality_etl.py<br/>scripts/validators.py"]
    end

    LAMB -->|passed| RAW
    LAMB -->|failed| QUAR
    GLUE -->|read| RAW
    GLUE -->|passed| CLEAN
    GLUE -->|failed| QUAR
    SCRIPTS -.-> GLUE

    subgraph Observability["Observability & Alerting"]
        CW["CloudWatch<br/>Namespace: CNDE/DataQuality"]
        ALM["CloudWatch Alarm<br/>PassRate < 99.9%"]
        SNS["SNS: cnde-data-quality-alerts"]
    end

    LAMB -->|PutMetricData| CW
    GLUE -->|PutMetricData| CW
    CW --> ALM
    ALM --> SNS
    SNS --> EMAIL["Email subscription"]
```

---

## Lambda Ingestion Sequence

```mermaid
sequenceDiagram
    participant EVT as Event / API
    participant L as Lambda handler
    participant RE as RuleEngine
    participant S3 as S3 Data Lake
    participant CW as CloudWatch

    EVT->>L: records[] payload
    L->>RE: validate_batch(records)
    RE-->>L: passed[] + quarantined[]
    alt passed records exist
        L->>S3: PutObject raw/retail/orders/.../passed.json
    end
    alt quarantined records exist
        L->>S3: PutObject quarantine/retail/orders/.../failed.json
    end
    L->>CW: RecordsProcessed, RecordsQuarantined, PassRate
    L-->>EVT: {pass_rate_pct, within_slo}
```

---

## Glue Batch Validation Sequence

```mermaid
sequenceDiagram
    participant SF as Step Functions / Scheduler
    participant G as Glue Job
    participant S3 as S3
    participant RE as RuleEngine

    SF->>G: StartJobRun (INPUT_DATE, RULES_S3_PATH)
    G->>S3: Download metadata/rules/retail/orders_rules.json
    G->>S3: Read raw/retail/orders/year=/month=/day=/
    G->>RE: validate_record() per row
    G->>S3: Write cleaned/.../*.parquet (passed)
    G->>S3: Write quarantine/.../*.json (failed + _violations)
    G-->>SF: Job SUCCEEDED
```

---

## Key Components

| Component | Service | Role |
|-----------|---------|------|
| `cnde-dev-order-validation` | Lambda | Ingestion-time validation; writes raw/quarantine; publishes metrics |
| `orders_quality_etl.py` | Glue | Batch read raw CSV → validate → write Parquet cleaned + JSON quarantine |
| `validators.py` | Shared library | Lab 4.1 RuleEngine reused in Lambda zip and Glue Python path |
| `orders_rules.json` | S3 metadata | Versioned declarative rules; updatable without code redeploy |
| `CNDE/DataQuality` | CloudWatch | Custom namespace: `RecordsProcessed`, `RecordsQuarantined`, `PassRate` |
| `cnde-orders-pass-rate-below-slo` | CloudWatch Alarm | Fires when `PassRate` < 99.9% for `Dataset=retail/orders` |
| `cnde-data-quality-alerts` | SNS | Email/Slack notification on SLO breach |

---

## S3 Paths & Data Flow

| Zone | S3 Path Pattern | Written By | Format |
|------|-----------------|------------|--------|
| Raw (passed) | `s3://{bucket}/raw/retail/orders/year={Y}/month={M}/day={D}/lambda-{request_id}/passed.json` | Lambda | JSON |
| Cleaned | `s3://{bucket}/cleaned/retail/orders/year={Y}/month={M}/day={D}/` | Glue | Parquet |
| Quarantine (Lambda) | `s3://{bucket}/quarantine/retail/orders/year={Y}/month={M}/day={D}/lambda-{request_id}/failed.json` | Lambda | JSON |
| Quarantine (Glue) | `s3://{bucket}/quarantine/retail/orders/year={Y}/month={M}/day={D}/glue-run-{HHMMSS}/` | Glue | JSON |
| Rules | `s3://{bucket}/metadata/rules/retail/orders_rules.json` | Manual upload | JSON |
| Inventory rules | `s3://{bucket}/metadata/rules/retail/inventory_rules.json` | Example | JSON |
| Glue scripts | `s3://{bucket}/scripts/orders_quality_etl.py` | Deploy | Python |

### End-to-End Data Flow

```text
EventBridge / S3 Event
        │
        ├──► Lambda ──► RuleEngine ──┬──► raw/retail/orders/ (passed)
        │                            └──► quarantine/retail/orders/ (failed)
        │
        └──► Glue ETL ──► RuleEngine ──┬──► cleaned/retail/orders/ (Parquet)
                                       └──► quarantine/retail/orders/ (JSON)

Both paths ──► CloudWatch metrics ──► Alarm (PassRate < 99.9%) ──► SNS
```

### CloudWatch Metric Dimensions

| Metric | Unit | Dimension | SLO |
|--------|------|-----------|-----|
| `RecordsProcessed` | Count | `Dataset=retail/orders` | — |
| `RecordsQuarantined` | Count | `Dataset=retail/orders` | — |
| `PassRate` | Percent | `Dataset=retail/orders` | ≥ 99.9% |

---

## Related Labs

- **Previous:** [Lab 4.1 – Quality Framework](../lab-4.1-quality-framework/diagram.md)
- **Next:** [Lab 4.3 – Quarantine Zone](../lab-4.3-quarantine-zone/diagram.md)
