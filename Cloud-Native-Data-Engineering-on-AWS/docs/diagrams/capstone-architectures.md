# Capstone Architecture Options

Reference architecture diagrams for the four Module 10 capstone scenarios. Each option extends the course platform (Modules 1–9) with scenario-specific sources, compliance controls, and consumers.

---

## Shared Platform Foundation

All capstone options build on the same cloud-native patterns taught in this course:

```mermaid
flowchart TB
    subgraph Ingest["Ingestion Layer"]
        SRC[External Sources]
        LAMB[Lambda Ingestion]
        EB[EventBridge]
    end

    subgraph Lake["S3 Medallion Lake"]
        RAW[(raw/)]
        CLN[(cleaned/)]
        CUR[(curated/)]
        QUA[(quarantine/)]
    end

    subgraph Process["Processing & Orchestration"]
        GLUE[AWS Glue ETL]
        SF[Step Functions]
        DQ[Data Quality Framework]
    end

    subgraph Analytics["Analytics & ML"]
        GC[Glue Data Catalog]
        ATH[Amazon Athena]
        ML[ml/ training & features]
    end

    subgraph Ops["Security & Operations"]
        KMS[AWS KMS]
        IAM[IAM / RBAC]
        CW[CloudWatch + SNS]
        CE[Cost Explorer + Budgets]
    end

    SRC --> LAMB --> RAW
    EB --> LAMB
    RAW --> GLUE --> CLN --> GLUE --> CUR
    CLN --> DQ
    DQ -->|fail| QUA
    CUR --> GC --> ATH
    CUR --> ML

    KMS & IAM --> Lake
    GLUE & LAMB & SF --> CW
    Lake & GLUE --> CE
```

---

## Option 1: Banking Regulatory Data Platform

Build a reporting platform for financial settlement and transaction data with audit trails, lineage, and strict access controls for regulatory submissions.

### Architecture Diagram

```mermaid
flowchart TB
    subgraph Sources["Financial Sources"]
        CORE[Core Banking API]
        SWIFT[SWIFT / Settlement Files]
        LEDGER[General Ledger Exports]
    end

    subgraph Ingest["Secure Ingestion"]
        LAMB[Lambda Ingestion<br/>checksum validation]
        SM[Secrets Manager<br/>API credentials]
    end

    subgraph Lake["Regulatory Data Lake"]
        RAW[(raw/settlements/<br/>raw/transactions/)]
        CLN[(cleaned/)]
        CUR[(curated/regulatory/<br/>daily_settlement_report/)]
        META[(metadata/lineage/)]
    end

    subgraph Controls["Compliance Controls"]
        KMS[AWS KMS SSE-KMS]
        IAM[IAM RBAC<br/>no analyst raw access]
        CT[CloudTrail + S3 access logs]
        AUD[Audit Report<br/>GOVERNANCE.md]
    end

    subgraph Consumers["Regulatory Consumers"]
        REG[Compliance Officers]
        ATH[Athena SQL Reports]
        EXP[Regulatory Export<br/>Parquet / CSV]
    end

    CORE & SWIFT & LEDGER --> LAMB
    SM --> LAMB
    LAMB --> RAW
    RAW --> GLUE[Glue ETL] --> CLN --> CUR
    CUR --> ATH --> EXP
    CUR --> META
    KMS & IAM & CT --> Lake
    ATH --> REG
    AUD --> REG
```

### Key Components

| Component | Purpose |
|-----------|---------|
| Multi-source ingestion | Settlement files, transaction logs, account summaries |
| Immutable raw zone | Audit-ready source copies with versioning |
| Lineage metadata | `metadata/lineage/` documents transform provenance |
| Encryption + RBAC | KMS + zone-based IAM from Module 7 |
| Regulatory curated models | Daily settlement reports, transaction aggregates |
| Audit trail | CloudTrail + governance audit from Lab 7.3 |

### Data Flows

| Stage | Input | Process | Output |
|-------|-------|---------|--------|
| Ingest | Settlement CSV/API | Validate checksum, timestamp | `raw/settlements/` |
| Clean | Raw transactions | Type coercion, dedup | `cleaned/finance/` |
| Curate | Cleaned data | Regulatory aggregations | `curated/regulatory/daily_settlement_report/` |
| Report | Curated tables | Athena SQL + export | Compliance-ready dataset |
| Audit | All layers | CloudTrail + governance checks | Quarterly audit report |

---

## Option 2: Healthcare Analytics Platform

HIPAA-aware patient analytics with PII masking, strict governance, and operational reporting on synthetic clinical data.

### Architecture Diagram

