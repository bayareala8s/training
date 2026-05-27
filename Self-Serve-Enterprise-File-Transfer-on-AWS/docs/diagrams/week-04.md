# Module 4 — AWS stencil diagrams: Step Functions orchestration

**Module:** [week-04.md](../modules/week-04.md) · **Lab:** [Lab 4](../labs/lab-04-step-functions-workflow.md)

---

## Diagram 1 — Orchestration vs choreography

```mermaid
flowchart TB
  subgraph CH["Choreography — Module 3 style"]
    S3a[("S3")] -->|event| LA[Lambda A]
    S3a -->|event| LB[Lambda B]
  end
  subgraph OR["Orchestration — Module 4 style"]
    SFN["AWS Step Functions<br/>Standard workflow"]
    SFN --> V[Validate task]
    V --> C[Copy task]
    C --> N[Notify task]
  end

  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  class S3a storage
  class LA,LB compute
  class SFN,V,C,N orchestration
```

---

## Diagram 2 — Lab 4 state machine (happy + failure paths)

```mermaid
stateDiagram-v2
  [*] --> ValidateFile: StartExecution
  ValidateFile --> CheckValid: Lambda OK
  CheckValid --> CopyToProcessing: valid = true
  CheckValid --> NotifyFailure: valid = false
  CopyToProcessing --> NotifySuccess
  NotifySuccess --> [*]
  NotifyFailure --> FailState
  FailState --> [*]

  note right of ValidateFile
    Retry: service errors only
    Catch: States.ALL → NotifyFailure
  end note
```

---

## Diagram 3 — Step Functions + Lambda + SNS (lab stack)

```mermaid
flowchart TB
  API[Manual / API start] --> SFN["AWS Step Functions<br/>transfer-workflow"]
  SFN --> LV["Lambda<br/>workflow_validate"]
  SFN --> LC["Lambda<br/>workflow_copy"]
  SFN --> LS["Lambda<br/>notify_success"]
  SFN --> LF["Lambda<br/>notify_failure"]
  LV & LC --> S3[("Amazon S3")]
  LS & LF --> SNS["Amazon SNS"]
  SNS --> EMAIL[Email / ops]

  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef integration fill:#FF9900,stroke:#232F3E,color:#fff
  class SFN orchestration
  class LV,LC,LS,LF compute
  class S3 storage
  class SNS integration
```

---

## Diagram 4 — Correlation ID propagation

```mermaid
sequenceDiagram
  participant Client
  participant SFN as Step Functions
  participant Val as Lambda validate
  participant Copy as Lambda copy
  participant SNS as SNS notify

  Client->>SFN: StartExecution {correlation_id}
  SFN->>Val: Invoke {correlation_id, bucket, key}
  Val-->>SFN: {valid: true, correlation_id}
  SFN->>Copy: Invoke same correlation_id
  Copy-->>SFN: {dest_key, correlation_id}
  SFN->>SNS: Publish correlation_id in message
```

---

## Diagram 5 — Standard vs Express workflow choice

| Use **Standard** when | Use **Express** when |
|----------------------|----------------------|
| Auditors need full history | Sub-minute high volume |
| Runs minutes to hours | Fan-out micro-steps |
| Human approval waits | No long-running branch |

```mermaid
flowchart LR
  MFT[Enterprise MFT job] --> STD["Step Functions<br/>STANDARD"]
  MICRO[High-volume micro route] --> EXP["Step Functions<br/>EXPRESS"]

  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  class STD,EXP orchestration
```

---

**Editable stencil:** [week-04-step-functions.drawio](week-04-step-functions.drawio)
