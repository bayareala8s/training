# Lab 3.2 Architecture — Glue Crawlers and the Data Catalog

Discover and register RetailCo raw and cleaned dataset schemas in the AWS Glue Data Catalog for SQL analytics via Amazon Athena.

## Catalog Discovery Architecture

```mermaid
flowchart TB
    subgraph s3["S3 Data Lake — cnde-dev-datalake-{account-id}"]
        RAW["raw/retail/orders/<br/>year=2024/month=01/day=15/<br/>orders_2024-01-15.csv"]
        CLEAN["cleaned/retail/orders/<br/>year=2024/month=01/day=15/<br/>part-00000.snappy.parquet"]
    end

    subgraph crawlers["AWS Glue Crawlers"]
        RC["Raw Crawler<br/>cnde_dev_datalake-raw-crawler"]
        CC["Cleaned Crawler<br/>cnde_dev_datalake-cleaned-crawler"]
    end

    subgraph catalog["AWS Glue Data Catalog"]
        DB["Database<br/>cnde_dev_datalake"]
        TR["Table: raw_retail_orders<br/>Format: CSV, types: string"]
        TC["Table: cleaned_retail_orders<br/>Format: Parquet, typed schema"]
    end

    subgraph analytics["Query Layer"]
        ATH["Amazon Athena"]
        RES["s3://{bucket}/athena-results/"]
    end

    RAW --> RC
    CLEAN --> CC
    RC -->|schema inference| TR
    CC -->|schema inference + partitions| TC
    TR --> DB
    TC --> DB
    DB --> ATH
    ATH -->|query results| RES
```

## Crawler Run Sequence

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Crawler as Glue Crawler
    participant S3 as Amazon S3
    participant Catalog as Glue Data Catalog
    participant Athena as Amazon Athena

    Dev->>Crawler: start-crawler (cleaned)
    Crawler->>S3: Scan cleaned/retail/orders/ prefix
    Crawler->>Crawler: Infer Parquet schema + Hive partitions
    Crawler->>Catalog: Register cleaned_retail_orders table
    Note over Catalog: Columns: order_id, total_amount, order_status, year, month, day

    Dev->>Crawler: start-crawler (raw)
    Crawler->>S3: Scan raw/retail/orders/ prefix
    Crawler->>Catalog: Register raw_retail_orders table
    Note over Catalog: CSV columns inferred as string types

    Dev->>Athena: SELECT ... WHERE year='2024' AND month='01'
    Athena->>Catalog: Resolve table schema + partitions
    Athena->>S3: Read only matching partition files
    Athena-->>Dev: Query results (partition pruning)
```

## Schema Evolution Flow

```mermaid
flowchart LR
    NEW["New raw CSV with<br/>promotional_code column"]
    RC2["Re-run Raw Crawler"]
    CAT["Catalog updates<br/>raw_retail_orders schema"]
    ETL["Glue ETL Job<br/>unchanged contract"]
    CLEAN2["cleaned_retail_orders<br/>no promotional_code"]

    NEW --> RC2 --> CAT
    CAT -.->|"column visible in catalog"| ETL
    ETL --> CLEAN2
    Note1["Governance: ETL contract<br/>controls cleaned schema"]
```

## Key Components

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Raw Crawler | AWS Glue Crawler | Discovers CSV schema and Hive partitions in `raw/retail/orders/` |
| Cleaned Crawler | AWS Glue Crawler | Registers typed Parquet schema from `cleaned/retail/orders/` |
| Data Catalog Database | AWS Glue Data Catalog | Central metadata repository (`cnde_dev_datalake`) |
| Catalog Tables | AWS Glue Data Catalog | `raw_retail_orders` and `cleaned_retail_orders` table definitions |
| Athena | Amazon Athena | Serverless SQL queries against cataloged tables |
| Query Results | Amazon S3 | Athena output stored at `athena-results/` prefix |
| Glue IAM Role | AWS IAM | Crawler execution role with S3 read and catalog write permissions |

## S3 Path Conventions

| Target | Crawler S3 Path | Catalog Table |
|--------|-----------------|---------------|
| Raw orders | `s3://{bucket}/raw/retail/orders/` | `cnde_dev_datalake.raw_retail_orders` |
| Cleaned orders | `s3://{bucket}/cleaned/retail/orders/` | `cnde_dev_datalake.cleaned_retail_orders` |
| Athena results | `s3://{bucket}/athena-results/` | N/A (query output only) |

### Crawler Configuration

| Setting | Recommended Value | Purpose |
|---------|-------------------|---------|
| Recrawl policy | `CRAWL_NEW_FOLDERS_ONLY` | Avoid re-scanning unchanged partitions |
| Schema update | `UPDATE_IN_DATABASE` | Reflect new columns in catalog |
| Schema delete | `LOG` | Never silently delete columns in production |
| Table prefix | `raw_` / `cleaned_` | Consistent naming across zones |

### Example Athena Query

```sql
SELECT order_status, COUNT(*) AS order_count, SUM(total_amount) AS revenue
FROM cnde_dev_datalake.cleaned_retail_orders
WHERE year = '2024' AND month = '01' AND day = '15'
GROUP BY order_status;
```
