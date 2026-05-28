## AI Automation & Agents with AWS Bedrock — Capstone Handbook

This handbook defines capstone options, milestones, demo expectations, and the grading rubric.

### Capstone goals

- Deliver a **production-minded** AI automation system with clear business value
- Demonstrate reliability: retries, fallbacks, idempotency, and safe replays
- Demonstrate governance: audit trail, redaction, approvals for risky actions
- Demonstrate operability: dashboards, alerts, runbook, cost controls

---

## Capstone options (choose one)

### Option 1 — AI Operations Assistant

**Problem**: Reduce time-to-triage for incidents and operational tickets.

**Typical flow**

- Ingest incident payload (EventBridge or API)
- Summarize + classify severity
- Route to owner/team
- Create action stub (e.g., ticket payload) with approval for high-risk actions
- Persist audit events + show dashboard

**Suggested stretch goals**

- Human-in-the-loop approvals for critical changes
- Memory: session context and historical incident summaries

### Option 2 — AI File Automation Platform

**Problem**: Automate document ingestion, classification, and routing.

**Typical flow**

- Upload to S3
- Trigger EventBridge/Lambda
- Extract metadata + classify
- Route to downstream workflow / queue
- Store audit trail + outputs

**Suggested stretch goals**

- Confidence thresholds with “needs review” path
- PII-safe logging and redaction

### Option 3 — Enterprise AI Workflow Engine

**Problem**: Provide a reusable orchestration engine for internal automation.

**Typical flow**

- API request defines workflow type + payload
- Step Functions executes:
  - model call(s)
  - validation
  - branching logic
  - actions
- Centralized governance + observability

**Suggested stretch goals**

- Template library of workflows with versioning
- Policy enforcement layer for tool/action safety

### Option 4 — Internal AI API Platform

**Problem**: Deliver reusable, governed AI endpoints for internal teams.

**Typical endpoints**

- `/classify`, `/summarize`, `/route`, plus one differentiated endpoint for your org

**Suggested stretch goals**

- Per-client rate limits and budgets
- Prompt versioning + evaluation gate for releases

---

## Required components (minimum bar)

Your capstone must include:

- **Orchestration**: Step Functions workflow (or equivalent) with error handling
- **AI integration**: Bedrock invocation with structured outputs
- **Validation**: deterministic schema validation + fallback path
- **Persistence**: DynamoDB or S3 for outputs and/or audit events
- **Observability**: CloudWatch dashboard + at least 1 alert
- **Governance**: audit trail + redaction policy + documented “what we do not log”
- **Cost controls**: request limits and a simple cost/risk write-up

---

## Milestones (recommended timeline)

### Milestone 1 (end of Week 6): Design freeze

- Architecture diagram + data flow
- API/workflow contracts (inputs/outputs)
- Failure modes and fallback plan
- Cost controls and governance plan

### Milestone 2 (end of Week 7): Feature complete

- Happy path works end-to-end
- Validation + fallbacks implemented
- Audit events emitted and stored
- Dashboard created

### Milestone 3 (Week 8): Demo-ready + operationalized

- Failure injection scenario prepared
- Alerts configured
- Runbook + demo script completed
- Final documentation polished

---

## Demo checklist (demo day)

### What you must show live

- **Happy path**: request/event → orchestration → outputs stored → response returned
- **Evidence of validation**: show schema enforcement
- **Audit trail**: retrieve audit events by correlation ID
- **Dashboard**: show key metrics (volume, errors, latency proxy, validation failures)
- **Cost controls**: show request limits and explain why they exist

### Failure scenario (required)

Demonstrate one of:

- Low confidence output triggers fallback/human review
- Validation failure triggers safe default
- Throttling/transient error triggers retries/backoff

---

## Final deliverables (what to submit)

- **Repo** with:
  - run instructions
  - architecture diagram(s)
  - state machine definition(s)
  - API docs (if applicable)
- **Governance review**:
  - what is logged vs not logged
  - approval policies (if any)
  - prompt versioning approach
- **Cost & risk analysis** (1–2 pages):
  - main cost drivers
  - request limits and throttles
  - key risks + mitigations
- **Ops readiness**:
  - dashboard screenshots/export
  - alert description and test evidence
  - runbook

---

## Capstone grading rubric (30 points)

### 1) Architecture & narrative (8 points)

- **8–7**: clear problem statement, success metrics, coherent architecture with sound tradeoffs
- **6–4**: generally correct but missing constraints or unclear data flows
- **3–0**: unclear scope or incoherent design

### 2) Reliability (8 points)

- **8–7**: retries/backoff, timeouts, fallbacks, idempotency strategy documented and demonstrated
- **6–4**: some reliability patterns present, incomplete failure handling
- **3–0**: minimal error handling; brittle workflow

### 3) Governance & safety (6 points)

- **6–5**: audit trail, redaction policy, least privilege, clear “no secrets/PII” stance
- **4–3**: partial governance, unclear logging boundaries
- **2–0**: missing audit/safety fundamentals

### 4) Observability & ops readiness (4 points)

- **4**: dashboards + alerts + runbook, demonstrates how to operate in production
- **3–2**: dashboards exist but alerts/runbook incomplete
- **1–0**: minimal observability

### 5) Cost controls (4 points)

- **4**: clear limits + explanation, identifies cost drivers, shows controls working
- **3–2**: mentions cost but weak controls
- **1–0**: no cost awareness

