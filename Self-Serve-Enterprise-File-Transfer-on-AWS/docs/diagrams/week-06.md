# Module 6 — AWS stencil diagrams: Self-serve platform

**Module:** [week-06.md](../modules/week-06.md) · **Lab:** [Lab 6](../labs/lab-06-self-serve-api.md)

---

## Diagram 1 — Self-serve control plane (logical)

```mermaid
flowchart TB
  subgraph Experience["Experience layer"]
    U[Business user]
    UI[Web app or Postman]
  end
  subgraph Auth["Authentication"]
    COG["Amazon Cognito<br/>User pool"]
  end
  subgraph API["API layer"]
    APIGW["Amazon API Gateway<br/>HTTP API + JWT authorizer"]
    APIL["AWS Lambda<br/>api handler"]
  end
  subgraph Data["Platform data"]
    DDB1[("DynamoDB<br/>connections")]
    DDB2[("DynamoDB<br/>jobs")]
  end
  subgraph Automation["Transfer automation"]
    SFN["AWS Step Functions"]
    S3[("Amazon S3")]
    TF["Transfer Family"]
  end
  U --> UI --> COG
  UI -->|Bearer JWT| APIGW --> APIL
  APIL --> DDB1 & DDB2
  APIL -->|StartExecution| SFN
  SFN --> S3 & TF

  classDef auth fill:#DD344C,stroke:#232F3E,color:#fff
  classDef api fill:#E7157B,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef database fill:#C925D1,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  class COG auth
  class APIGW api
  class APIL compute
  class DDB1,DDB2 database
  class S3 storage
  class TF transfer
  class SFN orchestration
```

---

## Diagram 2 — POST /v1/jobs sequence

```mermaid
sequenceDiagram
  autonumber
  participant User
  participant Cognito as Amazon Cognito
  participant APIGW as API Gateway
  participant API as Lambda api
  participant DDB as DynamoDB jobs
  participant SFN as Step Functions

  User->>Cognito: Authenticate
  Cognito-->>User: IdToken (JWT)
  User->>APIGW: POST /v1/jobs + Authorization
  APIGW->>APIGW: Validate JWT (sub, aud)
  APIGW->>API: Invoke
  API->>DDB: Verify connection owned by sub
  API->>SFN: StartExecution (correlation_id)
  API->>DDB: PutItem job RUNNING
  API-->>User: 202 {job_id, correlation_id}
```

---

## Diagram 3 — Authorization boundary (owner scope)

```mermaid
flowchart TD
  JWT[JWT claims sub] --> API[Lambda API]
  API --> Q{connection.owner_sub<br/>== jwt.sub?}
  Q -->|no| R403[403 Forbidden]
  Q -->|yes| OK[Allow catalog / job]
  OK --> PREFIX{source_key under<br/>connection prefix?}
  PREFIX -->|no| R400[400 Bad request]
  PREFIX -->|yes| SFN[Start workflow]

  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  class API,Q,PREFIX compute
```

**Never return** Secrets Manager ARNs or SSH private keys in API responses.

---

## Diagram 4 — Entity relationship (simplified)

```mermaid
erDiagram
  USER ||--o{ CONNECTION : owns
  CONNECTION ||--o{ JOB : submits
  JOB ||--|| EXECUTION : maps_to
  EXECUTION {
    string execution_arn
    string correlation_id
  }
  CONNECTION {
    string connection_id
    string type
    string landing_prefix
  }
  JOB {
    string job_id
    string state
  }
```

---

## Diagram 5 — Idempotency at API layer

```mermaid
flowchart LR
  REQ[POST /jobs<br/>x-idempotency-key] --> API[Lambda]
  API --> DDB[("DynamoDB<br/>idempotency table")]
  DDB -->|new key| SFN[Start execution]
  DDB -->|duplicate key| RET[Return prior job_id]

  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef database fill:#C925D1,stroke:#232F3E,color:#fff
  class API compute
  class DDB database
```

---

**Editable stencil:** [week-06-self-serve-api.drawio](week-06-self-serve-api.drawio)
