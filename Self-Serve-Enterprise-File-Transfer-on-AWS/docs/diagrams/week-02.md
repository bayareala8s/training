# Module 2 — AWS stencil diagrams: Security & governance

**Module:** [week-02.md](../modules/week-02.md) · **Lab:** [Lab 2](../labs/lab-02-security-hardening.md)

---

## Diagram 1 — Defense-in-depth layers

Each layer provides **evidence** for auditors.

```mermaid
flowchart TB
  subgraph L1["Layer 1 — Identity"]
    IAM["AWS IAM<br/>roles & policies"]
    TFU[Transfer user + SSH key]
  end
  subgraph L2["Layer 2 — Encryption"]
    KMS["AWS KMS<br/>CMK"]
    TLS[TLS in transit SFTP]
  end
  subgraph L3["Layer 3 — Storage controls"]
    S3[("Amazon S3")]
    BPA[S3 Block Public Access]
    BP[Bucket policy]
  end
  subgraph L4["Layer 4 — Audit"]
    CT[AWS CloudTrail]
    ALOG[S3 access logs]
    CW[Amazon CloudWatch Logs]
  end
  TFU --> IAM --> S3
  KMS --> S3
  BPA --> S3
  BP --> S3
  S3 --> ALOG
  IAM --> CT

  classDef security fill:#DD344C,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
  class IAM,KMS,BPA security
  class S3 storage
  class CT,CW,ALOG mgmt
```

---

## Diagram 2 — KMS encryption flow (SSE-KMS)

Who must have `kms:Decrypt`?

```mermaid
flowchart LR
  UP[Uploader<br/>Transfer or Lambda] -->|PutObject| S3[("S3 object<br/>SSE-KMS")]
  S3 -->|envelope| KMS[(AWS KMS CMK)]
  DOWN[Downloader<br/>Lambda / analyst] -->|GetObject| S3
  DOWN -->|Decrypt| KMS

  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef security fill:#DD344C,stroke:#232F3E,color:#fff
  class S3 storage
  class KMS security
```

**Common failure:** Switch bucket to CMK but Lambda role lacks KMS permissions.

---

## Diagram 3 — IAM role separation (least privilege)

Never use one “super role” for all partners.

```mermaid
flowchart TB
  TF["Transfer Family"] --> R1["Role: transfer-inbound<br/>prefix partners/demo/*"]
  L3["Lambda s3_processor"] --> R2["Role: lambda-processor<br/>read/write landing bucket"]
  SFN["Step Functions"] --> R3["Role: sfn-workflow<br/>invoke Lambdas"]
  CON["Transfer connector"] --> R4["Role: connector-access<br/>StartFileTransfer + S3"]

  R1 & R2 & R3 & R4 --> S3[("S3 landing bucket")]

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class TF,CON transfer
  class L3 compute
  class SFN orchestration
  class S3 storage
```

---

## Diagram 4 — Network: public Transfer + S3 gateway endpoint

Lab stack uses public Transfer endpoint; Lambda/ECS can use VPC endpoints.

```mermaid
flowchart TB
  subgraph Internet
    PC[Partner client]
  end
  subgraph AWS["AWS Region"]
    TF["Transfer Family<br/>PUBLIC endpoint"]
    subgraph VPC["VPC (Lab 9)"]
      L["Lambda / ECS<br/>optional"]
      EP["VPC Gateway Endpoint<br/>S3"]
    end
    S3[("Amazon S3")]
  end
  PC -->|SFTP :22| TF
  TF --> S3
  L --> EP --> S3

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef network fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class TF transfer
  class EP network
  class S3 storage
```

---

## Diagram 5 — Audit evidence chain

Answer: “Who uploaded file X and when?”

```mermaid
flowchart LR
  E1[Transfer / API action] --> CT[CloudTrail<br/>who assumed role]
  E2[S3 PutObject] --> ALOG[S3 server access log<br/>source IP, key]
  E3[Object version] --> VER[S3 versioning<br/>overwrite history]
  CT & ALOG & VER --> AUDIT[Compliance narrative]

  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  class CT,ALOG mgmt
  class VER storage
```

---

**Editable stencil:** [week-02-security-governance.drawio](week-02-security-governance.drawio)
