# Module 16 — Advanced Engineer Interview Simulator

**Duration:** ~4.5 hours of lessons plus 5 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Defend BayPay decisions at Engineer through Principal level  
**Portfolio artifact:** System-design response from [INTERVIEW-1604](../../../labs/INTERVIEW-1604/README.md) using [student/worksheets/PF-design.md](../../../student/worksheets/PF-design.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, question prompt, spoken answer, and design sketch you see is synthetic. Do not treat this pack as a live hiring loop, a licensed interview product, or a second 100-question file.

**Delivery note:** the grade bar is **paper plus method**. Phase A is this module, [datasets/baypay-interview/ROUNDS.md](../../../datasets/baypay-interview/ROUNDS.md), and [interview-bank/simulator.py](../../../interview-bank/simulator.py). A BayLearn interview UI, Bedrock call, or portal session store is **not** required to pass. The bank is exactly **100** records, `AEJE-IQ-001` through `AEJE-IQ-100`, in [interview-bank/questions.json](../../../interview-bank/questions.json). Do not add a 101st question. Do not invent a second bank.

---

## Business context

Harbor Bike Co still charges Avery Chen `$84.00` through `POST /api/v1/payments`. The process is still the Java 21 / Spring Boot 3.5.5 modular monolith in `reference-apps/baypay`, listening on port `8080`, health on `/actuator/health/liveness` and `/actuator/health/readiness`. Priya Nair still spends a **99.9%** monthly error budget. Jordan Voss still ships an immutable tag. Sam Okada still refuses NAT Gateway “for realism.” Morgan Hale’s leftover cell (`dmgr-east`, `PaymentCluster`) is still not the estate you page.

This module asks a different question: **can you defend those decisions out loud?** A hiring loop will not accept one memorized paragraph for Engineer, Senior, Staff, and Principal. Riley Okonkwo must name a mechanism and a check. Priya must name an SLO sentence and a next gate. Sam must name a platform trade-off for *this* quarter. A Principal must say no to a seventh service without sounding theatrical.

The locked contract is one sentence:

**Defend BayPay at Engineer through Principal — different scope, not a longer copy of the same paragraph.**

| Mode | Lab | What “done” means |
|---|---|---|
| Practice | INTERVIEW-1601 | Open a question, write Engineer + Senior (or Staff), then compare to the bank — no timer required |
| Timed interview | INTERVIEW-1601 variant or 1605 | Same quality bar under a clock (8 minutes / question) |
| Rapid fire | INTERVIEW-1602 | Short answers, many items; depth is not the grade |
| Troubleshooting | INTERVIEW-1603 | Evidence → hypothesis → next gate; lucky RCA does not max Diagnostic method |
| System design | INTERVIEW-1604 | One BayPay design; trade-offs; portfolio `PF-design.md` |
| Full mock loop | INTERVIEW-1605 | Several rounds in one sitting, including one timed item |

Domain counts are locked. Do not rewrite an id’s domain.

| Domain | Count | Lessons that train the voice |
|---|---|---|
| Java/JVM | 20 | L-16.1 |
| Spring/Jakarta | 10 | L-16.2 |
| WebSphere/Liberty | 15 | L-16.3 |
| Containers/Kubernetes/OpenShift | 15 | L-16.4 |
| AWS | 10 | L-16.5 |
| Automation | 8 | L-16.6 |
| Linux/Networking/TLS | 7 | Woven into L-16.4 / L-16.5 / L-16.7 |
| Production Engineering | 7 | L-16.7 |
| HA/Security | 4 | L-16.7 / L-16.8 |
| Leadership/Architecture | 4 | L-16.8 / L-16.9 |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |

On-call names: **Riley Okonkwo** (application), **Priya Nair** (SRE), **Sam Okada** (platform), **Jordan Voss** (release), **Morgan Hale** (WAS leftover). Payment happy path is still `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. Never recommend ND-in-Docker, never set `-Xmx` equal to the cgroup, and never bounce `dmgr-east` as the Boot answer.

Scoring when an item is diagnostic uses the question `scoreRubric` plus course weights: Technical 25 / Method 20 / Production 15 / Trade-off 15 / Security 10 / Comms 10 / Efficiency 5.

---

## Learning objectives

After this module you can:

- Open `AEJE-IQ-001`–`AEJE-IQ-100` with `simulator.py` and write **four maturity layers**, not one recycled paragraph.
- Practice Java/JVM and Spring/Jakarta prompts, then run INTERVIEW-1601 without a timer or a portal.
- Fire short, correct-enough answers across several domains (INTERVIEW-1602) without turning every item into a whiteboard.
- Work a troubleshooting pack as evidence → hypothesis → next gate (INTERVIEW-1603) and refuse a lucky RCA as max method.
- Defend one BayPay system design with explicit trade-offs and export [PF-design.md](../../../student/worksheets/PF-design.md) (INTERVIEW-1604).
- Sit a full mock loop (INTERVIEW-1605) that mixes practice or timed, troubleshooting, and a design slice.

---

## Prerequisites

- Modules 1–14, especially JVM memory and dumps, Spring/Jakarta transactions and Actuator, leftover WAS vs Liberty, container limits, ECS in `us-west-2`, Terraform/Ansible/CI, RED/USE and incident method, and paper HA/DR.
- Locked rounds: [ROUNDS.md](../../../datasets/baypay-interview/ROUNDS.md). Bank contract: [interview-bank/README.md](../../../interview-bank/README.md), [schema.json](../../../interview-bank/schema.json), [modes.md](../../../interview-bank/modes.md).
- Comfort speaking for 60–90 seconds and writing a one-page design. A BayLearn login, Interview Accelerator enrollment, or live AWS apply is **not** required.

You do **not** need a portal simulator. Paper plus the CLI is enough.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional. Lessons teach **method and maturity**. They cite one or two bank ids as *practice handles*. They do **not** dump bank answers or lecture instructor RCAs.

| Id | Title | What it unlocks |
|---|---|---|
| [L-16.1](lessons/L-16.1.md) | Java / JVM round | Four-layer JVM voice; practice handle `AEJE-IQ-001` |
| [L-16.2](lessons/L-16.2.md) | Spring / Jakarta round | Transaction and injection voice; INTERVIEW-1601 |
| [L-16.3](lessons/L-16.3.md) | WebSphere / Liberty round | Cell vs `server.xml`; never ND-in-Docker |
| [L-16.4](lessons/L-16.4.md) | Containers / Kubernetes round | Limits vs heap; liveness vs readiness |
| [L-16.5](lessons/L-16.5.md) | AWS round | Fargate default; ECS vs EKS vs OpenShift this quarter |
| [L-16.6](lessons/L-16.6.md) | Automation round | Gates and rollback; INTERVIEW-1602 |
| [L-16.7](lessons/L-16.7.md) | Production incident round | Method over lucky RCA; INTERVIEW-1603 |
| [L-16.8](lessons/L-16.8.md) | System design round | One BayPay design; INTERVIEW-1604 / `PF-design.md` |
| [L-16.9](lessons/L-16.9.md) | Leadership / architecture round | ADR and influence; INTERVIEW-1605 |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [INTERVIEW-1601](../../../labs/INTERVIEW-1601/README.md) | INTERVIEW | Practice mode | L-16.2 |
| [INTERVIEW-1602](../../../labs/INTERVIEW-1602/README.md) | INTERVIEW | Rapid fire | L-16.6 |
| [INTERVIEW-1603](../../../labs/INTERVIEW-1603/README.md) | INTERVIEW | Troubleshooting interview | L-16.7 |
| [INTERVIEW-1604](../../../labs/INTERVIEW-1604/README.md) | INTERVIEW | System design | L-16.8 |
| [INTERVIEW-1605](../../../labs/INTERVIEW-1605/README.md) | INTERVIEW | Full mock loop | L-16.9 |

Time-box INTERVIEW-1601 and 1602 at **45–75 minutes**. INTERVIEW-1603 at **45–75 minutes**. INTERVIEW-1604 at **60–90 minutes**. INTERVIEW-1605 at **75–120 minutes**. Student guides show **prompts and method**. Do not open `solutions/INTERVIEW-160N/` until your worksheet has four maturity layers (or the mode’s shorter bar), quoted evidence on a troubleshooting item, and a design with trade-offs.

Treat **symptom classes** (P99 spike, unhealthy target, `OOMKilled`, handshake failure) as classes. Quote *this* pack’s evidence. A fluent paragraph that happens to match a lab title does **not** max Diagnostic method. Lessons do **not** lecture instructor RCAs.

Phase A is files plus CLI. Do not require a portal to pass.

---

## Assessment and portfolio

1. Complete INTERVIEW-1601 through INTERVIEW-1605 with written maturity layers, a troubleshooting method sheet, and one BayPay design.
2. Take [Q-16](../../quizzes/Q-16.md) when your cohort opens it.
3. Export the **system-design response** using [student/worksheets/PF-design.md](../../../student/worksheets/PF-design.md).

The worksheet is the Module 16 portfolio artifact. Later reviews will assume you can defend the same estate without reciting a bank reveal.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/24-system-design/overview.md`, `docs/30-mock-interviews/overview.md`, and `docs/25-architecture-leadership/overview.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). They deepen whiteboard structure, mock discipline, and architecture influence. This module stands alone without them.

---

## Guardrails

- **Exactly 100 questions.** `AEJE-IQ-001`–`AEJE-IQ-100`. Locked domain counts. Do not add a 101st. Do not rewrite an id’s domain.
- Phase A is paper plus `interview-bank/simulator.py`. A BayLearn interview UI is optional Phase B and is **not** required.
- Answers must differ by **Engineer / Senior / Staff / Principal**. One memorized paragraph is a fail.
- Do not treat a model dump or a copied bank `--reveal` as your spoken answer in a live mock.
- Do not name instructor RCAs from INCIDENT labs as if they were the only correct interview story.
- Never recommend ND-in-Docker, `-Xmx` equal to the cgroup, or bouncing `dmgr-east` as the Boot answer.
- Synthetic data only. No PAN, CVV, full account numbers, `BAYPAY_DB_PASSWORD`, or live access keys in a worksheet or prompt.
- Region is **`us-west-2`** when AWS is named. Do not apply NAT Gateway, EKS, OpenSearch, or a second region “for the mock.”
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`. Lessons do not replace them.
