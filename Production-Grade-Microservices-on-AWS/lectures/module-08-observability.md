# Module 8 — Observability, SLOs & Incident Response

**Production-Grade Microservices on AWS · BayAreaLa8s**

| | |
|---|---|
| **Duration** | 90 minutes lecture + 4 hours lab |
| **Week** | 8 of 10 |
| **Prerequisites** | Module 4 (ECS deploy) |

---

## Learning Objectives

Students will be able to:

1. Apply the **three pillars**: logs, metrics, traces.
2. Use **CloudWatch** log groups, metrics, dashboards, and alarms for ECS services.
3. Define **SLI**, **SLO**, and **error budget** for a critical API.
4. Execute a structured **incident response** lifecycle.
5. Correlate a failed order across User, Product, Order, and Notification using logs.

---

## Session Agenda

| Segment | Time | Topic |
|---------|------|--------|
| Three pillars | 20 min | Logs, metrics, traces |
| CloudWatch deep dive | 25 min | Course log groups, Container Insights |
| SLOs & error budgets | 20 min | Order POST example |
| Incident response | 20 min | Detect → postmortem |
| Demo & wrap-up | 5 min | Find failed order in logs |

**Diagrams:** [14-observability](../docs/diagrams/14-observability.md) · [AWS observability stencil](../docs/diagrams/aws-stencils/png/14-observability-cloudwatch-detail.png)

---

## 1. The Three Pillars (20 minutes)

### 1.1 Why observability matters in microservices

A single user click may traverse **4+ services**. Without correlation, debugging is guesswork.

| Pillar | Question | Tool (course) |
|--------|----------|---------------|
| **Logs** | What happened? | CloudWatch Logs |
| **Metrics** | How much / how fast? | CloudWatch Metrics, ALB metrics |
| **Traces** | Where did time go? | X-Ray (extension) |

### 1.2 Logs — structured vs unstructured

**Unstructured:**

```
User logged in successfully
```

**Structured (JSON):**

```json
{
  "level": "info",
  "service": "order-service",
  "order_id": "ord_123",
  "duration_ms": 45,
  "trace_id": "abc-def"
}
```

**Benefits:** Filter in CloudWatch Logs Insights, index in OpenSearch.

### 1.3 Metrics — types

| Type | Example |
|------|---------|
| **Counter** | Total orders placed |
| **Gauge** | Current queue depth |
| **Histogram** | Request latency distribution |

**RED method** (services): Rate, Errors, Duration.

**USE method** (resources): Utilization, Saturation, Errors.

### 1.4 Traces (extension)

**AWS X-Ray** or OpenTelemetry: single trace ID across ALB → Order → Product.

**Instrumentation:** SDK in FastAPI middleware; propagate `X-Amzn-Trace-Id` or W3C `traceparent`.

---

## 2. Amazon CloudWatch (25 minutes)

### 2.1 Log architecture

Course tasks ship stdout to:

```
Log group: /ecs/ms-course-dev
Stream prefix: user-service | product-service | order-service | notification-service
```

Configured in task definition `logConfiguration` (`ecs.tf`).

### 2.2 Logs Insights query examples

**Errors in order service (last hour):**

```sql
fields @timestamp, @message
| filter @logStream like /order-service/
| filter @message like /ERROR/
| sort @timestamp desc
| limit 50
```

**Slow requests (if JSON logged):**

```sql
fields @timestamp, duration_ms, path
| filter duration_ms > 1000
```

### 2.3 Metrics

| Source | Metrics |
|--------|---------|
| **ECS** | CPUUtilization, MemoryUtilization |
| **ALB** | TargetResponseTime, HTTPCode_Target_5XX_Count |
| **Custom** | `PutMetricData` for business KPIs |

**Container Insights** enabled on cluster—richer dashboards.

### 2.4 Dashboards & alarms

| Artifact | Purpose |
|----------|---------|
| **Dashboard** | Single pane for cohort demo |
| **Alarm** | CPU > 80% for 5 min → SNS → email/Slack |
| **Composite alarm** | Multiple conditions |

**SNS topic** — extension for on-call integration (PagerDuty).

### 2.5 EventBridge audit logs

OrderPlaced rules may target CloudWatch Logs for **event audit trail** (Module 5).

---

## 3. SLOs & Error Budgets (20 minutes)

### 3.1 Definitions

| Term | Meaning |
|------|---------|
| **SLI** | Measurable indicator (e.g. % successful `POST /orders`) |
| **SLO** | Target for SLI (e.g. 99.5% over 30 days) |
| **Error budget** | Allowed failure (0.5% ≈ 3.6 hours downtime/month) |

### 3.2 Example: Order placement SLO

| SLI | `(successful orders) / (total order attempts)` |
| SLO | **99.5%** monthly |
| Measurement window | Rolling 30 days |

**When budget burned:** Freeze features; focus on reliability (Google SRE book principle).

### 3.3 SLI pitfalls

- Measuring only 200 responses (ignore client errors caused by server)
- Ignoring synthetic monitoring
- No exclusion for planned maintenance (define policy)

### 3.4 Diagram

Walk [14-observability](../docs/diagrams/14-observability.md) SLO flow: SLI → SLO → Error budget.

---

## 4. Incident Response (20 minutes)

### 4.1 Lifecycle

```
Detect → Triage → Mitigate → Resolve → Postmortem (blameless)
```

| Phase | Actions |
|-------|---------|
| **Detect** | Alarm fires, customer report, synthetic test |
| **Triage** | Severity, owner, comms channel |
| **Mitigate** | Rollback, scale up, disable feature flag |
| **Resolve** | Root cause fix deployed |
| **Postmortem** | Timeline, contributing factors, action items |

### 4.2 Severity levels (example)

| Sev | Description | Response |
|-----|-------------|----------|
| **SEV1** | Checkout down | All hands, exec comms |
| **SEV2** | Degraded latency | On-call + lead |
| **SEV3** | Minor bug | Next business day |

### 4.3 Runbooks

Document for Order service:

1. Check ALB target health
2. Check ECS service events
3. Query CloudWatch for `order-service` errors
4. Verify Product Service health
5. Rollback to previous task definition revision

### 4.4 Blameless postmortems

Focus on **systems and processes**, not individuals. Required for learning culture.

---

## 5. Demo & Wrap-Up (5 minutes)

### Instructor demo

1. Introduce intentional failure (wrong `product_id`).
2. Show 404 in order logs.
3. Show ALB 4xx metrics spike.
4. Walk mitigation: fix client, redeploy if needed.

```bash
aws logs tail /ecs/ms-course-dev --follow --filter-pattern "order"
```

---

## Lab & Assignment

- **Lab 08:** [`labs/module-08/README.md`](../labs/module-08/README.md)
- **Assignment 08:** [`assignments/module-08.md`](../assignments/module-08.md)

### Summary

You cannot operate what you cannot **see**. Microservices require **structured logs**, **service-level metrics**, and clear **SLOs** before scaling teams.

---

## Discussion Questions

1. What SLI would you choose for Notification email delivery?
2. Logs vs metrics—when is each sufficient alone?
3. How does error budget change prioritization for product managers?
4. What should a blameless postmortem include?

---

*BayAreaLa8s · Production-Grade Microservices on AWS*
