# Week 8 Lecture: Monitoring, Cost Optimization & Operations

**Duration:** 2 hours · **Module 8**

---

## Learning Objectives

By the end of this lecture you will:

1. Design observability for batch and event-driven data pipelines on AWS
2. Build CloudWatch dashboards and alarms aligned to pipeline SLIs and SLOs
3. Implement cost allocation with tagging and Cost Explorer reporting
4. Configure SNS alerting with severity-based routing and anomaly detection
5. Apply operational excellence practices to data platform incident response

---

## 1. Why Operations Matter for Data Platforms

Data pipelines are production systems. When they fail silently, downstream teams make decisions on stale or incorrect data—a failure mode worse than a visible outage.

### The Cost of Unobserved Pipelines

| Failure Mode | Business Impact |
|--------------|-----------------|
| ETL job fails overnight | Finance reports on incomplete data |
| Schema drift undetected | Athena queries return nulls; dashboards break |
| Duplicate ingestion | Revenue and conversion metrics inflated |
| Runaway Glue DPU usage | Unexpected AWS bill at month-end |
| Quarantine zone fills up | Bad records never reviewed; trust erodes |

**Operational excellence** for data engineering means: measure what matters, alert before users notice, allocate cost to owners, and respond with documented runbooks.

---

## 2. Observability for Data Pipelines

### Three Pillars Applied to Data Engineering

| Pillar | Data Platform Question | AWS Tools |
|--------|------------------------|-----------|
| **Metrics** | Is the job running? How long? How many records? | CloudWatch, Glue job metrics, custom metrics |
| **Logs** | Why did validation fail? What was the stack trace? | CloudWatch Logs, Glue job logs |
| **Traces** | Which step in the workflow failed? | X-Ray (optional), Step Functions execution history |

### Service-Level Indicators (SLIs) for Pipelines

Define measurable signals tied to business outcomes:

| SLI | Definition | Example Target |
|-----|------------|----------------|
| **Freshness** | Time from source event to curated availability | Orders in curated within 2 hours |
| **Completeness** | % of expected records processed | ≥ 99.9% of source rows |
| **Correctness** | Quality rule pass rate | ≥ 99.5% pass rate |
| **Availability** | Job success rate over 30 days | ≥ 99.5% successful runs |
| **Latency** | End-to-end pipeline duration | Glue job < 45 minutes P95 |

These SLIs become **SLOs** when you attach targets and error budgets (Module 4). Module 8 implements the **monitoring layer** that detects SLO breaches.

### What to Monitor by Layer

```text
┌─────────────────────────────────────────────────────────────┐
│ INGESTION          Lambda errors · S3 PUT rate · DLQ depth  │
├─────────────────────────────────────────────────────────────┤
│ PROCESSING         Glue job status · DPU hours · duration   │
├─────────────────────────────────────────────────────────────┤
│ QUALITY            Pass rate · quarantine count · rule hits │
├─────────────────────────────────────────────────────────────┤
│ ORCHESTRATION      Step Functions failures · retry count    │
├─────────────────────────────────────────────────────────────┤
│ STORAGE            S3 bucket size · request counts · IA %   │
├─────────────────────────────────────────────────────────────┤
│ ANALYTICS          Athena query scans · failed queries      │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Amazon CloudWatch for Data Platforms

### Native Metrics (No Code Required)

| Service | Key Metrics |
|---------|-------------|
| **AWS Glue** | `glue.driver.aggregate.numCompletedTasks`, `glue.ALL.s3.filesystem.read_bytes`, job run status |
| **AWS Lambda** | `Invocations`, `Errors`, `Duration`, `Throttles`, `ConcurrentExecutions` |
| **Amazon S3** | `BucketSizeBytes`, `NumberOfObjects`, `AllRequests` |
| **Step Functions** | `ExecutionsFailed`, `ExecutionsTimedOut`, `ExecutionTime` |
| **Amazon Athena** | Query execution metrics via API / workgroup settings |

### Custom Metrics

Publish pipeline-specific metrics from Glue jobs or Lambda:

```python
import boto3

cloudwatch = boto3.client("cloudwatch")

