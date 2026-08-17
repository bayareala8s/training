# Architecture Diagrams – Option 4 Enterprise Data Platform

**Project:** `cnde-cap-enterprise`

## Context (full platform)

```mermaid
flowchart LR
  subgraph Sources
    RET[Retail OMS]
    WMS[Warehouse / Inventory]
    VND[Vendor API feeds]
  end

  subgraph Platform["cnde-cap-enterprise"]
    ING[Multi-ingest<br/>file + API + events]
    LAKE[(Medallion Lake<br/>raw→cleaned→curated)]
    QUAL[Quality + Quarantine]
    ORCH[Step Functions<br/>daily_etl.asl.json]
    GLUE[Glue curated job]
    FEAT[ML features zone]
    MON[CloudWatch + SNS]
  end

  BI[BI / Athena]
  ML[Optional SageMaker / Feature consumers]
  STEW[Data Stewards]

  RET --> ING
  WMS --> ING
  VND --> ING
  ING --> LAKE
  ORCH --> ING
  ORCH --> QUAL
  ORCH --> GLUE
  QUAL --> LAKE
  QUAL --> STEW
  GLUE --> LAKE
  GLUE --> FEAT
  LAKE --> BI
  FEAT --> ML
  ORCH --> MON
  GLUE --> MON
```

## Medallion + orchestration

```mermaid
flowchart TB
  SF[Step Functions: IngestRawZones]
  SF --> P{Parallel ingest}
  P --> O[orders CSV]
  P --> I[inventory CSV]
  P --> V[vendor_feeds JSON]
  O --> RAW[(raw/)]
  I --> RAW
  V --> RAW
  RAW --> Q[ValidateQuality]
  Q --> GATE{pass_rate ≥ 85%?}
  GATE -->|yes| G[Glue: KPI + features]
  GATE -->|no| SNS[SNS quarantine alert]
  SNS --> G
  G --> KPI[curated/enterprise_kpi_daily]
  G --> CF[curated/customer_order_features]
  G --> OK[PublishSuccess]
  G -->|error| FAIL[PipelineFailed]
```

## Module coverage map

```mermaid
mindmap
  root((Option 4 Platform))
    M1 Lake zones
      raw cleaned curated quarantine metadata
    M2 Ingestion
      batch files vendor JSON events
    M3 Glue ETL
      glue_job.py Parquet
    M4 Quality
      RuleEngine quarantine reports
    M5 Catalog
      Athena tables on curated
    M6 Orchestration
      daily_etl.asl.json
    M7 Security
      IAM KMS tagging
    M8 Monitoring
      dashboard_widgets.json
    M9 ML data
      customer_order_features
```

## Data products

```mermaid
erDiagram
  ORDERS_CLEANED ||--o{ CUSTOMER_ORDER_FEATURES : aggregates
  INVENTORY_CLEANED ||--o| ENTERPRISE_KPI_DAILY : feeds
  ORDERS_CLEANED ||--o| ENTERPRISE_KPI_DAILY : feeds
  VENDOR_FEEDS_CLEANED ||--o{ VENDOR_QUALITY : summarizes
  CUSTOMER_ORDER_FEATURES {
    string customer_id
    float gmv_30d
    float avg_order_value
    float cancel_rate
  }
  ENTERPRISE_KPI_DAILY {
    date kpi_date
    int sku_count
    float fill_rate_pct
    int order_count
    float gmv
  }
```
