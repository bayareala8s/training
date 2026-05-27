# Module 3 — AWS stencil diagrams: Event-driven automation

**Module:** [week-03.md](../modules/week-03.md) · **Lab:** [Lab 3](../labs/lab-03-s3-event-processor.md)

---

## Diagram 1 — End-to-end processing pipeline

```mermaid
flowchart LR
  subgraph Ingest
    SFTP["Transfer Family"] --> IN[("S3<br/>inbound/")]
  end
  subgraph Process
    IN -->|ObjectCreated| L["AWS Lambda<br/>s3_processor"]
    L -->|valid| PROC[("S3<br/>processing/")]
    L -->|invalid| Q[("S3<br/>quarantine/")]
  end
  subgraph Next
    PROC --> SFN["Step Functions<br/>Module 4"]
  end

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  class SFTP transfer
  class IN,PROC,Q storage
  class L compute
  class SFN orchestration
```

---

## Diagram 2 — S3 event notification wiring

**Important:** One bucket = one notification configuration (all Lambda targets merged).

```mermaid
flowchart TB
  S3[("Amazon S3<br/>landing bucket")]
  S3 -->|prefix partners/demo/inbound/| L1["Lambda<br/>s3_processor"]
  S3 -->|prefix partners/demo/large/inbound/| L2["Lambda<br/>ecs_dispatcher"]
  L1 --> PROC[processing/ or quarantine/]
  L2 --> ECS["ECS RunTask<br/>Module 9"]

  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  class S3 storage
  class L1,L2 compute
```

---

## Diagram 3 — Idempotency with DynamoDB

S3 events are **at-least-once**.

```mermaid
sequenceDiagram
  participant S3 as Amazon S3
  participant L as Lambda s3_processor
  participant DDB as DynamoDB idempotency

  S3->>L: ObjectCreated event
  L->>DDB: GetItem idempotency_key
  alt Already processed
    DDB-->>L: exists
    L-->>S3: skip (200)
  else First time
    DDB-->>L: not found
    L->>S3: CopyObject → processing/
    L->>DDB: PutItem idempotency_key
  end
```

---

## Diagram 4 — Validation decision tree (Lambda logic)

```mermaid
flowchart TD
  START[ObjectCreated] --> EXT{Allowed extension?}
  EXT -->|no| Q[Copy to quarantine/]
  EXT -->|yes| SIZE{Size within limit?}
  SIZE -->|no| Q
  SIZE -->|yes| DUP{Idempotency key exists?}
  DUP -->|yes| SKIP[Exit success]
  DUP -->|no| P[Copy to processing/]
  P --> LOG[Structured JSON log]

  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  class Q,P storage
  class START,EXT,SIZE,DUP compute
```

---

## Diagram 5 — EventBridge alternative (production pattern)

```mermaid
flowchart LR
  S3[("S3")] --> EB[Amazon EventBridge]
  EB --> R1[Rule: inbound validate]
  EB --> R2[Rule: large file dispatch]
  R1 --> L1[Lambda]
  R2 --> L2[Lambda]

  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef integration fill:#E7157B,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  class S3 storage
  class EB integration
  class L1,L2 compute
```

Lab 3 uses direct S3→Lambda for simplicity.

---

**Editable stencil:** [week-03-event-driven.drawio](week-03-event-driven.drawio)
