# Lab 2.1 Architecture — Lambda File Ingestion to S3 Raw Zone

Ingest JSON transaction records into the RetailCo data lake raw zone using a serverless Lambda function with deterministic, idempotent S3 keys.

## Ingestion Pipeline

```mermaid
flowchart LR
    subgraph trigger["Invocation Sources"]
        CLI["AWS CLI<br/>test-event.json"]
        API["Future: API Gateway"]
    end

    subgraph compute["Serverless Compute"]
        L["AWS Lambda<br/>cnde-lab21-file-ingest<br/>handler.py"]
        IAM["IAM Role<br/>cnde-lab21-lambda-ingest"]
        CW["Amazon CloudWatch Logs<br/>/aws/lambda/cnde-lab21-file-ingest"]
    end

    subgraph storage["S3 Data Lake"]
        S3[("cnde-dev-datalake-{account-id}")]
        RAW["raw/lambda-ingest/transactions/<br/>year=YYYY/month=MM/day=DD/<br/>{record_id}.json"]
    end

    CLI -->|Invoke| L
    L --> IAM
    IAM -->|s3:PutObject raw/*| RAW
    L -->|structured logs| CW
    RAW --> S3
```

## Record Ingestion Sequence

```mermaid
sequenceDiagram
    participant User as Developer / CLI
    participant Lambda as Lambda cnde-lab21-file-ingest
    participant S3 as Amazon S3
    participant CW as CloudWatch Logs

    User->>Lambda: Invoke with record_id + data payload
    Lambda->>Lambda: Validate record_id present
    Lambda->>Lambda: Build deterministic S3 key from record_id + date
    Lambda->>S3: PutObject raw/lambda-ingest/transactions/year=.../TXN-1001.json
    Note over S3: Enriched JSON: record_id, payload, source_system, dataset, ingested_at
    Lambda->>CW: Log ingestion_success
    Lambda-->>User: {"ingested": 1, "s3_key": "..."}

    User->>Lambda: Re-invoke same record_id (idempotency test)
    Lambda->>S3: PutObject same key (safe overwrite)
    Note over S3: Single key path — no duplicates
```

## Key Components

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Ingestion Function | AWS Lambda | Validates JSON payload and writes to raw zone with enriched metadata |
| Execution Role | AWS IAM | Least-privilege `s3:PutObject` scoped to `raw/*` prefix only |
| Data Lake Bucket | Amazon S3 | Target storage for ingested transaction records |
| CloudWatch Logs | Amazon CloudWatch | Structured logging for operational troubleshooting |
| Environment Variables | AWS Lambda | Configures bucket, prefix, source system, and dataset name |

## S3 Path Conventions

| Path | Pattern | Example |
|------|---------|---------|
| Raw transactions | `s3://{bucket}/raw/{source}/{dataset}/year={YYYY}/month={MM}/day={DD}/{record_id}.json` | `s3://cnde-dev-datalake-123456789012/raw/lambda-ingest/transactions/year=2024/month=01/day=15/TXN-1001.json` |

### Environment Configuration

| Variable | Value | Purpose |
|----------|-------|---------|
| `DATA_LAKE_BUCKET` | `cnde-dev-datalake-{account-id}` | Target bucket from Lab 1.1 Terraform output |
| `RAW_PREFIX` | `raw/` | Base prefix for raw zone writes |
| `SOURCE_SYSTEM` | `lambda-ingest` | Lineage identifier in output JSON |
| `DATASET` | `transactions` | Dataset name segment in S3 path |

### Idempotency

Re-invoking with the same `record_id` produces the **same S3 key**, resulting in a safe overwrite rather than duplicate objects.