cloudwatch.put_metric_data(
    Namespace="CNDE/DataQuality",
    MetricData=[
        {
            "MetricName": "ValidationPassRate",
            "Dimensions": [
                {"Name": "Dataset", "Value": "retail/orders"},
                {"Name": "Environment", "Value": "dev"},
            ],
            "Value": 99.87,
            "Unit": "Percent",
        }
    ],
)
```

**Naming convention:** Use a consistent namespace (`CNDE/Pipeline`, `CNDE/DataQuality`) and dimensions (`Dataset`, `Environment`, `JobName`).

### CloudWatch Dashboards

Dashboards provide a single pane of glass for on-call engineers and data stewards:

- **Executive view:** Freshness, pass rate, cost trend (weekly)
- **Engineering view:** Job duration, errors, DPU utilization, DLQ depth
- **Per-dataset view:** Orders pipeline end-to-end health

Dashboards can be defined in JSON and deployed via Terraform (Lab 8.1).

### CloudWatch Alarms

Alarms evaluate metrics against thresholds and trigger actions:

| Alarm Type | Use Case |
|------------|----------|
| **Static threshold** | Glue job failure count > 0 in 5 minutes |
| **Anomaly detection** | Unexpected spike in S3 PUT requests or Lambda errors |
| **Composite alarm** | Multiple conditions (freshness AND pass rate) |
| **Metric math** | Pass rate = passed / (passed + quarantined) × 100 |

**Alarm states:** `OK` → `INSUFFICIENT_DATA` → `ALARM`. Always set `TreatMissingData` intentionally—missing Glue metrics may mean the job never started.

---

## 4. Alerting with Amazon SNS

### Alert Design Principles

1. **Actionable** — Every alert should tell the responder what to do
2. **Routed by severity** — Page for P1, email/Slack for P2/P3
3. **De-duplicated** — Avoid alert storms; use composite alarms or cooldowns
4. **Documented** — Link to runbook in alarm description

### Severity Model

| Severity | Example | Channel | Response Time |
|----------|---------|---------|---------------|
| **P1 – Critical** | Curated orders stale > 4 hours; finance deadline at risk | PagerDuty / SMS | 15 minutes |
| **P2 – High** | Glue job failed; auto-retry exhausted | Email + Slack | 1 hour |
| **P3 – Medium** | Pass rate below warning threshold | Email | Next business day |
| **P4 – Low** | Cost anomaly on dev environment | Weekly digest | Informational |

### SNS Architecture

```text
CloudWatch Alarm ──→ SNS Topic (cnde-alerts-critical)
                           │
                           ├── Email subscription (on-call)
                           ├── Lambda → Slack webhook
                           └── Lambda → PagerDuty (optional)

CloudWatch Alarm ──→ SNS Topic (cnde-alerts-warning)
                           └── Email (data stewards)
```

### Anomaly Detection

CloudWatch anomaly detection uses machine learning to establish a baseline and alert on deviations—useful for:

- Seasonal traffic patterns (retail peaks)
- Variable Glue job duration as data volume grows
- Unexpected cost spikes

Enable with `ANOMALY_DETECTION_BAND` in metric math expressions (Lab 8.2).

---

## 5. Cost Optimization for Data Lakes

### The AWS Cost Stack for Data Engineering

| Service | Typical Cost Driver | Optimization Lever |
|---------|--------------------|--------------------|
| **S3** | Storage volume, request count | Lifecycle policies, Intelligent-Tiering, Parquet |
| **Glue** | DPU-hours, crawlers | Job bookmarks, worker type tuning, schedule off-peak |
| **Athena** | Data scanned per query | Partition pruning, column selection, workgroup limits |
| **Lambda** | Invocations, duration, memory | Right-size memory, batch S3 events |
| **CloudWatch** | Custom metrics, log ingestion | Log retention, metric filters vs custom metrics |

### Cost Allocation Tags

Tags enable **showback/chargeback** to teams and projects:

| Tag Key | Purpose | Example |
|---------|---------|---------|
| `Project` | Course or business project | `cnde` |
| `Environment` | dev / staging / prod | `dev` |
| `CostCenter` | Finance billing unit | `CC-4521-retail-analytics` |
| `Dataset` | Data domain owner | `retail-orders` |
| `Student` | Lab attribution (course) | `jane-doe` |

Activate cost allocation tags in **Billing → Cost Allocation Tags**. Allow 24 hours for tags to appear in Cost Explorer.

### Cost Explorer Workflow

1. Filter by tag (`Project=cnde`, `Environment=dev`)
2. Group by service (S3, Glue, Athena)
3. Set granularity (daily during labs, monthly for capstone)
4. Export CSV for capstone `COST-ANALYSIS.md`

### FinOps Practices for Data Teams

1. **Budgets and alerts** — AWS Budgets at 80% and 100% of monthly limit
2. **Right-size before scale** — Profile Glue jobs before adding DPUs
3. **Query governance** — Athena workgroup with scan limits in dev
4. **Lifecycle everything** — Raw → IA → Glacier for compliance archives
5. **Review weekly** — 15-minute cost standup during active development

---

## 6. Operational Excellence Framework

### AWS Well-Architected: Operational Excellence Pillar

Applied to data platforms:

| Practice | Implementation |
|----------|----------------|
| **Operations as code** | Terraform for dashboards, alarms, SNS (Lab 8.1–8.2) |
| **Runbooks** | Documented incident response (Assignment 8) |
| **Learn from failures** | Blameless post-mortems within 48 hours |
| **Anticipate failure** | Step Functions retries, DLQs, circuit breakers |
| **Frequent, small changes** | Incremental ETL deploys with rollback plan |

### Incident Response Lifecycle

```text
Detect → Triage → Mitigate → Resolve → Post-Mortem → Improve
   ↑                                                      │
   └──────────────── Monitoring feedback loop ────────────┘
