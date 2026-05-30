# Lab 2.2 Architecture — EventBridge Scheduled API Ingestion

Automate recurring pull-based ingestion from an external API into the RetailCo raw zone using EventBridge schedules, Lambda, and metadata watermarks.

## Scheduled Ingestion Pipeline

```mermaid
flowchart TB
    subgraph schedule["Scheduling"]
        EB["Amazon EventBridge<br/>cnde-lab22-ingest-schedule<br/>rate(15 minutes)"]
    end

    subgraph compute["Serverless Compute"]
        L["AWS Lambda<br/>cnde-lab22-scheduled-ingest<br/>scheduled_ingestion.py"]
        IAM["IAM Role<br/>cnde-lab22-scheduled-ingest"]
        CW["Amazon CloudWatch Logs"]
    end

    subgraph external["External Source"]
        API["JSONPlaceholder API<br/>/posts endpoint"]
    end

    subgraph lake["S3 Data Lake — cnde-dev-datalake-{account-id}"]
        RAW["raw/api-ingest/posts/<br/>year=YYYY/month=MM/day=DD/<br/>snapshot_{timestamp}.json"]
        WM["metadata/watermarks/<br/>api-ingest/posts.json"]
    end

    EB -->|Invoke| L
    L --> IAM
    L -->|HTTPS GET| API
    API -->|100 posts JSON| L
    L -->|PutObject snapshot| RAW
    L -->|GetObject + PutObject| WM
    L -->|scheduled_ingestion_complete| CW
```

## Scheduled Run Sequence

```mermaid
sequenceDiagram
    participant EB as EventBridge Rule
    participant Lambda as Lambda cnde-lab22-scheduled-ingest
    participant API as JSONPlaceholder API
    participant S3 as Amazon S3
    participant CW as CloudWatch Logs

    EB->>Lambda: Trigger every 15 minutes
    Lambda->>S3: GetObject metadata/watermarks/api-ingest/posts.json
    Note over S3: Read last_successful_run, last_snapshot_key
    Lambda->>API: GET https://jsonplaceholder.typicode.com/posts
    API-->>Lambda: JSON array (100 records)
    Lambda->>S3: PutObject raw/api-ingest/posts/year=.../snapshot_{ts}.json
    Lambda->>S3: PutObject watermark (overwrite)
    Note over S3: Update last_successful_run, records_ingested
    Lambda->>CW: Log scheduled_ingestion_complete
```

## Key Components

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Schedule Rule | Amazon EventBridge | Triggers ingestion every 15 minutes via `rate(15 minutes)` |
| Ingestion Function | AWS Lambda | Fetches API data and writes time-stamped snapshots to raw zone |
| Execution Role | AWS IAM | Read/write access to `raw/*` and `metadata/*` prefixes |
| External API | JSONPlaceholder | Simulated RetailCo upstream data source |
| Watermark File | Amazon S3 (metadata zone) | Tracks last successful run and snapshot location |
| CloudWatch Logs | Amazon CloudWatch | Monitors scheduled execution and record counts |

## S3 Path Conventions

| Path | Pattern | Example |
|------|---------|---------|
| API snapshots | `s3://{bucket}/raw/{source}/{dataset}/year={YYYY}/month={MM}/day={DD}/snapshot_{timestamp}.json` | `s3://cnde-dev-datalake-123456789012/raw/api-ingest/posts/year=2024/month=01/day=15/snapshot_20240115T143000Z.json` |
| Watermark | `s3://{bucket}/metadata/watermarks/{source}/{dataset}.json` | `s3://cnde-dev-datalake-123456789012/metadata/watermarks/api-ingest/posts.json` |

### Watermark Schema

| Field | Purpose |
|-------|---------|
| `last_successful_run` | ISO timestamp of most recent successful ingestion |
| `last_snapshot_key` | S3 key of the latest snapshot file |
| `records_ingested` | Count of records in the last snapshot |

### Environment Configuration

| Variable | Value |
|----------|-------|
| `SOURCE_SYSTEM` | `api-ingest` |
| `DATASET` | `posts` |
| `API_URL` | `https://jsonplaceholder.typicode.com/posts` |
| `WATERMARK_KEY` | `metadata/watermarks/api-ingest/posts.json` |
