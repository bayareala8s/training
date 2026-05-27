# Module 5 — AWS stencil diagrams: Connectors & partner routing

**Module:** [week-05.md](../modules/week-05.md) · **Lab:** [Lab 5](../labs/lab-05-sftp-connector.md)

---

## Diagram 1 — Transfer server vs connector

```mermaid
flowchart TB
  subgraph Server["Transfer SERVER — partner comes to you"]
    P1[Partner] -->|SFTP upload| SRV["AWS Transfer Family<br/>server"]
    SRV --> S3a[("S3 inbound/")]
  end
  subgraph Connector["Transfer CONNECTOR — you go to partner"]
    S3b[("S3 outbound staging/")] --> CON["AWS Transfer<br/>connector"]
    CON -->|SFTP upload| P2[Partner SFTP host]
  end

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class SRV,CON transfer
  class S3a,S3b storage
```

---

## Diagram 2 — Connector components

```mermaid
flowchart LR
  OPS[Operator / Step Functions] --> API["transfer:StartFileTransfer"]
  API --> CON[Transfer connector]
  CON --> SM["AWS Secrets Manager<br/>SSH key / password"]
  CON --> IAM[IAM access role]
  CON -->|SFTP TLS| REMOTE[Partner endpoint]
  IAM --> S3[("Amazon S3")]
  CON --> HK[Trusted host keys]

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef security fill:#DD344C,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class CON transfer
  class SM,HK security
  class S3 storage
```

---

## Diagram 3 — Four canonical transfer patterns

```mermaid
flowchart TB
  subgraph S3S3["S3 → S3"]
    A1[Internal copy / replication]
  end
  subgraph S3SFTP["S3 → SFTP"]
    S1[("S3")] --> C1[Connector] --> X1[Partner]
  end
  subgraph SFTPS3["SFTP → S3"]
    X2[Partner] --> SRV[Server] --> S2[("S3")]
  end
  subgraph SFTPSFTP["SFTP → SFTP"]
    X3[Partner A] --> H[Hub S3] --> C2[Connector] --> X4[Partner B]
  end

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class C1,C2,SRV transfer
  class S1,S2,H storage
```

---

## Diagram 4 — Multi-hop with correlation ID

```mermaid
flowchart LR
  PA[Partner A] -->|inbound| S3[("S3 land")]
  S3 --> L["Lambda transform"]
  L --> STG[("S3 outbound staging")]
  STG --> CON[Connector]
  CON --> PB[Partner B]
  DDB[("DynamoDB jobs<br/>correlation_id")] -.-> L
  DDB -.-> CON

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef database fill:#C925D1,stroke:#232F3E,color:#fff
  class CON transfer
  class S3,STG storage
  class DDB database
```

---

## Diagram 5 — Lab 5: Connector to same server (loopback demo)

The lab connector points at **your own** Transfer server to avoid external partner dependencies.

```mermaid
flowchart LR
  S3[("S3 connector prefix")] --> CON[Transfer connector]
  CON -->|SFTP| TF["Transfer server<br/>same account"]
  TF --> S3

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class CON,TF transfer
  class S3 storage
```

---

**Editable stencil:** [week-05-connectors.drawio](week-05-connectors.drawio)
