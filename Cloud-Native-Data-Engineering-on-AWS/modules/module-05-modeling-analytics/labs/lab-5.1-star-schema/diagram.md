# Lab 5.1: Build Star Schema — Architecture Diagram

## Purpose

Create a curated analytics star schema in the Glue Data Catalog with dimension tables (`dim_customer`, `dim_product`) and a partitioned fact table (`fact_orders`). Load data from Module 3 cleaned orders using surrogate keys, validate referential integrity with star joins, and document the S3 curated zone layout aligned with Module 1 data lake zones.

---

## Star Schema (ER Diagram)

```mermaid
erDiagram
    dim_customer ||--o{ fact_orders : "customer_key"
    dim_product  ||--o{ fact_orders : "product_key"

    dim_customer {
        bigint customer_key PK
        string customer_id
        string customer_name
        string email
        string customer_segment
        string acquisition_channel
        string country_code
        date first_order_date
        boolean is_active
        timestamp updated_at
    }

    dim_product {
        bigint product_key PK
        string sku
        string product_name
        string category
        string subcategory
        string brand
        double unit_cost_usd
        double unit_price_usd
        boolean is_active
        timestamp updated_at
    }

    fact_orders {
        bigint order_key PK
        string order_id
        bigint customer_key FK
        bigint product_key FK
        timestamp order_timestamp
        string order_status
        int quantity
        double unit_price_usd
        double discount_amount_usd
        double order_amount_usd
        string currency
        double fulfillment_hours
        string source_system
        string etl_batch_id
        string year "partition"
        string month "partition"
        string day "partition"
    }
```

---

## ETL & Query Architecture

```mermaid
flowchart TB
    subgraph Cleaned["S3 Cleaned Zone (Module 3)"]
        CO["cleaned_retail_orders<br/>Parquet partitioned<br/>year=/month=/day="]
    end

    subgraph Scripts["Athena DDL & Load Scripts"]
        S01["01_create_database.sql"]
        S02["02_create_dim_customer.sql"]
        S03["03_create_dim_product.sql"]
        S04["04_create_fact_orders.sql"]
        S05["05_load_dimensions.sql<br/>CTAS with surrogate keys"]
        S06["06_load_fact_orders.sql<br/>JOIN dims → fact"]
        S07["07_validation_queries.sql"]
    end

    subgraph Curated["S3 Curated Zone (Lab 5.1)"]
        DC["dim_customer/*.parquet"]
        DP["dim_product/*.parquet"]
        FO["fact_orders/year=/month=/day=/*.parquet"]
    end

    subgraph Catalog["Glue Data Catalog"]
        DB["cnde_dev_datalake"]
        ATH["Amazon Athena"]
    end

    CO -->|05_load_dimensions| DC
    CO -->|05_load_dimensions| DP
    CO -->|06_load_fact_orders| FO
    DC --> DB
    DP --> DB
    FO --> DB
    DB --> ATH
    S07 --> ATH
```

---

## Load Sequence

```mermaid
sequenceDiagram
    participant U as Analyst
    participant A as Athena
    participant S3 as S3 Curated
    participant C as cleaned_retail_orders

    U->>A: Run 01–04 DDL scripts
    U->>A: 05_load_dimensions.sql (CTAS)
    A->>C: SELECT DISTINCT customers, products
    A->>S3: Write dim_customer/*.parquet
    A->>S3: Write dim_product/*.parquet
    U->>A: 06_load_fact_orders.sql (CTAS)
    A->>C: JOIN dim_customer, dim_product
    A->>S3: Write fact_orders/year=/month=/day=/
    U->>A: MSCK REPAIR TABLE fact_orders
    U->>A: 07_validation_queries.sql
    A-->>U: 0 orphan rows, revenue by category
```

---

## Key Components

| Component | Type | Role |
|-----------|------|------|
| `cnde_dev_datalake` | Glue Database | Catalog namespace for curated analytics tables |
| `dim_customer` | External table (Parquet) | SCD Type 1 customer dimension with surrogate `customer_key` |
| `dim_product` | External table (Parquet) | Product hierarchy flattened for star joins |
| `fact_orders` | Partitioned external table | Grain: one row per `order_id`; partitioned by year/month/day |
| `cleaned_retail_orders` | Source table (Module 3) | Upstream cleaned Parquet data |
| Athena CTAS | Load mechanism | Creates Parquet files directly in curated S3 prefixes |
| `07_validation_queries.sql` | Validation | Orphan check, category revenue, row count reconciliation |

---

## S3 Paths & Data Flow

| Table | S3 Location | Format | Partitioned |
|-------|-------------|--------|-------------|
| Source | `s3://{bucket}/cleaned/retail/orders/year={Y}/month={M}/day={D}/` | Parquet | Yes |
| `dim_customer` | `s3://{bucket}/curated/retail/dim_customer/` | Parquet (Snappy) | No |
| `dim_product` | `s3://{bucket}/curated/retail/dim_product/` | Parquet (Snappy) | No |
| `fact_orders` | `s3://{bucket}/curated/retail/fact_orders/year={Y}/month={M}/day={D}/` | Parquet (Snappy) | Yes |
| Athena results | `s3://{bucket}/athena-results/` | CSV/Parquet | No |

### Curated Zone Layout

```text
s3://{bucket}/curated/retail/
├── dim_customer/*.parquet
├── dim_product/*.parquet
└── fact_orders/
    └── year=YYYY/month=MM/day=DD/*.parquet
```

### Data Flow Summary

```text
cleaned/retail/orders/ (Module 3)
        │
        ├── CTAS 05_load_dimensions.sql ──► curated/retail/dim_customer/
        │                              └──► curated/retail/dim_product/
        │
        └── CTAS 06_load_fact_orders.sql ──► curated/retail/fact_orders/year=/month=/day=/
                                                    │
                                                    ▼
                                            Athena star joins
                                    (fact_orders ⋈ dim_customer ⋈ dim_product)
```

### Validation Checks

| Check | Query | Expected |
|-------|-------|----------|
| Fact row count | Count vs cleaned partition | Matches (minus cancelled if filtered) |
| Orphan facts | LEFT JOIN dims WHERE key IS NULL | **0 rows** |
| Category revenue | Star join aggregation | Non-empty when data exists |

---

## Related Labs

- **Previous:** Module 4 Data Quality (cleaned data quality gates)
- **Next:** [Lab 5.2 – Athena Query Optimization](../lab-5.2-athena-optimization/diagram.md)
