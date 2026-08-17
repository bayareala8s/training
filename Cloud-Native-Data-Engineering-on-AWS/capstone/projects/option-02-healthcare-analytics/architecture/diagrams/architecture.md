# Architecture Diagrams – Healthcare Analytics Platform

Project: `cnde-cap-healthcare` · Capstone Option 2 · SYNTHETIC data

---

## Context

```mermaid
flowchart LR
  subgraph Sources
    EHR[EHR Demographics]
    SCH[Scheduling System]
    LAB[Lab Information System]
  end

  subgraph Platform["cnde-cap-healthcare"]
    ING[Ingestion]
    RAW[S3 raw]
    DQ[RuleEngine]
    CUR[Curated transforms]
    META[Audit metadata]
  end

  subgraph Consumers
    OPS[Clinical Operations]
    AN[Analysts]
    PRIV[Privacy Stewards]
  end

  EHR --> ING
  SCH --> ING
  LAB --> ING
  ING --> RAW --> DQ
  DQ -->|pass| CUR
  DQ -->|fail| PRIV
  CUR --> OPS
  CUR --> AN
  CUR --> META
```

---

## Medallion + PHI Boundary

```mermaid
flowchart TB
  RAW["raw/patients · appointments · lab_results\n(plaintext synthetic PHI)"]
  DQ["validators: not_null · range · enum · regex"]
  CLN[cleaned]
  QUA[quarantine]
  CP["curated/patients\nssn_masked + email_hash"]
  CA["curated/appointments\nby department"]
  CL["curated/lab_results\nclinical facts"]
  META[metadata reports]

  RAW --> DQ
  DQ -->|pass| CLN
  DQ -->|fail| QUA
  CLN --> CP
  CLN --> CA
  CLN --> CL
  DQ --> META

  subgraph AnalystView["Analyst IAM: curated only"]
    CP
    CA
    CL
  end
```

---

## Patient Masking Detail

```mermaid
flowchart LR
  A[Raw SSN 123-45-6789] --> B["Mask ***-**-6789"]
  C[Raw email user@example.com] --> D[SHA-256 hex digest]
  B --> E[Curated patient row]
  D --> E
```

---

## Appointment Aggregation

```mermaid
flowchart LR
  A[Cleaned appointments] --> G[GROUP BY department]
  G --> M["counts · duration · completion_rate"]
  M --> R[appointments_by_department]
```
