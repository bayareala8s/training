# Module 8 — AWS stencil diagrams: Capstone full platform

**Module:** [week-08.md](../modules/week-08.md) · **Capstone:** [capstone.md](../capstone.md)

---

## Diagram 1 — End-to-end reference architecture (all modules)

This is the **target picture** for capstone demos and stakeholder decks.

```mermaid
flowchart TB
  subgraph Users["Users & partners"]
    BU[Business user]
    PT[Partner SFTP]
  end
  subgraph Experience["Module 6 — Experience"]
    UI[Self-serve UI / API client]
    COG["Amazon Cognito"]
  end
  subgraph Control["Module 6 — Control plane"]
    APIGW["API Gateway"]
    API["Lambda api"]
    DDB[("DynamoDB<br/>connections + jobs")]
  end
  subgraph Edge["Modules 1 & 5 — Edge"]
    TF["Transfer Family<br/>server"]
    CON["Transfer Family<br/>connector"]
  end
  subgraph Landing["Modules 1–2 — Landing"]
    S3[("Amazon S3<br/>KMS encrypted")]
  end
  subgraph Automate["Modules 3–4 — Automation"]
    L1["Lambda s3_processor"]
    SFN["Step Functions workflow"]
    SNS["Amazon SNS"]
  end
  subgraph Ops["Module 7 — Operations"]
    CW["CloudWatch<br/>dashboard + alarms"]
  end
  subgraph Large["Module 9 — Large files"]
    DISP["Lambda ecs_dispatcher"]
    ECS["Amazon ECS Fargate"]
  end

  BU --> UI --> COG
  UI --> APIGW --> API --> DDB
  API --> SFN
  PT --> TF --> S3
  SFN --> L1 --> S3
  SFN --> CON --> PT
  S3 -->|large/inbound/| DISP --> ECS --> S3
  TF & L1 & SFN & ECS --> CW
  SFN --> SNS

  classDef auth fill:#DD344C,stroke:#232F3E,color:#fff
  classDef api fill:#E7157B,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef database fill:#C925D1,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
  class COG auth
  class APIGW api
  class API,L1,DISP compute
  class ECS compute
  class DDB database
  class S3 storage
  class TF,CON transfer
  class SFN orchestration
  class CW mgmt
  class SNS integration
```

---

## Diagram 2 — Capstone demo path (10-minute narrative)

```mermaid
flowchart LR
  S1[1 Problem statement] --> S2[2 Architecture slide]
  S2 --> S3[3 Login / catalog]
  S3 --> S4[4 Upload or SFTP]
  S4 --> S5[5 Step Functions success]
  S5 --> S6[6 Security evidence KMS logs]
  S6 --> S7[7 Roadmap]

  classDef step fill:#232F3E,stroke:#232F3E,color:#fff
  class S1,S2,S3,S4,S5,S6,S7 step
```

---

## Diagram 3 — Capstone tracks A / B / C focus

```mermaid
flowchart TB
  subgraph A["Track A — Self-serve"]
    A1[Cognito + API depth]
    A2[Connection catalog UX]
  end
  subgraph B["Track B — Automation hub"]
    B1[Step Functions + idempotency]
    B2[Audit + quarantine story]
  end
  subgraph C["Track C — Migration"]
    C1[As-is / to-be diagrams]
    C2[Phased cutover plan]
  end
  CORE[Shared core<br/>Transfer + S3 + security]
  CORE --> A & B & C

  classDef core fill:#7AA116,stroke:#232F3E,color:#fff
  class CORE core
```

---

## Diagram 4 — Production hardening checklist (beyond lab)

```mermaid
mindmap
  root((Production MFT))
    Security
      SCPs
      Separate accounts
      CMK rotation
    Reliability
      Multi-AZ
      DLQ
      Replay runbooks
    Scale
      EventBridge fan-out
      Express workflows
      Fargate workers
    Governance
      Partner matrix
      Approval workflows
      Cost allocation tags
```

---

**Editable stencil:** [week-08-capstone-platform.drawio](week-08-capstone-platform.drawio) · **Full lab wiring:** [lab-stack-reference.drawio](lab-stack-reference.drawio)
