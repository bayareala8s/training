# Assignment 8: Operations Runbook for Data Platform Incidents

**Due:** End of Week 8 · **Weight:** Part of Assignments (20%)

---

## Scenario

**RetailCo** (from Assignments 1 and 4) now runs a production data platform on AWS with:

- Daily Glue ETL for orders and inventory (curated by 5 AM UTC for finance)
- Event-driven clickstream ingestion via Lambda and S3 events
- Step Functions orchestration with retry logic
- CloudWatch dashboards and SNS alerts (Labs 8.1–8.2)
- Data quality SLAs with quarantine routing (Assignment 4)

Last month, three incidents caused business impact:

1. **Glue OOM failure** — Orders ETL failed at 2 AM; finance discovered missing data at 7 AM
2. **Silent schema drift** — New `discount_code` column broke Athena queries; no alert fired
3. **Cost spike** — A student re-ran full-history Glue jobs in dev, exceeding the team budget

Your platform lead asks for a formal **Operations Runbook** so on-call engineers can detect, triage, and resolve incidents consistently.

---

## Your Task

Write an operations runbook (3–4 pages) covering detection, response, and recovery for data platform incidents. The runbook becomes the team's operational reference linked from CloudWatch alarm descriptions.

---

## Deliverables

Submit a document (3–4 pages) containing:

### 1. Executive Summary (½ page)

- Why operational runbooks matter for data platforms
- Scope of this runbook (services, datasets, environments)
- On-call roles and escalation overview

### 2. Monitoring and Alert Reference (½ page)

Document the monitoring stack deployed in Labs 8.1–8.2:

| Component | Name / ARN Pattern | Purpose |
|-----------|-------------------|---------|
| Dashboard | `cnde-dev-etl-pipeline` | |
| SNS Critical | `cnde-dev-alerts-critical` | |
| SNS Warning | `cnde-dev-alerts-warning` | |
| Glue failure alarm | `cnde-dev-glue-failure-*` | |
| Quality SLO alarm | `cnde-dev-quality-pass-rate-low` | |

Include links or paths to dashboard JSON and Terraform module.

### 3. Incident Runbooks (2 pages minimum)

Write a **complete runbook** for each incident type below. Each runbook must include:

- **Symptoms** — What alarms, users, or dashboards report
- **Impact** — Affected datasets, consumers, and SLOs
- **Severity** — P1/P2/P3 with response time SLA
- **Diagnostic steps** — Numbered checks (CloudWatch, Glue console, S3 paths, logs)
- **Mitigation** — Immediate actions to limit blast radius
- **Recovery** — Steps to restore healthy data flow
- **Verification** — How to confirm resolution
- **Escalation** — When and whom to contact

#### Runbook A: Glue ETL Job Failure

Cover: job failure alarm, CloudWatch Logs (`/aws-glue/jobs/error`), DPU/memory issues, retry via Step Functions, manual re-run with job bookmarks.

Reference paths:

```text
s3://retailco-prod-datalake/cleaned/retail/orders/
s3://retailco-prod-datalake/quarantine/retail/orders/
CloudWatch: AWS/Glue → glue.driver.aggregate.numFailedTasks
```

#### Runbook B: Data Freshness / SLA Breach

Cover: curated data not updated by SLO deadline, Step Functions stuck, upstream source delay vs pipeline failure, finance notification path.

Include decision tree:

```text
Is Glue job running? ──No──→ Check schedule / Step Functions
        │
       Yes
        │
Is job progressing? ──No──→ Check DPU, data volume, logs
        │
       Yes
        │
Is source data present in raw/? ──No──→ Escalate to source team
        │
       Yes──→ Investigate transform logic / quality quarantine
```

#### Runbook C: Data Quality SLO Breach

Cover: pass rate alarm, quarantine zone growth, halt curated publish (circuit breaker), steward review process. Reference Assignment 4 SLAs.

#### Runbook D: Unexpected Cost Spike

Cover: Cost Explorer investigation, identifying runaway Glue jobs, Athena scan anomalies, tagging gaps, budget alert response.

### 4. Post-Incident Process (½ page)

Define the **blameless post-mortem** template:

| Section | Content |
|---------|---------|
| Incident summary | One paragraph |
| Timeline | Detect → mitigate → resolve (UTC timestamps) |
| Root cause | Technical and process factors |
| Impact | Duration, datasets affected, downstream effects |
| Action items | Owner, due date, preventive measure |
| Lessons learned | What monitoring/runbook gaps were exposed |

Require post-mortems within **48 hours** for P1/P2 incidents.

### 5. On-Call Quick Reference (½ page)

Provide a single-page cheat sheet:

- Dashboard URL pattern
- Key CLI commands (list alarms, tail Glue logs, check S3 prefix)
- Escalation phone/email matrix
- Maintenance window policy
- "When in doubt" default action (e.g., halt curated publish)

**Example CLI block to include:**

```bash
# Check Glue job status
aws glue get-job-runs --job-name cnde-orders-etl --max-results 3

# Tail recent Glue errors
aws logs filter-log-events \
  --log-group-name /aws-glue/jobs/error \
  --filter-pattern "ERROR" \
  --limit 20

# Verify curated partition exists
aws s3 ls s3://BUCKET/curated/sales/fact_orders/year=YYYY/month=MM/day=DD/
```

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Runbook completeness (all 4 incident types) | 30 |
| Diagnostic steps actionable and ordered | 20 |
| Alignment with Labs 8.1–8.2 monitoring stack | 15 |
| Escalation and severity model | 15 |
| Post-mortem process | 10 |
| Clarity, professionalism, quick reference | 10 |
| **Total** | **100** |

---

## Submission Format

- File: `assignment-08-{your-name}.md` or PDF
- Optional: link runbook sections in Terraform alarm descriptions (screenshot)
- Submit via your learning platform

---

## Tips

- Reference [Week 8 Lecture](../lectures/week-08-lecture.md) SLI/SLO and alerting concepts
- Use imperative voice in diagnostic steps ("Check X", "Run Y", not "You might want to")
- Link alarm descriptions to runbook sections (production best practice)
- Tie severity to business impact—finance deadline makes orders freshness P1
- Include "do no harm" guidance: never delete raw data; prefer quarantine over silent drops

---

**Next week:** [Module 9 – Data Engineering for AI & ML](../../module-09-ai-ml-data/README.md)
