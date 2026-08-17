# Lab 6.3: Failure Handling with SNS Notifications — Architecture Diagram

## Purpose

Add operational visibility to the Lab 6.2 pipeline by publishing structured **SNS** notifications on pipeline failure (and optionally success). Create an SNS topic with email subscription, wire `sns:Publish` tasks into the Step Functions state machine, and document an on-call runbook linking automated alerts to concrete recovery steps for the RetailCo daily ETL.

---

## Architecture Overview

```mermaid
flowchart TD
    subgraph Trigger["Execution Trigger"]
        EB["EventBridge Schedule<br/>Daily 06:00 UTC"]
        MAN["Manual start-execution"]
    end

    subgraph Pipeline["Step Functions Pipeline (Lab 6.2 base)"]
        VI["ValidateInput"]
        GLUE["StartGlueETL"]
        QC["RunQualityCheck"]
        EV["EvaluateQuality"]
        VI --> GLUE --> QC --> EV
    end

    EB --> Pipeline
    MAN --> Pipeline

    subgraph Outcomes["Terminal States"]
        SUCC["PipelineSucceeded"]
        WARN["PipelineSucceededWithWarning"]
        PREP_F["PrepareFailureNotification"]
        PREP_S["PrepareSuccessNotification<br/>(optional)"]
        FAIL["PipelineFailed"]
    end

    EV -->|pass >= 99.9| SUCC
    EV -->|pass >= 99.0| WARN
    EV -->|pass < 99.0| PREP_F
    VI -.->|invalid| PREP_F
    GLUE -.->|catch| PREP_F

    SUCC --> PREP_S
    PREP_S -->|sns:Publish| SNS_OK["SNS Success Message<br/>(optional)"]
    PREP_F -->|sns:Publish| SNS_FAIL["SNS Failure Alert"]
    PREP_F --> FAIL

    subgraph Notification["Alert Delivery"]
        SNS["SNS Topic<br/>cnde-dev-pipeline-alerts"]
        EMAIL["Email Subscription"]
        SLACK["Slack / Lambda fan-out<br/>(future)"]
        RB["RUNBOOK.md<br/>On-call procedures"]
    end

    SNS_FAIL --> SNS
    SNS_OK --> SNS
    SNS --> EMAIL
    SNS --> SLACK
    EMAIL --> RB
```

---

## Failure Notification Sequence

```mermaid
sequenceDiagram
    participant SF as Step Functions
    participant PREP as PrepareFailureNotification
    participant SNS as SNS Topic
    participant E as Email / On-Call
    participant RB as RUNBOOK.md

    SF->>SF: EvaluateQuality (pass_rate = 95.0)
    SF->>PREP: Build notification payload
    Note over PREP: processing_date, pass_rate,<br/>execution_id, failed_state
    SF->>SNS: sns:Publish (States.JsonToString)
    SNS->>E: [RetailCo] Daily ETL FAILED
    E->>RB: Follow triage steps
    RB->>SF: Open execution by execution_id
    RB->>RB: Identify failed state → recovery action
    SF->>SF: PipelineFailed (terminal)
```

---

## SNS Message Structure

```mermaid
flowchart LR
    subgraph Payload["Failure Notification JSON"]
        PD["processing_date"]
        DS["dataset"]
        PR["pass_rate"]
        EID["execution_id"]
        FS["failed_state"]
        CAUSE["error.Cause"]
    end

    PREP["PrepareFailureNotification<br/>Pass state"] --> Payload
    Payload --> SNSP["sns:Publish<br/>TopicArn: cnde-dev-pipeline-alerts"]
    SNSP --> SUB["Email: your-email@example.com"]
```

---

## Key Components

| Component | Service | Role |
|-----------|---------|------|
| `daily_etl_with_sns.asl.json` | Step Functions | ASL with `PrepareFailureNotification` + `sns:Publish` tasks |
| `cnde-dev-pipeline-alerts` | SNS Topic | Central alert fan-out for pipeline events |
| Email subscription | SNS | Confirmed endpoint for on-call notifications |
| `PrepareFailureNotification` | Pass state | Builds structured JSON message from execution context |
| `NotifyFailureSNS` | Task (sns:Publish) | Publishes failure alert before terminal Fail |
| `PrepareSuccessNotification` | Pass state | Optional success message (disable in prod) |
| `RUNBOOK.md` | Documentation | Triage, common causes, recovery, escalation |
| Terraform module | IaC | `sns_topic_arn` parameter adds `sns:Publish` to execution role |

---

## S3 Paths & Data Flow

| Failed State | S3 Investigation Path | Runbook Action |
|--------------|----------------------|----------------|
| `StartGlueETL` | Glue logs; `raw/retail/orders/` | Check Glue job logs; replay partition |
| `RunQualityCheck` | `quarantine/retail/orders/` | Review quarantined records |
| `EvaluateQuality` | `metadata/quality-reports/` | Steward review; block curated publish |
| Recovery | `metadata/pipeline-runs/` | Document re-run with same `processing_date` |

### SNS Message Fields

| Field | Source | Purpose |
|-------|--------|---------|
| `processing_date` | `$.processing_date` | Identify affected data partition |
| `dataset` | `$.dataset` | Scope of failure (e.g., `retail/orders`) |
| `pass_rate` | `$.quality_result.Payload.pass_rate` | Quality SLO context |
| `execution_id` | `$$.Execution.Id` | Direct link to Step Functions console |
| `failed_state` | `$.error` or last state name | Triage starting point |

### Alert Flow Summary

```text
Pipeline failure (quality, Glue, input)
      │
      ▼
PrepareFailureNotification
      │  build JSON: {processing_date, pass_rate, execution_id, ...}
      ▼
sns:Publish → cnde-dev-pipeline-alerts
      │
      ├──► Email: [RetailCo] Daily ETL FAILED
      │
      └──► On-call → RUNBOOK.md
              ├── 1. Triage (5 min) — open execution by ID
              ├── 2. Common causes table
              ├── 3. Recovery — fix + re-run processing_date
              └── 4. Escalation — finance impact → platform lead
```

### IAM Addition

```json
{
  "Effect": "Allow",
  "Action": "sns:Publish",
  "Resource": "arn:aws:sns:us-east-1:{account}:cnde-dev-pipeline-alerts"
}
```

### Test Scenarios

| Input | Expected Alert | Final Status |
|-------|---------------|--------------|
| `mock_pass_rate: 95.0` | Failure email with pass_rate | `PipelineFailed` |
| `mock_pass_rate: 99.95` | Optional success email | `PipelineSucceeded` |

---

## Related Labs

- **Previous:** [Lab 6.2 – Retry and Error Branching](../lab-6.2-retry-error-branching/diagram.md)
- **Next:** Assignment 6 – Orchestration Capstone
