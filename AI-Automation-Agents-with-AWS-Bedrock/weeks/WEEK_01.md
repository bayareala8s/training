## Week 1 — Enterprise AI Foundations

This week establishes the “production mindset”: LLMs are powerful but probabilistic, so enterprise systems need **constraints, validation, observability, security, and cost controls**.

### Learning objectives

By the end of Week 1, students can:

- Explain LLMs vs ML vs rules engines and where each fits
- Describe enterprise AI risks (hallucinations, leakage, cost spikes) and mitigations
- Invoke an AWS Bedrock model and compare responses under different settings
- Produce a clear AI workflow architecture diagram for a real enterprise use case

### Core concepts (lecture notes)

- **Where AI fits in enterprises**
  - Automate repetitive cognitive tasks (triage, classification, summarization, routing)
  - Assist humans with structured recommendations, not unchecked authority
- **LLMs vs ML vs rules engines**
  - Rules: deterministic, auditable, brittle for language ambiguity
  - ML: supervised, stable within training distribution, slower iteration
  - LLMs: flexible language reasoning, non-deterministic, requires guardrails
- **Failure modes**
  - Hallucinations → require validation, bounded outputs, and safe defaults
  - Data leakage → strict logging/redaction policies, least privilege, data minimization
  - Cost spikes → quotas, throttling, max input/output limits, caching where appropriate
- **Production patterns introduced**
  - Constrain outputs (structured JSON, bounded length)
  - Validate outputs deterministically (schema/enum checks)
  - Observe everything (correlation IDs, success/failure, latency)
  - Design fallbacks (rules, “unknown”, human review)

### In-class activities (45–60 min)

- **Activity A — Risk mapping**
  - Pick one use case (incident triage / document routing / internal assistant).
  - Identify: data sensitivity, failure impact, required auditability, cost sensitivity.
- **Activity B — Architecture sketch**
  - Draw the reference pipeline for your use case (event → orchestration → model → validation → action → storage → monitoring).

### Demos (instructor-led)

- **Demo 1**: Minimal Bedrock invocation (Python) and timing measurement.
- **Demo 2**: Compare prompt styles:
  - open-ended vs “JSON-only”
  - low vs moderate temperature
  - short vs long context

### Hands-on lab (students)

Complete:

- `LABS_GUIDE.md` → **Week 1 Labs**: Lab 1.1 and Lab 1.2
- Runnable code: `labs/week01/` — see `labs/README.md`

### Assignment (due end of week)

Submit:

- **Architecture diagram + narrative** (1–2 pages)
  - problem statement and success metrics
  - inputs/outputs and data classification (sensitive vs non-sensitive)
  - risks and mitigations
- **Bedrock invocation examples**
  - command/script + captured outputs
  - latency measurement
- **Cost/latency analysis**
  - short table comparing 2–4 runs

Rubric:

- See `ASSIGNMENTS_AND_RUBRICS.md` → **Week 1**

### Quiz (5–10 questions)

1. What is one scenario where a rules engine is preferred over an LLM?
2. Why are structured outputs important for automation workflows?
3. Name two common enterprise AI risks and one mitigation for each.
4. What factors commonly drive LLM cost?
5. What is a safe fallback when model confidence is low?
6. What should you never include in logs for AI systems?

### Architecture diagram

Detailed instructor diagram (Draw.io · PNG · SVG):

- [`diagrams/drawio/02-week01.drawio`](../diagrams/drawio/02-week01.drawio) · [PNG](../diagrams/png/02-week01.png) · [SVG](../diagrams/svg/02-week01.svg)

Use in class to compare **rules vs ML vs LLM** and introduce enterprise risks before the first Bedrock lab.

### Expected artifacts (portfolio-ready)

- Architecture diagram with production concerns (security, cost, reliability)
- Repeatable invocation script with timing and basic run notes

