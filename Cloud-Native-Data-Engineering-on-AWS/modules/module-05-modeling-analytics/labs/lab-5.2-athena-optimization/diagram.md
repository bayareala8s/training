# Lab 5.2: Athena Query Optimization — Architecture Diagram

## Purpose

Measure and reduce **data scanned** by comparing intentionally inefficient queries against optimized alternatives on the Lab 5.1 star schema. Apply partition pruning, column projection, and filter-pushdown patterns; use EXPLAIN and `$partitions` metadata to verify optimization; and document before/after cost and performance improvements for RetailCo analysts.

---

## Optimization Architecture

```mermaid
flowchart LR
    subgraph Before["Before — High Scan Patterns"]
        B1["B1: No partition filter<br/>Full table scan"]
        B2["B2: SELECT *<br/>All columns read"]
        B3["B3: CAST on partition cols<br/>Pruning broken"]
        B4["B4: Join before filter<br/>Large intermediate set"]
    end

    subgraph Athena["Amazon Athena Engine v3"]
        SCAN["Data Scanned Metric<br/>Query execution stats"]
        EXPLAIN["EXPLAIN plan analysis"]
    end

    subgraph After["After — Optimized Patterns"]
        A1["A1: year/month/day literals<br/>Partition pruning"]
        A2["A2: Explicit column list<br/>Column projection"]
        A3["A3: IN list on day<br/>No CAST on partitions"]
        A4["A4: Filtered subquery<br/>Then join dims"]
    end

    B1 --> SCAN
    B2 --> SCAN
    B3 --> SCAN
    B4 --> SCAN
    A1 --> SCAN
    A2 --> SCAN
    A3 --> SCAN
    A4 --> SCAN
    A1 --> EXPLAIN
    A3 --> EXPLAIN
```

---

## Query Optimization Flow

```mermaid
flowchart TB
    subgraph Source["Curated Tables (Lab 5.1)"]
        FO["fact_orders<br/>PARTITIONED BY year, month, day"]
        DC["dim_customer"]
        DP["dim_product"]
    end

    subgraph AntiPatterns["Anti-Patterns (before_queries.sql)"]
        AP1["Scan all partitions"]
        AP2["Read unused columns"]
        AP3["year = CAST('2024' AS VARCHAR)"]
        AP4["JOIN dims on full fact table"]
    end

    subgraph BestPractices["Best Practices (after_queries.sql)"]
        BP1["year='2024' AND month='01' AND day='15'"]
        BP2["SELECT order_id, order_amount_usd, ..."]
        BP3["day IN ('01','02',...,'15')"]
        BP4["WITH filtered AS (SELECT ... WHERE partition)"]
    end

    FO --> AntiPatterns
    FO --> BestPractices
    DC --> AntiPatterns
    DP --> AntiPatterns
    DC --> BestPractices
    DP --> BestPractices

    AntiPatterns --> METRICS["Record: bytes scanned, runtime"]
    BestPractices --> METRICS
    METRICS --> REPORT["LAB-REPORT.md<br/>Scan reduction %"]
```

---

## Partition Pruning Sequence

```mermaid
sequenceDiagram
    participant A as Analyst
    participant ATH as Athena
    participant S3 as S3 Partitions
    participant META as $partitions view

    A->>ATH: Run B1 (no partition filter)
    ATH->>S3: Scan ALL fact_orders partitions
    ATH-->>A: High data scanned

    A->>ATH: Run A1 (year/month/day filter)
    ATH->>S3: Scan SINGLE partition only
    ATH-->>A: Low data scanned

    A->>META: SELECT year, month, day FROM $partitions
    META-->>A: Partition inventory
    A->>S3: aws s3 ls curated/retail/fact_orders/
    Note over A,S3: Verify catalog matches S3 folders
```

---

## Key Components

| Component | Location | Role |
|-----------|----------|------|
| `before_queries.sql` | `scripts/` | B1–B4 intentionally inefficient baseline queries |
| `after_queries.sql` | `scripts/` | A1–A4 optimized counterparts |
| `explain_checks.sql` | `scripts/` | EXPLAIN plans to verify partition filters |
| `fact_orders` | Glue Catalog | Primary optimization target (partitioned Parquet) |
| `dim_customer`, `dim_product` | Glue Catalog | Join targets; filter facts before joining |
| `$partitions` | Athena metadata | Inventory of registered Hive partitions |
| Athena workgroup | Console | Engine v3; displays Data Scanned per query |

---

## S3 Paths & Data Flow

| Resource | S3 Path | Relevance to Optimization |
|----------|---------|----------------------------|
| Fact table | `s3://{bucket}/curated/retail/fact_orders/year={Y}/month={M}/day={D}/` | Partition pruning targets specific prefixes |
| Dimensions | `s3://{bucket}/curated/retail/dim_customer/` | Small; full scan acceptable |
| Dimensions | `s3://{bucket}/curated/retail/dim_product/` | Small; full scan acceptable |
| Query results | `s3://{bucket}/athena-results/` | Athena output staging |

### Query Pair Reference

| Pair | Before (Anti-Pattern) | After (Optimization) | Expected Reduction |
|------|----------------------|------------------------|-------------------|
| B1 → A1 | No partition filter | Single-day partition literals | ≥ 80% (multi-partition) |
| B2 → A2 | `SELECT *` | Explicit column list | Proportional to column count |
| B3 → A3 | `CAST()` on partition column | `IN` list on `day` | Restores pruning |
| B4 → A4 | Join then filter | Filtered subquery then join | Smaller join input |

### Cost Calculation

```text
Scan reduction % = (1 - after_scan / before_scan) × 100
Estimated savings  = (before_scan - after_scan) / 1 TB × $5.00  (us-east-1 illustrative)
```

### Partition Verification

```sql
-- Catalog inventory
SELECT year, month, day, COUNT(*) AS partition_count
FROM "cnde_dev_datalake$partitions"
WHERE tablename = 'fact_orders'
GROUP BY year, month, day;

-- S3 verification
aws s3 ls s3://{bucket}/curated/retail/fact_orders/ --recursive | grep PRE
```

### Data Flow (Read Path)

```text
Analyst query
      │
      ├── Partition filter present? ──YES──► Scan only matching S3 prefixes
      │                                    (year=/month=/day=/)
      │
      └── No filter / CAST on partition ──► Full table scan (all partitions)
```

---

## Related Labs

- **Previous:** [Lab 5.1 – Star Schema](../lab-5.1-star-schema/diagram.md)
- **Next:** [Lab 5.3 – Cost-Efficient Queries](../lab-5.3-cost-efficient-queries/diagram.md)