```mermaid
flowchart TB
    subgraph Sources["Clinical Sources (Synthetic)"]
        EHR[EHR Exports]
        APPT[Appointment Records]
        LAB[Lab Results]
    end

    subgraph Ingest["HIPAA-Aware Ingestion"]
        LAMB[Lambda Ingestion]
        EB[EventBridge Schedule]
    end

    subgraph Lake["Healthcare Data Lake"]
        RAW[(raw/clinical/<br/>PHI – restricted)]
        CLN[(cleaned/<br/>masked identifiers)]
        CUR[(curated/operations/<br/>de-identified aggregates)]
        QUA[(quarantine/)]
    end

    subgraph Privacy["Privacy & Governance"]
        MASK[PII Masking in ETL]
        KMS[KMS CMK – clinical key]
        RBAC[Steward / Analyst RBAC]
        LF[Lake Formation<br/>optional fine-grained]
        AUD[HIPAA Audit Log]
    end

    subgraph Consumers["Analytics Consumers"]
        OPS[Operations Dashboards]
        ATH[Athena – curated only]
        STE[Data Stewards<br/>quarantine review]
    end

    EHR & APPT & LAB --> LAMB
    EB --> LAMB
    LAMB --> RAW
    RAW --> GLUE[Glue ETL + Masking] --> CLN
    CLN --> DQ[Quality Validation] --> CUR
    DQ -->|fail| QUA
    MASK --> GLUE
    KMS & RBAC --> Lake
    CUR --> ATH --> OPS
    QUA --> STE
    AUD --> RBAC
```

### Key Components

| Component | Purpose |
|-----------|---------|
| PHI raw zone | Highest sensitivity; engineer/steward access only |
| Masking in cleaned | Tokenize/remove direct identifiers before curated |
| HIPAA governance | Assignment 7 framework + Lab 7.3 audit |
| Quarantine | Failed validation records with 90-day lifecycle |
| De-identified curated | Operational KPIs without PHI |
| Break-glass procedure | Documented emergency access with audit |

### Data Flows

| Stage | Input | Process | Output |
|-------|-------|---------|--------|
| Ingest | Synthetic patient JSON | Secure upload SSE-KMS | `raw/clinical/` |
| Mask | Raw PHI | Hash/tokenize identifiers | `cleaned/clinical/` |
| Validate | Cleaned records | Module 4 quality rules | Pass → curated; Fail → quarantine |
| Curate | Validated data | Appointment/lab aggregates | `curated/operations/` |
| Analyze | Curated only | Athena (analyst role) | Operational reports |

---

## Option 3: E-Commerce Analytics Lakehouse

Customer and sales analytics with star schema, batch + event-driven ingestion, KPI dashboards, and cost-optimized ad-hoc queries.

### Architecture Diagram

```mermaid
flowchart TB
    subgraph Sources["Commerce Sources"]
        ORD[Order API / Files]
        INV[Inventory Feeds]
        CUST[Customer Profiles]
        CLICK[Clickstream Events]
    end

    subgraph Ingest["Multi-Pattern Ingestion"]
        LAMB_B[Lambda – Batch Files]
        LAMB_E[Lambda – Event Stream<br/>clickstream]
        EB[EventBridge]
        S3E[S3 Event Notifications]
    end

    subgraph Lake["Analytics Lakehouse"]
        RAW[(raw/)]
        CLN[(cleaned/)]
        CUR[(curated/sales/<br/>star schema tables)]
    end

    subgraph Model["Dimensional Model"]
        FACT[fact_orders]
        DIM_C[dim_customer]
        DIM_P[dim_product]
        DIM_D[dim_date]
    end

    subgraph Analytics["Query & BI Layer"]
        ATH[Athena<br/>partition projection]
        CW[CloudWatch Dashboard<br/>KPI widgets]
        ML[ml/features/<br/>recommendations prep]
    end

    ORD & INV & CUST --> LAMB_B
    CLICK --> LAMB_E
    EB & S3E --> LAMB_B & LAMB_E
    LAMB_B & LAMB_E --> RAW
    RAW --> GLUE[Glue ETL] --> CLN --> CUR
    CUR --> FACT & DIM_C & DIM_P & DIM_D
    FACT & DIM_C & DIM_P & DIM_D --> ATH
    ATH --> CW
    CUR --> ML
```

### Key Components

| Component | Purpose |
|-----------|---------|
| Dual ingestion | Batch (orders/inventory) + event-driven (clickstream) |
| Star schema | Module 5 fact/dimension tables in curated zone |
| Athena optimization | Partition projection, column pruning (Lab 5.2–5.3) |
| KPI dashboard | CloudWatch + business metrics (Lab 8.1) |
| ML readiness | Feature store + dataset prep (Module 9) |
| Cost controls | Tagged resources + Cost Explorer (Lab 8.3) |

### Data Flows

| Stage | Input | Process | Output |
|-------|-------|---------|--------|
| Batch ingest | Orders, inventory CSV | Lambda → raw | `raw/sales/`, `raw/inventory/` |
| Event ingest | Clickstream JSON | EventBridge → Lambda | `raw/clickstream/` |
| ETL | Raw zones | Glue transform + quality | `cleaned/` → `curated/sales/` |
| Model | Cleaned orders | Star schema build | `fact_orders`, `dim_*` |
| Query | Curated Parquet | Athena SQL | Ad-hoc analytics |
| Monitor | Pipeline metrics | CloudWatch | Revenue/inventory KPIs |

