## Week 6 — Observability, Governance & AI Safety

This week makes the system operable in production: **audit trails, dashboards, alerts, redaction, and human-in-the-loop patterns**.

### Learning objectives

By the end of Week 6, students can:

- Define what to log vs what never to log for AI systems
- Build an audit trail keyed by correlation IDs
- Create CloudWatch dashboards and at least one alert
- Design human-in-the-loop triggers for high-risk or low-confidence outcomes
- Add cost awareness (budgets/alerts and request limiting policies)

### Core concepts (lecture notes)

- **Observability requirements**
  - You need to explain: what happened, why, how long it took, and what it cost (or cost proxy)
  - Correlation IDs connect API requests, workflow runs, and audit records
- **Audit trails**
  - Store metadata events: timestamps, model ID, sizes, validation status, routing decisions
  - Make audit records searchable by correlation ID and timeframe
- **Safety and redaction**
  - Never log secrets or regulated content
  - Prefer logging sizes/hashes/classifications instead of raw text
- **Governance**
  - Prompt changes should be reviewed and evaluated before release
  - High-risk actions require approval gates
- **Cost controls**
  - Bound inputs/outputs, enforce quotas, alert on unusual volume/error rates

### In-class activities (45–60 min)

- **Activity A — Logging boundary definition**
  - Define: allowed-to-log fields and forbidden-to-log fields for your system.
- **Activity B — Runbook mini-workshop**
  - Write a 1-page runbook: symptoms → checks → mitigations for common incidents.

### Demos (instructor-led)

- **Demo 1**: Emit an “AI interaction event” and store it (DynamoDB/S3).
- **Demo 2**: CloudWatch dashboard + alarm; show correlation ID tracing end-to-end.
- **Demo 3 (optional)**: Human approval branch in a workflow (simulation).

### Hands-on labs (students)

Complete:

- `LABS_GUIDE.md` → **Week 6 Labs**: Lab 6.1 and Lab 6.2

### Assignment (due end of week)

Submit:

- **Observability**
  - dashboard(s) and at least one alert
  - evidence of alert test
- **Auditability**
  - audit event schema + stored records
  - retrieval by correlation ID
- **Governance & safety**
  - logging/redaction policy
  - human-in-the-loop trigger definition (when to require approval)
- **Ops report**
  - 1–2 pages: what you monitor, alerts, and response steps

Rubric:

- See `ASSIGNMENTS_AND_RUBRICS.md` → **Week 6**

### Quiz (5–10 questions)

1. What is a correlation ID and how is it used?
2. List three fields that are safe to store in an audit record.
3. List two things that should never be logged.
4. What should an alert detect in an AI workflow system?
5. When would you require human approval in an automation pipeline?

### Architecture diagram

- [`diagrams/drawio/07-week06.drawio`](../diagrams/drawio/07-week06.drawio) · [PNG](../diagrams/png/07-week06.png) · [SVG](../diagrams/svg/07-week06.svg)

Review the **governance checklist** and **never log** boxes before the audit lab.

### Student diagrams

- **Cheat sheet:** [cheat-week06](../diagrams/student/png/cheat-week06.png) — must log / never log / query audit
- **Anti-pattern:** [pattern-week06](../diagrams/student/png/pattern-week06.png) — log everything vs structured audit

### Expected artifacts (portfolio-ready)

