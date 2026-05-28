## AI Automation & Agents with AWS Bedrock — Instructor Lesson Plans

Use this document to run consistent, high-signal sessions. Each week includes objectives, an agenda, a suggested demo, and take-home work aligned to `SYLLABUS.md`.

> Recommended live format: 2 sessions/week. If you run 1 session/week, merge Session A and B and reduce lab scope.

---

## Week 1 — Enterprise AI Foundations

### Objectives (students can…)

- Explain where LLMs fit vs ML vs rules engines in enterprises
- Identify risks (hallucinations, leakage, cost) and mitigation patterns
- Invoke a Bedrock model and compare outputs for latency/cost/quality
- Draft a workflow architecture diagram for an enterprise use case

### Session A (Foundations + first invocation)

- **Lecture**: enterprise AI reference architectures; failure modes; why “structured outputs + validation” matter
- **Demo**: minimal Bedrock invocation (CLI or Python) + basic prompt hygiene
- **Discussion prompts**:
  - What should never be decided by an LLM?
  - Where do guardrails live (prompt vs code vs orchestration)?
- **Lab kickoff**: first invocation + side-by-side model comparison

### Session B (Cost/latency + architecture thinking)

- **Lecture**: cost drivers, token accounting, caching, throttling, batching
- **Demo**: same prompt evaluated with:
  - different temperatures
  - constrained response formats
  - short vs long context
- **Workshop**: students produce a 1-page “AI workflow proposal” (inputs, outputs, risks, success metrics)

### Homework / deliverables

- Architecture diagram + narrative (1–2 pages)
- Bedrock invocation examples (code + outputs)
- Latency/cost analysis (simple table + observations)

---

## Week 2 — AWS Bedrock Deep Dive

### Objectives

- Choose an appropriate Bedrock model for a workload with constraints
- Secure Bedrock usage with IAM and least-privilege access design
- Version and evaluate prompts with a lightweight rubric
- Explain private networking concepts and how they affect deployment choices

### Session A (Models, prompting, evaluation)

- **Lecture**: model selection, context windows, temperature/top_p tradeoffs
- **Demo**: prompt template + “golden set” evaluation harness (small CSV/JSONL)
- **Workshop**: define evaluation criteria for one target task (routing/classification)

### Session B (Security design)

- **Lecture**: IAM patterns (roles, policies, permissions boundaries), audit posture
- **Demo**: minimal secure architecture: Lambda role invokes Bedrock; deny-by-default; CloudWatch logs
- **Workshop**: students draft an IAM access design (who/what can invoke which models)

### Homework / deliverables

- Secure Bedrock architecture write-up
- Prompt evaluation results + decision rationale
- IAM access design (diagram + policy outline)

---

## Week 3 — AI Decision Engines & Structured Outputs

### Objectives

- Produce strict JSON outputs from LLMs for downstream automation
- Validate model outputs deterministically (schemas, enums, bounds)
- Implement routing decisions with confidence scoring and fallbacks
- Combine AI + rules for reliability and compliance

### Session A (Structured outputs + validation)

- **Lecture**: “AI as a probabilistic component” and why validation is mandatory
- **Demo**: classification with strict JSON schema + validator + fallback
- **Lab kickoff**: implement a decision engine API with validation

### Session B (Routing + confidence + hybrid)

- **Lecture**: confidence signals; human-in-the-loop triggers; risk-based routing
- **Demo**: hybrid router: rules first, AI second; or AI first with deterministic guardrails
- **Workshop**: students define their routing policy for a chosen use case

### Homework / deliverables

- AI decision engine (code + design notes)
- Validation workflow (schema + failure handling)
- Classification API (endpoint contract + examples)

---

## Week 4 — Orchestrating AI with Step Functions

### Objectives

- Model multi-step AI workflows with Step Functions
- Use retries/backoff, timeouts, and catch/fallback behavior appropriately
- Implement idempotency and safe replays
- Simulate failures and prove workflow resilience

### Session A (Orchestration patterns)

- **Lecture**: state machine design, error handling, idempotency keys
- **Demo**: multi-step workflow:
  - invoke Bedrock
  - validate output
  - branch to actions
  - persist results
