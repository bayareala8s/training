# Architecture Diagrams – Banking Regulatory Data Platform

Project: `cnde-cap-banking` · Capstone Option 1

---

## Context

```mermaid
flowchart LR
  subgraph Sources
    CBS[Core Banking Extracts]
    CLR[Clearing House Files]
  end

  subgraph Platform["cnde-cap-banking Data Platform"]
    ING[Ingestion / sample-data]
    LAKE[S3 Medallion Lake]
    DQ[RuleEngine Quality]
    ETL[Curated Transforms / Glue]
    META[Audit Metadata]
  end

  subgraph Consumers
    CMP[Compliance Analysts]
    FIN[Finance]
    STW[Data Stewards]
  end

  CBS --> ING
  CLR --> ING
  ING --> LAKE
  LAKE --> DQ
  DQ -->|passed| ETL
  DQ -->|failed| STW
  ETL --> LAKE
  ETL --> META
  LAKE --> CMP
  LAKE --> FIN
  META --> CMP
```

---

## Component / Medallion Flow

```mermaid
flowchart TB
  RAW["raw/\ntransactions · settlements · accounts"]
  QE["validators.RuleEngine\nnot_null · range · enum · regex"]
  CLN["cleaned/"]
  QUA["quarantine/"]
  CUR_T["curated/transactions\nenriched audit rows"]
  CUR_S["curated/settlements\ndaily_settlement_summary"]
  CUR_A["curated/accounts\ncompliance snapshot"]
  REP["metadata/quality-reports\n+ pipeline-runs"]

  RAW --> QE
  QE -->|pass| CLN
  QE -->|fail| QUA
  CLN --> CUR_T
  CLN --> CUR_S
  CLN --> CUR_A
  QE --> REP
```

---

## Settlement Aggregation

```mermaid
flowchart LR
  S[Cleaned settlements] --> G["GROUP BY\nsettlement_date, currency, status"]
  G --> A["SUM gross/net/fee\nCOUNT settlements\nAVG net"]
  A --> R["daily_settlement_summary CSV"]
```

---

## Security Boundaries

```mermaid
flowchart TB
  subgraph IAM
    R1[ingestion-role → raw Put]
    R2[glue-etl-role → all zones R/W]
    R3[compliance-role → curated Get]
    R4[steward-role → quarantine Get]
  end

  subgraph Controls
    E[SSE-S3 / KMS]
    T[TLS only]
    G[Block Public Access]
    TAG["Tags Project=capstone-option-1"]
  end

  R1 --> E
  R2 --> E
  R3 --> E
  R4 --> E
  E --> T
  T --> G
  G --> TAG
```
