# Assignment 6: Orchestration Design for Multi-Source Pipeline

**Due:** End of Week 6 · **Weight:** Part of Assignments (20%)

---

## Scenario

**RetailCo** is expanding beyond orders. Three source systems must land in the data lake daily:

| Source | Type | Landing Zone | SLA |
|--------|------|--------------|-----|
| **ERP orders** | Batch files (Module 2–3) | `raw/retail/orders/` | Curated by 05:00 UTC |
| **Supplier inventory** | SFTP CSV at 02:00 UTC | `raw/suppliers/inventory/` | Cleaned by 04:00 UTC |
| **Clickstream events** | Kinesis Firehose (continuous) | `raw/marketing/clickstream/` | Hourly rollup acceptable |

Module 4 quality rules differ per dataset. Module 5 curated models depend on **both** orders and inventory. Marketing clickstream feeds a separate `fact_events` table.

Current state: three independent Glue jobs started manually. Failures are discovered by finance, not engineering.

---

## Your Task

Design a **Step Functions-centric orchestration architecture** that coordinates all three sources with dependencies, retries, and notifications. No implementation required—design document only.

---

## Deliverables

Submit a document (4–5 pages) containing:

### 1. Executive Summary (½ page)

- Current risks of manual orchestration
- Proposed workflow overview
- Expected reliability improvements

### 2. State Machine Diagram (1 page)

Provide a Mermaid `stateDiagram-v2` or flowchart showing:

- Parallel ingestion branches where appropriate
- Synchronization point before curated build
- Quality gates per dataset
- Failure and warning paths
- SNS notification points

### 3. Execution Input Contract (½ page)

JSON schema for `StartExecution` input:

```json
{
  "processing_date": "2024-01-15",
  "sources": ["orders", "inventory", "clickstream"],
  "force_reprocess": false
}
```

Document output paths written to `metadata/pipeline-runs/`.

### 4. Dependency Matrix (1 page)

| Step | Depends On | Service | Timeout | Retry Policy |
|------|------------|---------|---------|--------------|
| Ingest inventory | SFTP arrival | Lambda / Transfer | | |
| Glue clean orders | Raw orders manifest | Glue | | |
| ... | | | | |

Include **critical path** analysis for 05:00 UTC curated SLA.

### 5. Error Handling Strategy (1 page)

For each failure type:

- Transient (throttle, timeout)
- Data quality (SLO breach)
- Configuration (IAM, missing file)
- Upstream source outage

Define: Retry? Branch? SNS severity? Halt curated publish?

### 6. Scheduling and Idempotency (½ page)

- EventBridge rules (cron expressions in UTC)
- How to prevent duplicate executions for same `processing_date`
- Catch-up logic after outage

### 7. IAM and Security (½ page)

- Step Functions execution role permissions (least privilege)
- Which roles may **not** start executions directly
- CloudTrail events to audit

### 8. Monitoring and Runbook (½ page)

- CloudWatch metrics and alarms
- Link to Lab 6.3 runbook structure
- Post-incident documentation requirements

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| State machine completeness and logical dependencies | 25 |
| Error handling and retry rationale | 25 |
| SLA / critical path analysis | 20 |
| IAM and operational monitoring | 15 |
| Clarity, diagram quality, professionalism | 15 |
| **Total** | **100** |

---

## Submission Format

- File: `assignment-06-{your-name}.md` or PDF
- Include Mermaid diagram source

---

## Tips

- Reference [Week 6 Lecture](../lectures/week-06-lecture.md)
- Inventory must complete before curated models joining orders + stock
- Clickstream can run in Parallel with batch sources
- Use Module 4 pass-rate thresholds in Choice states
- Do not put raw PII in SNS bodies (Module 7 preview)

---

**Next week:** [Module 7 – Security, Governance & Compliance](../../module-07-security-governance/README.md)
