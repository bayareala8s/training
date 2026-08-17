## Week 8 — Capstone Build & Demo

Week 8 is a build sprint and demo week. The focus is **scope control, evidence, and production readiness**.

### Learning objectives

By the end of Week 8, students can:

- Deliver a capstone that meets the minimum bar (orchestration, validation, audit, dashboards, cost controls)
- Run a demo with a prepared happy path and a prepared failure scenario
- Present architecture tradeoffs, risk mitigations, and operational readiness

### Capstone requirements (minimum bar)

Your capstone must include:

- Orchestration (Step Functions or equivalent) with error handling
- Bedrock integration with structured outputs
- Deterministic validation + safe fallback handling
- Persistence (DynamoDB or S3) for outputs and/or audit events
- CloudWatch dashboard + at least one alert
- Governance: audit trail + logging/redaction policy
- Cost controls: request limits and a short cost/risk analysis

See:

- `CAPSTONE_HANDBOOK.md` (options, milestones, rubric, demo checklist)

### Hands-on labs (students)

Complete capstone labs in [`labs/week08/`](../labs/week08/README.md):

| Option | Track | Endpoint |
|--------|-------|----------|
| A | Incident triage | `POST /capstone/incident` |
| B | Document classification | `POST /capstone/document` |
| C | Approval workflow | `POST /capstone/approval/request` + `/decide` |
| D | Enterprise agent | `POST /capstone/agent` |

```bash
cd labs && ./scripts/start.sh && source .stack.env
./scripts/verify-capstone.sh
```

Pick **one option** to extend for your portfolio submission, or demo all four.

- **Day 1**: finalize scope; confirm contracts (inputs/outputs) and success metrics
- **Day 2**: wire happy path end-to-end; persist outputs; add correlation ID tracing
- **Day 3**: add validation + fallbacks; add retries/backoff; implement idempotency where needed
- **Day 4**: audit trail + dashboard + alert; write runbook; prep demo script

### Demo expectations

You should be able to show:

- **Happy path**: request/event → workflow → outputs stored → response
- **Evidence of validation**: schema enforcement and/or low-confidence path
- **Audit retrieval**: search by correlation ID
- **Dashboard**: volume, errors, latency proxy, validation failures, retries
- **Cost controls**: show your limits and explain the rationale
- **Failure scenario**: one controlled failure and how the system responds safely

### Final submission package

Submit:

- Repo link with run instructions and architecture diagram(s)
- Workflow definition(s) and API docs (if applicable)
- Governance review (logging boundaries, approvals, prompt versioning approach)
- Cost & risk analysis (1–2 pages)
- Ops readiness artifacts:
  - dashboard screenshots/export
  - alert description + test evidence
  - runbook

### Architecture diagram

- [`diagrams/drawio/09-week08.drawio`](../diagrams/drawio/09-week08.drawio) · [PNG](../diagrams/png/09-week08.png) · [SVG](../diagrams/svg/09-week08.svg)
- Course reference: [`01-reference`](../diagrams/png/01-reference.png)

Project during capstone kickoff — students pick one option and map to the **minimum bar**.

### Student diagrams

- **Cheat sheet:** [cheat-week08](../diagrams/student/png/cheat-week08.png) — minimum bar, deliverables, demo script

### Grading

- See `CAPSTONE_HANDBOOK.md` → **Capstone grading rubric (30 points)**

### Quiz (5–10 questions)

1. What are the seven components of the capstone minimum bar?
2. What should you demonstrate in a controlled failure scenario during your demo?
3. Why is scope control important in the final week?
4. What belongs in an ops runbook for your capstone system?
5. How do lab options A–D map to the handbook capstone tracks?
6. What evidence should your portfolio submission include beyond source code?

Instructor answer key: `INSTRUCTOR_QUIZ_ANSWERS.md` → Week 8.

### Optional extensions (if time permits)

- Prompt evaluation gate for releases (golden set + score thresholds)
- Deeper policy enforcement for tool actions (approval branches)
- Better cost controls (per-client quotas, caching, batching)