---

## Option 4: Enterprise Data Platform

Full production-grade platform demonstrating every course module: multi-source ingestion, ETL, quality, orchestration, security, monitoring, cost controls, and ML readiness.

### Architecture Diagram

```mermaid
flowchart TB
    subgraph Sources["Enterprise Sources"]
        API[REST APIs]
        FILES[File Drops]
        EVENTS[Event Streams]
    end

    subgraph Ingest["Ingestion Patterns"]
        LAMB[Lambda Functions]
        EB[EventBridge Rules]
        S3EV[S3 Event Triggers]
    end

    subgraph Orchestration["Workflow Orchestration"]
        SF[Step Functions<br/>Ingest → Validate → ETL → Catalog]
        SNS_F[SNS Failure Alerts]
    end

    subgraph Lake["Medallion Data Lake"]
        RAW[(raw/)]
        CLN[(cleaned/)]
        CUR[(curated/)]
        QUA[(quarantine/)]
        META[(metadata/)]
        MLZ[(ml/training/<br/>ml/features/)]
    end

    subgraph Process["Processing"]
        GLUE[AWS Glue ETL<br/>schema evolution]
        DQ[Quality Framework<br/>Module 4]
        GC[Glue Data Catalog]
    end

    subgraph Analytics["Consumption"]
        ATH[Amazon Athena]
        BI[BI / Dashboards]
        ML[ML Training Pipeline]
    end

    subgraph Enterprise["Enterprise Controls"]
        KMS[KMS Encryption]
        IAM[Zone RBAC]
        GOV[Governance Audit]
        CW[CloudWatch + Alarms]
        COST[Cost Explorer + Budgets]
    end

    API & FILES & EVENTS --> LAMB
    EB & S3EV --> LAMB
    LAMB --> RAW
    SF --> LAMB & DQ & GLUE
    RAW --> GLUE --> CLN
    CLN --> DQ
    DQ -->|pass| CUR
    DQ -->|fail| QUA
    CUR --> GC --> ATH
    CUR --> MLZ --> ML
    GLUE --> GC
    SF -->|fail| SNS_F
    KMS & IAM & GOV --> Lake
    GLUE & LAMB & SF --> CW
    Lake --> COST
    ATH --> BI
```

### Key Components

| Layer | Services | Module Reference |
|-------|----------|------------------|
| Storage | S3 medallion zones | Module 1 |
| Ingestion | Lambda, EventBridge, S3 events | Module 2 |
| ETL | Glue jobs, crawlers | Module 3 |
| Quality | Validation, quarantine | Module 4 |
| Modeling | Star schema, Athena | Module 5 |
| Orchestration | Step Functions, SNS failures | Module 6 |
| Security | KMS, IAM RBAC, audit | Module 7 |
| Operations | Dashboards, alerts, cost | Module 8 |
| ML | Dataset prep, features, AI QA | Module 9 |

### Data Flows

| Stage | Input | Process | Output | Orchestration |
|-------|-------|---------|--------|---------------|
| Ingest | API/file/event | Lambda validation | `raw/` | Step Functions step 1 |
| Validate | Raw batch | Quality runner | Pass/fail routing | Step Functions step 2 |
| ETL | Cleaned input | Glue with bookmarks | `curated/` | Step Functions step 3 |
| Catalog | New partitions | Glue crawler | Data Catalog update | Step Functions step 4 |
| Secure | All objects | KMS + bucket policy | Encrypted at rest | Continuous |
| Monitor | Job metrics | CloudWatch alarms | SNS on failure | Event-driven |
| ML prep | Curated tables | Feature + dataset pipelines | `ml/` | Post-ETL trigger |
| Govern | All controls | Audit script | Governance report | Quarterly |

---

## Option Selection Guide

| Criterion | Option 1 Banking | Option 2 Healthcare | Option 3 E-Commerce | Option 4 Enterprise |
|-----------|------------------|---------------------|---------------------|---------------------|
| Primary focus | Regulatory reporting | HIPAA / PII | Analytics + KPIs | Full platform |
| Compliance depth | High (audit trails) | Highest (PHI) | Medium | High (all controls) |
| Ingestion complexity | Multi-file/API | Scheduled clinical | Batch + events | All patterns |
| ML component | Optional | Limited | Recommendations | Full Module 9 |
| Recommended for | Finance background | Healthcare interest | Retail/analytics focus | Portfolio showcase |

---

## Capstone Deliverable Mapping

| Deliverable | Primary Diagram Section |
|-------------|------------------------|
| `docs/ARCHITECTURE.md` | Option-specific diagram + data flows |
| `docs/GOVERNANCE.md` | Options 1, 2, 4 — security controls |
| `docs/COST-ANALYSIS.md` | All options — Cost Explorer integration |
| `architecture/diagrams/` | Export Mermaid renders as PNG for presentation |
