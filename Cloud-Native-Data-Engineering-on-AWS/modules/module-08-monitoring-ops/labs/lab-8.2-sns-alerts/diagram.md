# Lab 8.2 Architecture: SNS Alerts and Anomaly Detection

Severity-based alert routing from CloudWatch alarms to SNS topics, with critical and warning channels, optional Slack integration, and anomaly detection for ingestion error baselines.

---

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Metrics["Metric Sources"]
        GLUE[AWS/Glue<br/>Failed tasks]
        LAMB[AWS/Lambda<br/>Errors]
        DQ[CNDE/DataQuality<br/>Pass rate]
    end

    subgraph Alarms["CloudWatch Alarms"]
        A1[glue-failure-job<br/>Critical]
        A2[lambda-ingestion-errors<br/>Critical]
        A3[quality-pass-rate-low<br/>Warning]
        A4[lambda-errors-anomaly<br/>Warning + Anomaly Band]
    end

    subgraph SNS["SNS Topics"]
        CRIT[cnde-dev-alerts-critical]
        WARN[cnde-dev-alerts-warning]
    end

    subgraph Notify["Notification Channels"]
        EMAIL1[Email – On-call P1]
        EMAIL2[Email – Data Stewards P2]
        SLACK[Lambda → Slack<br/>optional]
    end

    GLUE --> A1
    LAMB --> A2 & A4
    DQ --> A3

    A1 & A2 --> CRIT
    A3 & A4 --> WARN

    CRIT --> EMAIL1
    WARN --> EMAIL2
    CRIT & WARN -.-> SLACK
```

---

## Key Components

| Component | AWS Service / Artifact | Role in Lab |
|-----------|------------------------|-------------|
| Critical SNS Topic | `cnde-dev-alerts-critical` | Routes P1 alarms (Glue failure, Lambda errors) |
| Warning SNS Topic | `cnde-dev-alerts-warning` | Routes P2/P3 alarms (quality SLO, anomaly) |
| Glue Failure Alarm | CloudWatch Alarm | Triggers when failed tasks > 0 |
| Lambda Error Alarm | CloudWatch Alarm | Static threshold: errors > 0 |
| Quality Pass Rate Alarm | CloudWatch Alarm | Warning when pass rate < 99% |
| Anomaly Detection Alarm | CloudWatch Alarm | `ANOMALY_DETECTION_BAND(m1, 2)` on Lambda errors |
| Email Subscriptions | SNS → Email | Requires confirmation click in inbox |
| Terraform Module | `infrastructure/modules/monitoring/main.tf` | Provisions topics, alarms, subscriptions |
| Escalation Matrix | `escalation-matrix.md` | Documents responders and SLAs |
| Test Alarm | `cnde-dev-test-lambda-error` | Dev-only alarm for end-to-end test |

---

## Data Flows

### Flow 1: Critical Alert (Glue Job Failure)

| Step | Component | Event |
|------|-----------|-------|
| 1 | Glue ETL | Job completes with `numFailedTasks > 0` |
| 2 | CloudWatch | `glue-failure-{job}` alarm → `ALARM` state |
| 3 | SNS Critical | Publishes JSON alarm message |
| 4 | Email | On-call receives notification within 2–5 minutes |
| 5 | Operator | Acknowledges per escalation matrix (15 min SLA) |

### Flow 2: Warning Alert (Quality SLO Breach)

```mermaid
sequenceDiagram
    participant QR as Quality Runner
    participant CW as CloudWatch
    participant AL as quality-pass-rate-low
    participant SNS as alerts-warning
    participant Email as Data Steward

    QR->>CW: ValidationPassRate = 97.5%
    CW->>AL: Metric below 99% threshold
    AL->>SNS: State = ALARM
    SNS->>Email: SLO breach notification
    Email->>Email: Steward investigates quarantine/
```

### Flow 3: Anomaly Detection vs Static Threshold

| Aspect | Static Alarm (`lambda-ingestion-errors`) | Anomaly Alarm (`lambda-errors-anomaly`) |
|--------|-------------------------------------------|----------------------------------------|
| Threshold | Fixed: errors > 0 | Dynamic band ±2σ from baseline |
| Baseline | N/A | Requires ~2 weeks production data |
| Use case | Hard zero-error SLO | Detect unusual spikes on noisy metrics |
| Lab behavior | Immediate trigger on test metric | Band visible; may need historical data |

### Flow 4: End-to-End Test (Lab Exercise)

| Step | Command / Action | Expected Result |
|------|------------------|-----------------|
| 1 | Create test alarm with threshold = 0 | Alarm in `OK` state |
| 2 | `put-metric-data` Errors = 1 | Metric published |
| 3 | Wait 2–5 minutes | Alarm → `ALARM` |
| 4 | SNS delivers email | Document subject + timestamp |
| 5 | Delete test alarm | Cleanup dev resources |

---

## Escalation Matrix (Reference)

| Alarm | Severity | Primary Responder | Escalation (30 min) |
|-------|----------|-------------------|---------------------|
| Glue job failure | P1 | Data engineer on-call | Platform lead |
| Lambda errors | P1 | Ingestion owner | Data engineer on-call |
| Pass rate low | P2 | Data steward | Data engineer |
| Anomaly detected | P3 | Data engineer | — |

---

## Alert Message Flow

```mermaid
flowchart LR
    M[Metric Breach] --> E[Alarm Evaluation<br/>1–5 min periods]
    E --> S[SNS Publish]
    S --> J[JSON: AlarmName,<br/>NewStateValue,<br/>NewStateReason]
    J --> EML[Email / Slack]
    EML --> RUN[Runbook – Assignment 8]
```
