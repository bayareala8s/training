# Module 7 — AWS stencil diagrams: Operations & observability

**Module:** [week-07.md](../modules/week-07.md) · **Lab:** [Lab 7](../labs/lab-07-observability.md)

---

## Diagram 1 — Observability stack (lab)

```mermaid
flowchart TB
  subgraph Sources["Metric & log sources"]
    TF["Transfer Family"]
    L["AWS Lambda"]
    SFN["Step Functions"]
    S3["Amazon S3"]
  end
  subgraph Observe["Observability"]
    CW["Amazon CloudWatch<br/>Metrics + Logs"]
    DASH["CloudWatch Dashboard<br/>baylearn-mft-lab-ops"]
    ALM["CloudWatch Alarms"]
  end
  subgraph Respond["Response"]
    SNS["Amazon SNS"]
    RB[Runbook link in alarm]
    ONCALL[Email / PagerDuty]
  end
  TF & L & SFN & S3 --> CW
  CW --> DASH
  CW --> ALM --> SNS --> ONCALL
  ALM --> RB

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  classDef orchestration fill:#E7157B,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
  classDef integration fill:#FF9900,stroke:#232F3E,color:#fff
  class TF transfer
  class L compute
  class SFN orchestration
  class S3 storage
  class CW,DASH,ALM mgmt
  class SNS integration
```

---

## Diagram 2 — SLI → SLO → error budget

```mermaid
flowchart LR
  SLI[SLI measurements<br/>success rate, P95 latency]
  SLO[SLO targets<br/>99.5% / 15 min P95]
  EB[Error budget<br/>allowed failures / month]
  DEC[Engineering decision<br/>feature freeze vs reliability]
  SLI --> SLO --> EB --> DEC

  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
  class SLI,SLO,EB,DEC mgmt
```

---

## Diagram 3 — Incident triage flow

```mermaid
flowchart TD
  ALM[Alarm fires] --> DASH[Open dashboard]
  DASH --> CID{Have correlation_id?}
  CID -->|yes| SFN[Step Functions execution history]
  CID -->|no| S3[S3 key + access logs]
  SFN --> LLOG[Lambda CloudWatch Logs]
  S3 --> LLOG
  LLOG --> RB[Runbook action]
  RB --> FIX[Mitigate / replay / quarantine]

  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
  class ALM,DASH mgmt
```

---

## Diagram 4 — Structured log fields (searchable)

```mermaid
flowchart LR
  subgraph Fields["Required JSON fields"]
    F1[correlation_id]
    F2[partner_id]
    F3[job_id]
    F4[s3_key]
    F5[component]
    F6[level]
  end
  Fields --> CW[CloudWatch Logs Insights]
  CW --> Q["Query: filter correlation_id"]

  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
  class CW mgmt
```

---

## Diagram 5 — Cost drivers (MFT on AWS)

```mermaid
flowchart TB
  C1["Transfer Family server<br/>~hourly while ONLINE"]
  C2["S3 storage + requests"]
  C3["Lambda invocations"]
  C4["Step Functions transitions"]
  C5["KMS API calls<br/>mitigate with bucket key"]
  C6["ECS Fargate<br/>per task second only"]
  STOP["./scripts/stop_stack.sh<br/>destroys billable lab resources"]

  classDef transfer fill:#8C4FFF,stroke:#232F3E,color:#fff
  classDef storage fill:#7AA116,stroke:#232F3E,color:#fff
  classDef compute fill:#D86613,stroke:#232F3E,color:#fff
  class C1 transfer
  class C2 storage
  class C3,C4,C6 compute
  class STOP mgmt
  classDef mgmt fill:#759C3E,stroke:#232F3E,color:#fff
```

---

**Editable stencil:** [week-07-observability.drawio](week-07-observability.drawio)