- **Lab kickoff**: build a state machine for the Week 3 decision engine

### Session B (Failure injection + reliability)

- **Lecture**: failure taxonomies (transient vs permanent), DLQs, compensating actions
- **Demo**: simulate Bedrock throttling / validation failure / downstream timeouts
- **Workshop**: students add observability checkpoints and create a retry report

### Homework / deliverables

- State machine definition + diagram
- Failure simulation evidence (logs/screenshots) + mitigations
- Retry automation report (what retried, why, with what backoff)

---

## Week 5 — AI Automation APIs

### Objectives

- Build API Gateway + Lambda + Bedrock endpoints safely
- Implement auth and rate limiting + usage plans
- Design cost-aware APIs (limits, caching, request shaping)
- Publish minimal API docs and example requests/responses

### Session A (API platform fundamentals)

- **Lecture**: endpoint design, contracts, versioning, quota/cost controls
- **Demo**: `/classify` end-to-end with:
  - strict request/response schemas
  - validation
  - structured error responses
- **Lab kickoff**: implement `/summarize` and `/route`

### Session B (Security + operations)

- **Lecture**: throttling, WAF (optional), request/response logging, redaction
- **Demo**: add auth + quotas; capture audit events
- **Workshop**: students write API docs with examples and failure modes

### Homework / deliverables

- AI API platform (3 endpoints: `/classify`, `/summarize`, `/route`)
- API documentation + sample payloads
- Security and cost control notes (limits, throttles, budgets)

---

## Week 6 — Observability, Governance & AI Safety

### Objectives

- Implement prompt/response logging with redaction and traceability
- Build audit trails and operational dashboards
- Track cost and build cost alarms/budgets
- Design human-in-the-loop triggers for high-risk outputs

### Session A (Observability)

- **Lecture**: what to log; what never to log; correlation IDs and tracing
- **Demo**: CloudWatch dashboards: latency, error rate, retries, Bedrock spend proxy metrics
- **Lab kickoff**: add audit logging to Week 5 APIs and Week 4 workflows

### Session B (Governance + safety)

- **Lecture**: governance controls, approvals, change management for prompts
- **Demo**: human-in-the-loop branch in Step Functions (approval simulation)
- **Workshop**: students create a governance checklist and a runbook for incidents

### Homework / deliverables

- Observability dashboards (screenshots + definitions)
- Governance workflow doc + checklist
- AI operations report (incidents to monitor, alerts, on-call playbook)

---

## Week 7 — Enterprise AI Agent Systems

### Objectives

- Explain agent components: planner/router/tools/memory/guardrails
- Build an agent-like operational assistant workflow with routing
- Implement simple memory patterns (session + durable store)
- Chain workflows via events for scalable automation

### Session A (Agent architecture)

- **Lecture**: agent boundaries; tool execution safety; memory and retrieval pitfalls
- **Demo**: routing agent that selects:
  - workflow A: summarize
  - workflow B: classify and route
  - workflow C: create ticket / action stub
- **Lab kickoff**: operational assistant workflow skeleton

### Session B (Event-driven chaining)

- **Lecture**: event-driven automation with EventBridge; fan-out; idempotent consumers
- **Demo**: chained workflow: event → router → workflow → audit → notification
- **Workshop**: students define “agent policies” (allowed actions, approvals, escalation)

### Homework / deliverables

- AI agent workflow (diagram + policy doc)
- Agent orchestration diagrams (routing + memory + tools)
- Multi-step automation system with evidence of event chaining

---

## Week 8 — Capstone

### Objectives

- Deliver a production-minded system with clear business narrative
- Demonstrate reliability: retries, fallbacks, idempotency, monitoring
- Present governance: audit logs, cost controls, safety constraints
- Run a clean demo with pre-baked test inputs and failure scenarios

### Capstone structure

- **Demo day format**:
  - 3 min problem + architecture
  - 5 min live demo (happy path)
  - 2 min failure scenario + recovery
  - 2 min Q&A

### Deliverables

- Architecture diagrams + system design summary
- Source code repo with run instructions
- Automation workflows + API docs (as applicable)
- Cost/risk analysis + governance review

