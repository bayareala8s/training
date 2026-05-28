## AI Automation & Agents with AWS Bedrock — Assignments & Rubrics

This document defines weekly assignments, expected artifacts, and consistent rubrics.

### Submission package (recommended)

Each submission should include:

- **Repo link** (or zip) with run instructions
- **Architecture artifact** (diagram + design notes)
- **Evidence** (logs/screenshots) proving:
  - happy path success
  - at least one failure path + recovery/fallback
- **Short write-up** covering security + cost considerations

---

## Weekly assignments

### Week 1 — Architecture proposal + Bedrock baseline

**Submit**

- Architecture diagram for a chosen enterprise use case
- Bedrock invocation example(s) (code + output)
- Latency/cost observations (simple table)

**Rubric (10 points)**

- **Problem framing (2)**: clear inputs/outputs and success criteria
- **Architecture correctness (3)**: coherent components and data flow
- **Experiment quality (3)**: meaningful comparison, clear observations
- **Risk awareness (2)**: identifies leakage/hallucination/cost risks

---

### Week 2 — Secure integration + prompt evaluation

**Submit**

- Least-privilege IAM design (diagram + policy outline)
- Secure Bedrock invocation from Lambda (evidence)
- Prompt evaluation harness results + decision note

**Rubric (10 points)**

- **Security design (4)**: least privilege, separation of duties, clarity
- **Evaluation method (3)**: golden set, scoring, repeatability
- **Operational considerations (2)**: logging/redaction, correlation IDs
- **Clarity (1)**: organized, readable artifacts

---

### Week 3 — Structured decision engine

**Submit**

- Decision engine service (API or function)
- Strict JSON schema + validation logic
- Fallback behavior for invalid/low-confidence outputs

**Rubric (10 points)**

- **Structured outputs (3)**: strict JSON, enums, bounds, deterministic parsing
- **Validation & fallback (4)**: rejects bad outputs, safe defaults, tests
- **Hybrid logic (2)**: rules + AI with confidence thresholding
- **API/design clarity (1)**: clear contract and examples

---

### Week 4 — Step Functions orchestration + reliability report

**Submit**

- State machine definition + diagram
- Evidence of retries/backoff and failure handling
- “Retry automation report” (1–2 pages)

**Rubric (10 points)**

- **Workflow design (4)**: correct states, branching, data passing
- **Resilience (4)**: retries/backoff, timeouts, catch/fallback paths
- **Idempotency (1)**: idempotency key strategy described and used
- **Evidence quality (1)**: run history + logs show expected behavior

---

### Week 5 — AI API platform (3 endpoints)

**Submit**

- API Gateway + Lambda implementation for:
  - `/classify`
  - `/summarize`
  - `/route`
- API documentation + example payloads
- Rate limiting / cost controls description

**Rubric (10 points)**

- **API contracts (3)**: request/response schemas, versioning, errors
- **Security + throttling (3)**: auth approach, rate limits, safe defaults
- **Reliability (2)**: validation, fallbacks, retries where appropriate
- **Docs (2)**: clear examples and operational notes

---

### Week 6 — Observability + governance

**Submit**

- CloudWatch dashboard(s) + alert(s)
- Audit trail implementation (DynamoDB/S3) with correlation IDs
- Governance checklist + operations runbook

**Rubric (10 points)**

- **Observability (4)**: useful metrics, dashboards, alerts
- **Auditability (3)**: traceability, event structure, retention strategy
- **Safety (2)**: redaction, secure logging, policy alignment
- **Runbook quality (1)**: clear actions for common incidents

---

### Week 7 — Agent system workflow

**Submit**

- Agent-like routing workflow (policy + tool selection)
- Memory pattern implementation (safe storage constraints)
- Event-driven chaining evidence (if applicable)

**Rubric (10 points)**

- **Agent architecture (4)**: router/tool selection, policy enforcement
- **Memory correctness (3)**: what is stored, TTL, safety constraints
- **Event-driven design (2)**: idempotent consumers, chaining correctness
- **Evidence (1)**: logs show routing + memory usage

---

## Architecture reviews (Weeks 2, 4, 6)

### Review format (10–15 min per student/team)

- **2 min**: problem + success metrics
- **3 min**: architecture diagram walkthrough
- **3 min**: reliability + safety (failures, fallbacks, logging)
- **2 min**: cost controls + scaling considerations
- **Q&A**

### Architecture review rubric (10 points)

- **Correctness (3)**: components and data flows are coherent
- **Reliability (3)**: retries, fallbacks, idempotency, failure isolation
- **Security & governance (2)**: IAM, data handling, audit posture
- **Cost & scalability (2)**: cost drivers, throttling/limits, scaling plan

---

## Capstone grading rubric (30 points)

Use the detailed rubric and checklists in `CAPSTONE_HANDBOOK.md`. Summary:

- **Architecture & narrative (8)**
- **Reliability (8)**
- **Governance & safety (6)**
- **Observability & ops readiness (4)**
- **Cost controls (4)**