```

### Runbook Essentials

Every data platform runbook should include:

1. **Symptoms** — What users or alarms report
2. **Impact** — Which datasets and consumers are affected
3. **Diagnostic steps** — CloudWatch, Glue console, S3 paths to check
4. **Mitigation** — Replay job, disable publish, rollback Terraform
5. **Escalation** — Who to contact and when
6. **Recovery verification** — How to confirm data is healthy

Assignment 8 asks you to build runbooks for common pipeline incidents.

### On-Call Readiness Checklist

- [ ] Dashboards deployed and bookmarked
- [ ] Alarms tested (SNS test message received)
- [ ] Runbooks linked in alarm descriptions
- [ ] Access to Glue, S3, Step Functions, CloudWatch
- [ ] Known maintenance windows documented

---

## 7. End-to-End Monitoring Architecture

```text
┌──────────────┐    custom metrics     ┌─────────────────┐
│  Glue ETL    │ ────────────────────→ │   CloudWatch    │
│  Lambda      │    logs + metrics     │   Metrics/Logs  │
│  Step Funcs  │ ────────────────────→ └────────┬────────┘
└──────────────┘                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │   Dashboards    │
                                         │  (Engineering)  │
                                         └────────┬────────┘
                                                  │
                    ┌─────────────────────────────┼─────────────────────────────┐
                    ▼                             ▼                             ▼
            ┌──────────────┐              ┌──────────────┐              ┌──────────────┐
            │   Alarms     │              │ Cost Explorer│              │  EventBridge │
            │  (SLO-based) │              │  (tag-based) │              │  (optional)  │
            └──────┬───────┘              └──────────────┘              └──────────────┘
                   │
                   ▼
            ┌──────────────┐
            │     SNS      │
            │  (routing)   │
            └──────┬───────┘
                   │
         ┌─────────┼─────────┐
         ▼         ▼         ▼
      Email    Slack     PagerDuty
```

---

## 8. Industry Use Cases

### Banking
Regulatory reporting deadlines require freshness alarms with escalation to compliance officers. Cost allocation by business line supports internal chargeback.

### Healthcare
Audit logs and access metrics monitored for HIPAA. Anomaly detection on S3 GET patterns may indicate unauthorized access attempts.

### Retail
Black Friday scale requires anomaly-based alerts on ingestion volume—not static thresholds. Cost dashboards per marketing campaign tag.

### Government
Multi-agency cost allocation via tags. Operational dashboards shared with platform governance board.

---

## 9. Key Terminology

| Term | Definition |
|------|------------|
| **SLI** | Service-Level Indicator—a measurable aspect of service health |
| **SLO** | Service-Level Objective—a target value for an SLI |
| **Error budget** | Allowed SLO misses before feature freeze or escalation |
| **MTTR** | Mean Time to Recovery |
| **MTTD** | Mean Time to Detect |
| **Showback** | Reporting costs to teams without billing them |
| **Chargeback** | Actually billing teams for their AWS usage |
| **Runbook** | Step-by-step operational procedure for an incident type |
| **Anomaly detection** | ML-based baseline deviation alerting |

---

## 10. Discussion Questions

1. Should a failed Glue job always page on-call, or only when retries are exhausted?
2. How do you balance CloudWatch custom metric costs vs observability depth?
3. When is `TreatMissingData = breaching` appropriate vs `notBreaching`?
4. How would you prove to finance that the data platform team’s AWS spend is justified?
5. What metrics would you put on an executive dashboard vs an engineering dashboard?

---

## 11. This Week's Labs

| Lab | Goal |
|-----|------|
| **Lab 8.1** | Deploy CloudWatch dashboards for ETL pipelines |
| **Lab 8.2** | Configure SNS alerts and anomaly detection |
| **Lab 8.3** | Build cost reports with tags and Cost Explorer |

**Assignment 8:** Write an operations runbook for data platform incidents (3–4 pages).

---

## Further Reading

- [AWS CloudWatch Best Practices](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html)
- [AWS Glue Monitoring](https://docs.aws.amazon.com/glue/latest/dg/monitor-glue.html)
- [AWS Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html)
- [Google SRE Book – Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)

---

**Next:** [Lab 8.1 – CloudWatch Dashboards](../labs/lab-8.1-cloudwatch-dashboards/README.md)
