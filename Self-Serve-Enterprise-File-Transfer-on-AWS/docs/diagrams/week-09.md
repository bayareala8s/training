# Module 9 — AWS stencil diagrams: ECS Fargate large files

**Module:** [week-09-ecs-fargate.md](../modules/week-09-ecs-fargate.md) · **Lab:** [Lab 9](../labs/lab-09-ecs-fargate-large-files.md)

---

## Diagram 1 — Lambda vs Fargate decision

```mermaid
flowchart TB
  FILE[File lands in S3]
  FILE --> Q{Size / duration?}
  Q -->|Small quick validate| L["AWS Lambda<br/>s3_processor"]
  Q -->|Large or long hash| PATH[prefix large/inbound/]
  PATH --> DISP["Lambda ecs_dispatcher"]
  DISP --> ECS["Amazon ECS Fargate<br/>RunTask on demand"]
  ECS --> OUT[("S3 large/processed/<br/>+ manifest.json")]

  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef container fill:#D86613,stroke:#232F3E,color:#fff
  class FILE,OUT storage
  class L,DISP compute
  class ECS container
```

---

## Diagram 2 — Lab 9 architecture (VPC + endpoints)

```mermaid
flowchart TB
  subgraph Event["Event path"]
    S3IN[("S3 large/inbound/")] -->|ObjectCreated| DISP["Lambda<br/>ecs_dispatcher"]
    DISP --> RT["ecs:RunTask"]
  end
  subgraph VPC["VPC — public subnets"]
    RT --> TASK["Fargate task<br/>worker container"]
    TASK --> VPCE["S3 Gateway<br/>VPC endpoint"]
  end
  subgraph Registry["Container"]
    ECR["Amazon ECR<br/>worker image"]
    ECR -.->|pull| TASK
  end
  VPCE --> S3OUT[("S3 large/processed/")]
  TASK --> CW["CloudWatch Logs<br/>/ecs/..."]

  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef network fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef registry fill:#D86613,stroke:#232F3E,color:#fff
  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
  class S3IN,S3OUT storage
  class DISP compute
  class TASK container
  class VPCE network
  class ECR registry
  class CW mgmt
```

**No NAT gateway** in lab — task uses public IP + S3 endpoint.

---

## Diagram 3 — Worker task sequence

```mermaid
sequenceDiagram
  participant S3 as Amazon S3
  participant Disp as Lambda dispatcher
  participant ECS as ECS Fargate
  participant Worker as Container worker
  participant Logs as CloudWatch Logs

  S3->>Disp: ObjectCreated large/inbound/file.bin
  Disp->>ECS: RunTask TRANSFER_JOB env JSON
  ECS->>Worker: Start container
  Worker->>S3: GetObject stream
  Worker->>Worker: SHA-256
  Worker->>S3: PutObject processed/file.bin
  Worker->>S3: PutObject manifest.json
  Worker->>Logs: JSON status lines
  ECS-->>Disp: Task stopped exit 0
```

---

## Diagram 4 — IAM roles (execution vs task)

```mermaid
flowchart LR
  subgraph Exec["ECS task execution role"]
    E1[ECR pull]
    E2[CloudWatch Logs write]
  end
  subgraph Task["ECS task role"]
    T1[S3 GetObject inbound]
    T2[S3 PutObject processed]
    T3[KMS Decrypt/Encrypt]
  end
  subgraph DispRole["Lambda dispatcher role"]
    D1[ecs:RunTask]
    D2[iam:PassRole]
  end
  DispRole --> ECS[ECS service]
  Exec & Task --> ECS

  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  class Exec,Task,DispRole compute
```

---

## Diagram 5 — Step Functions sync integration (future)

```mermaid
flowchart LR
  SFN["Step Functions"] -->|ecs:runTask.sync| ECS["Fargate worker"]
  ECS -->|manifest OK| SFN
  SFN --> SNS["Notify success"]

  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  classDef container fill:#D86613,stroke:#232F3E,color:#fff
  class SFN orchestration
  class ECS container
```

---

**Editable stencil:** [week-09-ecs-fargate.drawio](week-09-ecs-fargate.drawio)
