# Module 1 — AWS stencil diagrams: Enterprise MFT & Transfer Family

**Module:** [week-01.md](../modules/week-01.md) · **Lab:** [Lab 1](../labs/lab-01-transfer-family-sftp.md)

---

## Diagram 1 — Legacy MFT appliance (before AWS)

What many enterprises run today: a single appliance in the data center.

```mermaid
flowchart TB
  subgraph Partners["External partners"]
    P1[Vendor A]
    P2[Bank B]
    P3[Payroll provider]
  end
  subgraph DC["Corporate data center"]
    MFT[MFT appliance<br/>SFTP / AS2 / FTPS]
    NAS[(NAS / SAN storage)]
    SCR[Scheduled scripts<br/>cron / adapters]
    ERP[ERP / claims / data lake]
  end
  P1 & P2 & P3 -->|SFTP| MFT
  MFT --> NAS
  NAS --> SCR --> ERP

  classDef partner fill:#E8E8E8,stroke:#232F3E
  classDef legacy fill:#C7131F,stroke:#232F3E,color:#fff
  class P1,P2,P3 partner
  class MFT,SCR legacy
```

**Student takeaway:** The appliance is the **bottleneck** for scale, DR, and API integration.

---

## Diagram 2 — AWS Transfer Family + S3 (course target)

Managed protocol edge; S3 is the **system of record**.

```mermaid
flowchart LR
  subgraph Edge["AWS — Protocol edge"]
    TF["AWS Transfer Family<br/>SFTP server"]
  end
  subgraph Landing["AWS — Landing zone"]
    S3[("Amazon S3<br/>Versioned bucket")]
  end
  subgraph Auto["AWS — Automation (Weeks 3–8)"]
    L["AWS Lambda"]
    SFN["AWS Step Functions"]
    CON["Transfer connector"]
  end
  Partner[Partner SFTP client] -->|SSH/SFTP| TF
  TF -->|IAM role PutObject| S3
  S3 -->|ObjectCreated| L
  L --> SFN
  SFN --> CON

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  class TF,CON transfer
  class S3 storage
  class L compute
  class SFN orchestration
```

---

## Diagram 3 — Hub-and-spoke S3 prefix model

Prefixes are **security and lifecycle boundaries**, not folders.

```mermaid
flowchart TB
  B[("S3: company-transfer-landing")]
  B --> P[partners/]
  P --> D[demo/]
  D --> IN[inbound/]
  D --> OUT[outbound/]
  D --> Q[quarantine/]
  D --> ARC[archive/]
  D --> PROC[processing/]
  IN -->|Week 3 Lambda| PROC
  PROC -->|Week 4 SFN| ARC

  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class B storage
```

**Lab 1 path:** `partners/demo/inbound/` ← SFTP home directory mapping.

---

## Diagram 4 — Lab 1: Partner upload sequence

Trace this path when troubleshooting “file not in S3.”

```mermaid
sequenceDiagram
  autonumber
  participant Partner as Partner SFTP client
  participant TF as Transfer Family server
  participant IAM as IAM access role
  participant S3 as Amazon S3

  Partner->>TF: SSH connect (user + key)
  TF->>IAM: AssumeRole (scoped to bucket)
  Partner->>TF: PUT file (logical path /)
  TF->>S3: PutObject partners/demo/inbound/file.csv
  S3-->>Partner: Upload complete (via SFTP OK)
  Note over S3: Week 3 adds ObjectCreated → Lambda
```

---

## Diagram 5 — Push vs pull (business direction)

| Arrow label | Meaning |
|-------------|---------|
| Partner → you | **Inbound push** (Lab 1 server) |
| You → partner | **Outbound push** (Module 5 connector) |
| You ← partner | **Pull** (connector retrieve) |

```mermaid
flowchart LR
  subgraph Inbound["Inbound push"]
    P1[Partner] -->|upload| YOU1[Your Transfer server]
    YOU1 --> S3a[(S3 inbound/)]
  end
  subgraph Outbound["Outbound push"]
    S3b[(S3 outbound/)] --> CON[Transfer connector]
    CON -->|upload| P2[Partner SFTP]
  end

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class YOU1,CON transfer
  class S3a,S3b storage
```

---

**Editable stencil:** [week-01-transfer-edge.drawio](week-01-transfer-edge.drawio)
