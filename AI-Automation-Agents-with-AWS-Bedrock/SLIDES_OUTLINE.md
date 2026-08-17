## AI Automation & Agents with AWS Bedrock — Slide Deck Outline

This is a **speaker-ready outline** for building slides. Keep slides visual; push detail into speaker notes and labs.

---

## Deck 0 — Course kickoff (optional, 15–20 slides)

- Title + tagline
- What you’ll build (reference architecture)
- Outcomes and portfolio artifacts
- Who this course is for + prerequisites
- How grading works (high level)
- Course norms: security, cost controls, no secrets in prompts/logs
- Delivery schedule + office hours
- Capstone overview (options + milestones)

---

## Week 1 — Enterprise AI Foundations (25–35 slides)

- Enterprise AI: where it fits and where it doesn’t
- LLMs vs ML vs rules engines (decision matrix)
- Why production AI fails: hallucination, leakage, cost spikes
- Architecture primitives (event → orchestration → AI → actions → storage → monitoring)
- Prompt hygiene fundamentals (constraints, JSON-only, bounded responses)
- Latency and cost basics (what drives spend)
- Demo flow overview: first Bedrock invocation + comparison runs
- Lab checklist + deliverables

---

## Week 2 — AWS Bedrock Deep Dive (30–40 slides)

- Bedrock overview + model families (selection criteria)
- Model choice by task: classification, summarization, routing
- Prompt templates and versioning strategy
- Evaluation harness: golden sets + scoring
- Security: IAM patterns, least privilege, audit posture
- Private networking concepts (what changes, what doesn’t)
- Demo: secure Lambda→Bedrock invocation
- Lab checklist + deliverables

---

## Week 3 — Decision Engines & Structured Outputs (30–40 slides)

- AI as a probabilistic component (why validation is mandatory)
- Structured outputs: strict JSON, schemas, enums, bounds
- Confidence scoring and thresholds
- Hybrid AI + rules: patterns and tradeoffs
- Deterministic fallbacks + human-in-the-loop triggers
- Demo: JSON schema validation + fallback
- Lab checklist + deliverables

---

## Week 4 — Step Functions Orchestration (30–45 slides)

- Why orchestration matters (reliability, auditability, change control)
- Step Functions patterns:
  - retries/backoff
  - timeouts
  - catch/fallback
  - compensation
- Idempotency and safe replays
- Failure injection as a requirement
- Demo: classify → validate → act workflow
- Lab checklist + deliverables

---

## Week 5 — AI Automation APIs (30–45 slides)

- API design for AI: contracts, versioning, error models
- API Gateway + Lambda patterns
- Security: auth options, throttling, usage plans
- Cost-aware API design:
  - limits
  - request shaping
  - caching (when it helps)
- Demo: `/classify` end-to-end with validation
- Lab checklist + deliverables

---

## Week 6 — Observability, Governance & AI Safety (35–50 slides)

- What to log vs never log (redaction)
- Correlation IDs and traceability
- Audit trails (who/what/when/why)
- Monitoring: SLOs, dashboards, alerts
- Cost tracking + budgets + alerting strategy
- Human-in-the-loop: approvals and escalation paths
- Demo: audit event pipeline + CloudWatch dashboard
- Lab checklist + deliverables

---

## Week 7 — Enterprise AI Agent Systems (35–55 slides)

- Agent anatomy: router/planner/tools/memory/guardrails
- Tool execution safety and policy enforcement
- Memory patterns:
  - session summary memory
  - durable memory with TTL
  - what not to store
- Event-driven chaining with EventBridge
- Multi-agent workflows (when to split vs centralize)
- Demo: routing “agent” selects workflows safely
- Lab checklist + deliverables

---

## Week 8 — Capstone + Demo Day (20–35 slides)

- Capstone expectations: minimum bar (orchestration, validation, audit, dashboards, cost controls)
- Milestones and recommended scope control
- Demo script template:
  - happy path
  - failure scenario
  - recovery/fallback
- How we grade (rubric overview)
- Presentation tips: clarity, evidence, “what good looks like”

