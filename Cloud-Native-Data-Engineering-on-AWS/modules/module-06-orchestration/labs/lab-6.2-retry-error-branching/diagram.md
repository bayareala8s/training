# Lab 6.2: Retry Automation and Error Branching — Architecture Diagram

## Purpose

Extend the Lab 6.1 Step Functions pipeline with **Retry** blocks (exponential backoff + jitter) for transient Glue and Lambda failures, **Catch** handlers that preserve error context in `$.error`, and **Choice** states that implement three outcomes: full success (≥ 99.9%), degraded warning (≥ 99.0%), and hard failure (< 99.0%). Classify non-retriable errors (e.g., `AccessDenied`) to avoid pointless automated retries.

---

## State Machine Architecture

```mermaid
stateDiagram-v2
    [*] --> ValidateInput
    ValidateInput --> CheckInputValid
    CheckInputValid --> StartGlueETL: valid
    CheckInputValid --> ClassifyError: invalid

    StartGlueETL --> RunQualityCheck: success
    StartGlueETL --> StartGlueETL: retry transient
    StartGlueETL --> ClassifyError: catch after max retries

    RunQualityCheck --> EvaluateQuality: success
    RunQualityCheck --> RunQualityCheck: retry Lambda errors
    RunQualityCheck --> ClassifyError: catch

    EvaluateQuality --> PipelineSucceeded: pass >= 99.9
    EvaluateQuality --> QuarantineReview: pass >= 99.0
    EvaluateQuality --> NotifyFailure: pass < 99.0

    QuarantineReview --> PipelineSucceededWithWarning

    ClassifyError --> FailNoRetry: AccessDenied
    ClassifyError --> NotifyFailure: other errors

    PipelineSucceeded --> [*]
    PipelineSucceededWithWarning --> [*]
    NotifyFailure --> [*]
    FailNoRetry --> [*]
```

---

## Retry & Catch Flow

```mermaid
flowchart TD
    subgraph GlueState["StartGlueETL"]
        G1["Attempt 1"]
        G2["Attempt 2 (backoff 2×)"]
        G3["Attempt 3 (backoff 4×)"]
        GC["Catch → $.error"]
    end

    G1 -->|TaskFailed / Throttling| G2
    G2 -->|TaskFailed / Throttling| G3
    G3 -->|Still failing| GC

    subgraph Errors["ErrorEquals"]
        TF["TaskFailed"]
        TH["ThrottlingException"]
        CR["ConcurrentRunsExceededException"]
    end

    subgraph QualityBranch["EvaluateQuality"]
        Q1{"pass_rate?"}
        Q1 -->|>= 99.9| SUCC["PipelineSucceeded"]
        Q1 -->|>= 99.0| WARN["QuarantineReview<br/>→ PipelineSucceededWithWarning"]
        Q1 -->|< 99.0| FAIL["NotifyFailure"]
    end

    GC --> CE{"ClassifyError<br/>AccessDenied?"}
    CE -->|yes| NORETRY["FailNoRetry<br/>No further retries"]
    CE -->|no| FAIL
```

---

## Execution Scenarios

```mermaid
sequenceDiagram
    participant SF as Step Functions
    participant G as Glue ETL
    participant L as Validation Lambda

    Note over SF,G: Scenario 1: Transient Glue failure
    SF->>G: StartGlueETL (attempt 1)
    G-->>SF: ThrottlingException
    SF->>SF: Retry with backoff (2s → 4s → 8s)
    SF->>G: StartGlueETL (attempt 2)
    G-->>SF: SUCCEEDED

    Note over SF,L: Scenario 2: Degraded quality (99.5%)
    SF->>L: RunQualityCheck
    L-->>SF: {pass_rate: 99.5}
    SF->>SF: EvaluateQuality → QuarantineReview
    SF-->>SF: PipelineSucceededWithWarning ($.warning populated)

    Note over SF,G: Scenario 3: Non-retriable error
    SF->>G: StartGlueETL
    G-->>SF: AccessDenied
    SF->>SF: ClassifyError → FailNoRetry (immediate)
```

---

## Key Components

| Component | Location | Role |
|-----------|----------|------|
| `daily_etl_with_retry.asl.json` | `src/` | Extended state machine with Retry, Catch, Choice |
| `StartGlueETL` Retry | ASL block | MaxAttempts: 3, BackoffRate: 2.0, JitterStrategy |
| `RunQualityCheck` Retry | ASL block | MaxAttempts: 2 for Lambda service errors |
| `ClassifyError` | Choice state | Routes `AccessDenied` to `FailNoRetry` |
| `EvaluateQuality` | Choice state | Three-tier SLO: 99.9% / 99.0% / fail |
| `QuarantineReview` | Pass state | Warning path; triggers steward review |
| `PipelineSucceededWithWarning` | Succeed state | Degraded SLO; `$.warning` in output |
| `FailNoRetry` | Fail state | Non-retriable IAM/permission errors |

---

## S3 Paths & Data Flow

| Scenario | S3 Impact | Pipeline Outcome |
|----------|-----------|------------------|
| Glue retry succeeds | `cleaned/retail/orders/` written after retry | `PipelineSucceeded` |
| pass_rate 99.5% | Quarantine may have records; cleaned partially written | `PipelineSucceededWithWarning` |
| pass_rate 98.0% | Quarantine populated; curated publish blocked | `NotifyFailure` |
| AccessDenied on Glue | No S3 writes | `FailNoRetry` (immediate) |

### Retry Policy Table

| State | MaxAttempts | BackoffRate | IntervalSeconds | Errors Retried |
|-------|-------------|-------------|-----------------|----------------|
| `StartGlueETL` | 3 | 2.0 | 2 | `TaskFailed`, `ThrottlingException`, `ConcurrentRunsExceededException` |
| `RunQualityCheck` | 2 | 2.0 | 1 | Lambda service errors |

### SLO Thresholds

| Pass Rate | State Transition | Business Meaning |
|-----------|-----------------|------------------|
| ≥ 99.9% | `PipelineSucceeded` | Full success; publish curated |
| ≥ 99.0% | `QuarantineReview` → `PipelineSucceededWithWarning` | Degraded; steward review required |
| < 99.0% | `NotifyFailure` | Hard failure; block downstream |

### Data Flow Summary

```text
StartGlueETL
      ├── success ──► RunQualityCheck ──► EvaluateQuality
      │                                      ├── >= 99.9% ──► SUCCEED
      │                                      ├── >= 99.0% ──► WARNING (quarantine review)
      │                                      └── < 99.0%  ──► FAIL
      │
      ├── retry (transient) ──► up to 3 attempts with backoff
      │
      └── catch ──► ClassifyError
                        ├── AccessDenied ──► FailNoRetry
                        └── other ──► NotifyFailure
```

---

## Related Labs

- **Previous:** [Lab 6.1 – Step Functions ETL](../lab-6.1-step-functions-etl/diagram.md)
- **Next:** [Lab 6.3 – SNS Failure Handling](../lab-6.3-sns-failure-handling/diagram.md)
