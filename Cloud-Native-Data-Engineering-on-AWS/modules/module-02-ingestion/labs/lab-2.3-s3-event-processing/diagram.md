# Lab 2.3 Architecture — S3 Event Processing with Lambda

Promote uploaded files from a landing zone to partitioned raw paths using S3 event notifications, with invalid files routed to quarantine.

## Event-Driven Promotion Pipeline

```mermaid
flowchart TB
    subgraph upload["File Upload"]
        U["Developer / Partner<br/>Upload CSV to incoming/"]
    end

    subgraph bucket["S3 Data Lake — cnde-dev-datalake-{account-id}"]
        INC["incoming/transactions/<br/>batch_2024-01-15.csv"]
        RAW["raw/file-upload/transactions/<br/>year=2024/month=01/day=15/<br/>batch_2024-01-15.csv"]
        QUAR["quarantine/file-upload/transactions/<br/>malware.exe.error.json"]
    end

    subgraph events["Event Processing"]
        NOTIF["S3 Event Notification<br/>s3:ObjectCreated:*<br/>prefix: incoming/"]
        L["AWS Lambda<br/>cnde-lab23-s3-event<br/>s3_event_handler.py"]
        CW["Amazon CloudWatch Logs"]
    end

    U --> INC
    INC -->|ObjectCreated| NOTIF
    NOTIF -->|Invoke| L
    L -->|valid CSV| RAW
    L -->|invalid file| QUAR
    L -->|promotion_success / quarantined| CW
```

## File Processing Sequence

```mermaid
sequenceDiagram
    participant User as Uploader
    participant S3 as Amazon S3
    participant Notif as S3 Event Notification
    participant Lambda as Lambda cnde-lab23-s3-event
    participant CW as CloudWatch Logs

    User->>S3: PutObject incoming/transactions/batch_2024-01-15.csv
    S3->>Notif: s3:ObjectCreated event
    Notif->>Lambda: Invoke with bucket + key
    Lambda->>S3: GetObject incoming/transactions/batch_2024-01-15.csv
    Lambda->>Lambda: Validate extension, size, format
    alt Valid CSV
        Lambda->>S3: Copy to raw/file-upload/transactions/year=2024/month=01/day=15/
        Lambda->>CW: Log promotion_success
    else Invalid file
        Lambda->>S3: PutObject quarantine/.../filename.error.json
        Lambda->>CW: Log quarantined with reason
    end
```

## Validation Decision Flow

```mermaid
flowchart TD
    START([S3 ObjectCreated<br/>incoming/*]) --> READ[Read object metadata]
    READ --> EXT{Valid extension?<br/>.csv allowed}
    EXT -->|No| QUAR[Write error manifest<br/>to quarantine/]
    EXT -->|Yes| SIZE{Within size limit?<br/>MAX_FILE_BYTES}
    SIZE -->|No| QUAR
    SIZE -->|Yes| PROMOTE[Copy to partitioned raw path<br/>year=/month=/day=]
    PROMOTE --> DONE([promotion_success])
    QUAR --> FAIL([quarantined])
```

## Key Components

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Landing Prefix | Amazon S3 (`incoming/`) | Staging area for partner file uploads before validation |
| Event Notification | Amazon S3 | Triggers Lambda on `s3:ObjectCreated:*` for `incoming/` prefix |
| Event Handler | AWS Lambda | Validates files and promotes to raw or quarantine zones |
| Raw Zone | Amazon S3 | Partitioned storage for validated transaction CSV files |
| Quarantine Zone | Amazon S3 | Isolated storage with JSON error manifests for rejected files |
| Execution Role | AWS IAM | `GetObject` on incoming, `PutObject` on raw and quarantine |
| CloudWatch Logs | Amazon CloudWatch | Audit trail for promotions and quarantine decisions |

## S3 Path Conventions

| Zone | Path Pattern | Example |
|------|--------------|---------|
| Incoming (landing) | `s3://{bucket}/incoming/{dataset}/{filename}` | `s3://cnde-dev-datalake-123456789012/incoming/transactions/batch_2024-01-15.csv` |
| Raw (promoted) | `s3://{bucket}/raw/{source}/{dataset}/year={YYYY}/month={MM}/day={DD}/{filename}` | `s3://cnde-dev-datalake-123456789012/raw/file-upload/transactions/year=2024/month=01/day=15/batch_2024-01-15.csv` |
| Quarantine | `s3://{bucket}/quarantine/{source}/{dataset}/{filename}.error.json` | `s3://cnde-dev-datalake-123456789012/quarantine/file-upload/transactions/malware.exe.error.json` |

### Environment Configuration

| Variable | Value | Purpose |
|----------|-------|---------|
| `INCOMING_PREFIX` | `incoming/` | S3 event filter prefix |
| `SOURCE_SYSTEM` | `file-upload` | Lineage identifier in raw path |
| `DATASET` | `transactions` | Dataset segment in all paths |
| `MAX_FILE_BYTES` | `10485760` | 10 MB upload size limit |

### Idempotency

Re-uploading the same file to the same incoming key triggers a new event but produces the **same deterministic raw key** (overwrite, not duplicate).
