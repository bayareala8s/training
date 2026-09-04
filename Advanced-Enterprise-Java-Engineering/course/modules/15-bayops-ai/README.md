# Module 15 — BayOps AI — AI-Assisted Operations

**Duration:** ~3 hours of lessons plus 4 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Use AI as an investigator, never as the authority  
**Portfolio artifact:** AI-operations evaluation from [student/worksheets/PF-ai.md](../../../student/worksheets/PF-ai.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, log line, metric name, incident pack, and model output you see is synthetic. Do not treat this pack as a production SRE product, a live Bedrock tenant, or a license to auto-remediate `payment-service`.

**Delivery note:** the grade bar is **paper plus method**. Students pass by writing JSON that matches [infrastructure/bayops-ai/schema/output.schema.json](../../../infrastructure/bayops-ai/schema/output.schema.json). A live Amazon Bedrock call, Lambda deploy, or `terraform apply` is **not** required. Reuse [datasets/baypay-ai/BAYOPS.md](../../../datasets/baypay-ai/BAYOPS.md) and the sketch in [infrastructure/bayops-ai/README.md](../../../infrastructure/bayops-ai/README.md). Do not invent a second output contract.

---

## Business context

Modules 13 and 14 taught Riley Okonkwo to quote RED/USE, stabilize merchants, and refuse a leftover-cell bounce. Harbor Bike Co still charges Avery Chen `$84.00` through `POST /api/v1/payments`. The process is still the Java 21 / Spring Boot 3.5.5 modular monolith in `reference-apps/baypay`, listening on port `8080`, health on `/actuator/health/liveness` and `/actuator/health/readiness`. Jordan Voss still ships an immutable tag. Priya Nair still spends a **99.9%** monthly error budget. The new failure mode is a fluent paragraph that says **“Root cause: …”** with no file underneath it.

BayOps AI is a **teaching prototype**. It may *retrieve* a synthetic pack and *propose* four labeled sections. It is never the commander. A model that mixes a quoted log, a guess, and a bounce into one sentence is a **mixed summary** — a class you will rewrite, not a personality. Ranked guesses stay `unproven`. An unsafe runbook that auto-executes is a class you will reject. An unsupported diagnosis that invents a path or marks RCA proven is a class you will catch in AI-1504.

The locked contract is one sentence:

**Use AI as an investigator, never as the authority.**

| Bucket | What it may contain | What it must not do |
|---|---|---|
| **Evidence** | Quotes from files the operator opened (path, timestamp, text) | Invent a file, a metric, or a host |
| **Hypotheses** | Ranked, *unproven* explanations that fit the evidence so far | Mark one as proven / RCA / “confirmed” |
| **Recommended investigation** | The *next* gate or omitted evidence kind, and why | Skip to bounce / apply / force-push |
| **Suggested remediation** | Stabilize then remediations, each needing **human approval** | Auto-execute, auto-rollback, or disable TLS |

A fifth field rides on every mutating suggestion: `humanApproval` stays `pending` until Riley Okonkwo or Priya Nair (or the student playing on-call) writes `approved` or `rejected` with a name and time. Schema: [output.schema.json](../../../infrastructure/bayops-ai/schema/output.schema.json). Architecture sketch: **AEJE-D-069**.

| Field | Locked value |
|---|---|
| App | `payment-service` (Java 21, Spring Boot 3.5.5) |
| Region (when AWS is named) | `us-west-2` |
| Port / health | `8080` / `/actuator/health/liveness`, `/actuator/health/readiness` |
| Golden request | `POST /api/v1/payments` with `Idempotency-Key` |
| Live model | **Not required.** Paper fixtures + the JSON contract are enough |
| Allowed AWS *sketch* | Amazon Bedrock, Lambda, S3, DynamoDB, API Gateway, CloudWatch — paper |
| Do not apply | NAT Gateway, EKS, OpenSearch, always-on GPU, multi-AZ RDS “for the demo” |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |
| Example AI-lab payment | `c1501d33-0000-4000-8000-111111111501` |

On-call names: **Riley Okonkwo** (application), **Priya Nair** (SRE), **Sam Okada** (platform), **Jordan Voss** (release), **Morgan Hale** (WAS leftover). Payment happy path is still `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. Morgan’s leftover cell (`dmgr-east`, `PaymentCluster`) is not the estate you page and not a remediation target. Never recommend ND-in-Docker, never set `-Xmx` equal to the cgroup, and never auto-remediate production.

---

## Learning objectives

After this module you can:

- Summarize a synthetic `payment-service` pack into **Evidence / Hypotheses / Recommended investigation / Suggested remediation** without collapsing them into a proven RCA.
- Separate a quoted file from an unproven guess (AEJE-D-068), and refuse an invented path.
- Rank RCA hypotheses with `status=unproven` (or `weakened` / `withdrawn`) and name the next gate.
- Propose runbook steps that stabilize first, mark `approvalRequired=true`, and reject an unsafe auto-execute class.
- Hold `humanApproval` at `pending` until a named human writes `approved` or `rejected` (AEJE-D-070).
- Evaluate a model output for schema, citation, and hallucination — including a fixture that invents files or marks RCA proven — without treating the model as the authority.

---

## Prerequisites

- Modules 1–14, especially L-13.6 (hypothesis, evidence, stabilize, remediate, comms), L-13.1 (JSON log fields, no PAN on labels), L-12.6 (health before cut), and L-14.2 / L-14.3 (no secrets, no PAN to a model).
- Locked AI contract: [BAYOPS.md](../../../datasets/baypay-ai/BAYOPS.md). Sketch and fixtures: [infrastructure/bayops-ai](../../../infrastructure/bayops-ai/README.md). Ops names when you quote RED/USE: [OBSERVABILITY.md](../../../datasets/baypay-ops/OBSERVABILITY.md).
- Comfort reading JSON and a JSON Schema. A Bedrock API key, AWS account apply, or licensed APM is **not** required.

You do **not** need a live foundation model. Paper plus the four-bucket file is enough.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional. Lessons teach **method and the locked contract**. They do not lecture instructor answers for AI-1501–1504.

| Id | Title | What it unlocks |
|---|---|---|
| [L-15.1](lessons/L-15.1.md) | Incident summarization | Four buckets; mixed-summary class; AEJE-D-069 |
| [L-15.2](lessons/L-15.2.md) | Evidence vs hypothesis | Quote vs guess; AEJE-D-068 |
| [L-15.3](lessons/L-15.3.md) | RCA hypothesis generation | Ranked unproven hypotheses; next gate |
| [L-15.4](lessons/L-15.4.md) | Runbook recommendations | Suggested remediations; unsafe-runbook class |
| [L-15.5](lessons/L-15.5.md) | Human approval | `pending` until a named human; AEJE-D-070 |
| [L-15.6](lessons/L-15.6.md) | AI evaluation and hallucination detection | Unsupported-diagnosis class; AEJE-D-070 |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [AI-1501](../../../labs/AI-1501/README.md) | AI | Incident summarization | L-15.1 |
| [AI-1502](../../../labs/AI-1502/README.md) | AI | RCA hypotheses | L-15.3 |
| [AI-1503](../../../labs/AI-1503/README.md) | AI | Runbook recommendation | L-15.4 |
| [AI-1504](../../../labs/AI-1504/README.md) | AI | Evaluate hallucinated diagnosis | L-15.6 |

Time-box each lab at **45–75 minutes**. Student guides show **fixtures and method**. Do not open `solutions/AI-150N/` until your worksheet separates the four buckets, keeps hypotheses `unproven`, and leaves mutating steps `pending`.

Treat **mixed summary**, **ranked unproven hypotheses**, **unsafe runbook**, and **unsupported diagnosis** as *classes*. Quote *this* pack’s evidence. A fluent paragraph that happens to sound like an RCA does **not** max Diagnostic method. Lessons do **not** lecture those packs’ planted answers.

Live Bedrock is optional extra credit. Paper JSON that validates against the schema is the pass path.

---

## Assessment and portfolio

1. Complete AI-1501 through AI-1504 with four-bucket files and a human-approval record on any mutating suggestion.
2. Take [Q-15](../../quizzes/Q-15.md) when your cohort opens it.
3. Export the **AI-operations evaluation** using [student/worksheets/PF-ai.md](../../../student/worksheets/PF-ai.md).

The worksheet is the Module 15 portfolio artifact. Module 16 will assume you can defend “investigator, not authority” in an interview without reciting an instructor fixture.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/23-agentic-ai-architecture/agent-governance-and-safety.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). It deepens agent governance and human gates. This module stands alone without it.

---

## Guardrails

- **No live model required.** Fixtures + [output.schema.json](../../../infrastructure/bayops-ai/schema/output.schema.json) are enough to pass.
- Never auto-approve. `humanApproval.status` stays `pending` until Riley, Priya, or the student on-call writes a name and time.
- Never emit a **proven RCA**. `provenRootCause` is forbidden on teaching outputs. Hypotheses stay `unproven` until withdrawn or weakened.
- Synthetic data only. No PAN, CVV, full account numbers, `BAYPAY_DB_PASSWORD`, or live access keys in a prompt, fixture, or worksheet.
- Allowed sketch (paper): Bedrock, Lambda, S3, DynamoDB, API Gateway, CloudWatch in `us-west-2`. Do **not** apply NAT, EKS, OpenSearch, or provisioned Bedrock throughput “for realism.”
- Never recommend ND-in-Docker, `-Xmx` equal to the cgroup, or auto-remediate production. Never bounce `dmgr-east` as the Boot answer.
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`. Lessons do not replace them.
