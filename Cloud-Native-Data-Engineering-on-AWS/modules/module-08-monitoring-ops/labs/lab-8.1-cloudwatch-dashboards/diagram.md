# Lab 8.1 Architecture: CloudWatch Dashboards for ETL Pipelines

Operations dashboard aggregating native AWS metrics (Glue, Lambda, Step Functions, S3) and custom application metrics (`CNDE/DataQuality`) into a single CloudWatch view for pipeline health and SLO tracking.

---

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Pipelines["Data Platform Pipelines"]
        GLUE[AWS Glue Jobs<br/>cnde-orders-etl<br/>cnde-inventory-etl]
        LAMB[Lambda Ingestion<br/>cnde-dev-ingestion]
        SF[Step Functions<br/>ETL Orchestration]
        QR[Quality Runner<br/>Module 4]
    end

    subgraph Metrics["CloudWatch Metrics"]
        MG[AWS/Glue]
        ML[AWS/Lambda]
        MS[AWS/States]
        MS3[AWS/S3]
        MC[CNDE/DataQuality<br/>custom namespace]
    end

    subgraph Dashboard["Observability Layer"]
        JSON[etl_pipeline_dashboard.json]
        CW[CloudWatch Dashboard<br/>cnde-dev-etl-pipeline]
        LI[Logs Insights Widget<br/>Glue ERROR lines]
    end

    subgraph Deploy["Deployment Paths"]
        CLI[AWS CLI put-dashboard]
        TF[Terraform monitoring module]
    end

    GLUE --> MG
    LAMB --> ML
    SF --> MS
    QR --> MC
    GLUE --> LI

    S3[(S3 Data Lake)] --> MS3

    MG & ML & MS & MS3 & MC --> CW
    JSON --> CLI & TF
    CLI & TF --> CW
```

---

## Key Components

| Component | AWS Service / Artifact | Role in Lab |
|-----------|------------------------|-------------|
| CloudWatch Dashboard | Amazon CloudWatch | Single-pane view of pipeline SLIs and SLOs |
| Dashboard JSON | `src/etl_pipeline_dashboard.json` | Dashboard-as-code widget definitions |
| Glue Metrics | `AWS/Glue` namespace | Job failures, duration, DPU utilization |
| Lambda Metrics | `AWS/Lambda` namespace | Errors, duration, throttles for ingestion |
| Step Functions Metrics | `AWS/States` namespace | Execution success/failure counts |
| S3 Metrics | `AWS/S3` namespace | `BucketSizeBytes` for capacity trends |
| Custom Metrics | `CNDE/DataQuality` | `ValidationPassRate`, `QuarantinedRecords` |
| Logs Insights | CloudWatch Logs | Recent ERROR lines from Glue log groups |
| Terraform Module | `infrastructure/modules/monitoring/` | IaC deployment path for dashboard + alarms |
| SLO Annotation | Dashboard widget config | 99% pass-rate horizontal threshold |

---

## Data Flows

### Flow 1: Metric Emission → Dashboard Widget

| Step | Source | Metric | Dashboard Widget |
|------|--------|--------|------------------|
| 1 | Glue job run | `glue.driver.aggregate.numFailedTasks` | Glue Job Failures |
| 2 | Glue job run | `glue.driver.aggregate.elapsedTime` | Glue Job Duration |
| 3 | Lambda invocation | `Errors`, `Duration` | Lambda Health |
| 4 | Quality runner | `ValidationPassRate` (custom) | Data Quality Pass Rate |
| 5 | Quality runner | `QuarantinedRecords` (custom) | Quarantine Count |
| 6 | Step Functions | `ExecutionsFailed` | Orchestration Status |
| 7 | S3 bucket | `BucketSizeBytes` | Storage Trend |

### Flow 2: Custom Metric Publishing

```mermaid
sequenceDiagram
    participant QR as Quality Runner
    participant CW as CloudWatch
    participant DB as Dashboard

    QR->>QR: Validate dataset (Module 4)
    QR->>CW: put_metric_data<br/>Namespace=CNDE/DataQuality
    Note over CW: ValidationPassRate=99.92<br/>QuarantinedRecords=12
    CW->>DB: Aggregate metric datapoints
    DB->>DB: Render widgets (≤5 min latency)
```

### Flow 3: Dashboard Deployment

| Step | Method | Action |
|------|--------|--------|
| 1 | Developer | Resolves `ACCOUNT_ID` and job names in JSON |
| 2a | CLI path | `aws cloudwatch put-dashboard` |
| 2b | Terraform path | `terraform apply -target=module.monitoring` |
| 3 | Console | Verify widgets in CloudWatch → Dashboards |
| 4 | Operator | Add SLO annotation at 99% on pass-rate widget |

---

## Widget Categories

| Category | Purpose | Alert Integration |
|----------|---------|-------------------|
| Pipeline health | Glue failures, Lambda errors | Lab 8.2 alarms |
| Performance | Job duration, Lambda latency | Capacity planning |
| Data quality | Pass rate, quarantine volume | SLO breach → SNS warning |
| Orchestration | Step Functions success rate | Critical path monitoring |
| Capacity | S3 storage growth | Cost correlation (Lab 8.3) |
| Diagnostics | Logs Insights ERROR filter | Incident triage |

---

## SLI → SLO Mapping

| SLI (Indicator) | SLO (Objective) | Widget |
|-----------------|-----------------|--------|
| ETL success rate | Zero failed Glue tasks per run | Glue Job Failures |
| Ingestion reliability | Lambda error count = 0 | Lambda Health |
| Data quality pass rate | ≥ 99% validation pass | Pass Rate + annotation |
| Quarantine volume | Trend visibility (no hard SLO) | Quarantine Count |
