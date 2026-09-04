# Module 13 — Production Engineering and Observability

**Duration:** ~3.5 hours of lessons plus 2 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Operate `payment-service` against a written SLO, not a gut feeling  
**Portfolio artifact:** Operations dashboard notes and production RCA draft from [student/worksheets/PF-ops.md](../../../student/worksheets/PF-ops.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, metric name, dashboard JSON, and incident timeline you see is synthetic. Do not treat this pack as a real employer’s operations system.

**Delivery note:** the grade bar is **paper plus method**. BUILD-1300 ships a Grafana JSON (or equivalent panel list) **on disk**. A live Prometheus, Grafana, CloudWatch, or AMP stack is **not** required to pass. INCIDENT-1301 is a gated symptom pack. Student guides show **symptoms only**. Do not invent a second product SLO or a second metric vocabulary. Reuse [datasets/baypay-ops/OBSERVABILITY.md](../../../datasets/baypay-ops/OBSERVABILITY.md).

---

## Business context

Module 12 automated the release path: Git → `./mvnw test` on **Java 21** → immutable ECR tag → Terraform in `us-west-2` → validate / rollback. Harbor Bike Co still charges Avery Chen `$84.00` through `POST /api/v1/payments`. The process is the same Java 21 / Spring Boot 3.5.5 modular monolith in `reference-apps/baypay`, listening on port `8080`, health on `/actuator/health/liveness` and `/actuator/health/readiness`. A green pipeline is still not a merchant-healthy cut.

This module asks a different question: **is the cut still good an hour later?** Priya Nair needs RED on the golden request, USE on heap / CPU / Hikari `jdbc/baypay` / servlet threads, and an SLO she can spend. Riley Okonkwo needs a page that means “error budget is burning,” not “a log line said ERROR.” Jordan Voss needs a change that names rollback. Sam Okada needs scrape and cardinality hygiene so the platform does not become the outage. Morgan Hale’s leftover cell (`dmgr-east`, `PaymentCluster`) is not the estate you page.

The locked contract is one sentence:

**Logs, metrics, and traces on `POST /api/v1/payments`, scored against a 99.9% monthly SLO and a P99 under 400 ms, with ~43 minutes of error budget per month.**

| Signal | Owner (synthetic) | What “done” means |
|---|---|---|
| JSON logs | Riley / app | Fields `ts`, `level`, `logger`, `msg`, `correlationId`, `paymentId`, `outcome` — no PAN |
| Metrics | Priya / Micrometer | Scrape `/actuator/prometheus`; RED + USE names from OBSERVABILITY.md |
| Traces | optional OTel | W3C `traceparent` on inbound HTTP; not “we have CloudWatch” |
| SLO | Priya + product | 99.9% monthly on the payment-create SLI; P99 `< 400 ms` |
| Page | Priya | SLO burn or saturation that predicts burn — not CPU > 80% |
| Change | Jordan | Reviewed, canaried, reversible; health before merchant cut |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |

On-call names: **Riley Okonkwo** (application), **Priya Nair** (SRE), **Sam Okada** (platform), **Jordan Voss** (release), **Morgan Hale** (WAS leftover). Payment happy path is still `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. Example ops payment id: `c1300a11-0000-4000-8000-111111111300`.

Compute default stays **ECS on Fargate** in `us-west-2` when AWS is named. Do not apply EKS, NAT Gateway, OpenSearch, or a live Grafana “for realism.” 99.99% availability is a **Module 14** architecture target (ARCHITECT-1401). Do **not** upgrade this module’s dashboard SLO.

---

## Learning objectives

After this module you can:

- Separate logs, metrics, and traces for `payment-service`, and stitch a create with `correlationId` / `paymentId` / W3C `traceparent`.
- Read RED on `POST /api/v1/payments` and USE on heap, CPU, Hikari `jdbc/baypay`, and Tomcat / servlet threads.
- Write the payment-create SLI, hold the **99.9%** monthly SLO and P99 `< 400 ms`, and spend the ~43-minute error budget on purpose.
- Design pages for **SLO burn** and **saturation**, plus a paper dashboard that BUILD-1300 can export.
- Plan capacity from RPS, heap, Hikari, and thread pools with SLO-driven headroom — not from multi-region DR.
- Run an incident with hypothesis, evidence, stabilize, remediate, and comms — without naming INCIDENT-1301’s cause from a lesson.
- Gate production change: review, canary, validate, rollback — without bouncing `dmgr-east`.

---

## Prerequisites

- Modules 1–12, especially L-3.3 / L-3.5 (Actuator, `correlationId`), Module 7–8 (heap vs cgroup, pools), L-11.6 (CloudWatch is not a trace), L-12.6 (health before cut).
- Locked ops contract: [OBSERVABILITY.md](../../../datasets/baypay-ops/OBSERVABILITY.md). AWS names when needed: [ACCOUNT.md](../../../datasets/baypay-aws/ACCOUNT.md) (`us-west-2`, ECS/Fargate, port `8080`).
- Comfort reading PromQL-shaped expressions, JSON log lines, and a Grafana panel JSON file. A live metrics stack is **not** required.
- JDK 21 on `PATH` or `JAVA_HOME` if you want to run the reference app. You do **not** need a global Maven install.

You do **not** need Grafana Cloud, Amazon Managed Prometheus, or a licensed APM. Paper plus the reference app’s `/actuator/prometheus` locally is enough.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional. Lessons teach **method and the locked vocabulary**. They do not name the root cause of INCIDENT-1301.

| Id | Title | What it unlocks |
|---|---|---|
| [L-13.1](lessons/L-13.1.md) | Logs, metrics and traces | Three signals, JSON fields, Micrometer scrape, AEJE-D-059 |
| [L-13.2](lessons/L-13.2.md) | RED and USE concepts | Golden-request RED; heap / CPU / Hikari / threads USE, AEJE-D-060 |
| [L-13.3](lessons/L-13.3.md) | SLIs and SLOs | 99.9% monthly, P99 `< 400 ms`, ~43 min budget, AEJE-D-060 |
| [L-13.4](lessons/L-13.4.md) | Alerting and dashboards | Burn + saturation pages; paper Grafana, AEJE-D-061 |
| [L-13.5](lessons/L-13.5.md) | Capacity planning | RPS, heap, Hikari, thread pools, SLO headroom — not DR |
| [L-13.6](lessons/L-13.6.md) | Incident response and RCA | Hypothesis, evidence, stabilize, remediate, comms |
| [L-13.7](lessons/L-13.7.md) | Change management | Review, canary, validate, rollback; freeze literacy |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [BUILD-1300](../../../labs/BUILD-1300/README.md) | BUILD | BayPay operations dashboard | L-13.4 |
| [INCIDENT-1301](../../../labs/INCIDENT-1301/README.md) | INCIDENT | Throughput collapse and P99 latency spike | L-13.6 |

Time-box BUILD-1300 at 60–90 minutes. INCIDENT-1301 at 45–75 minutes. Student incident guide shows **symptoms only**. Work the pack’s gates. Do not open instructor materials until the worksheet has hypothesis, evidence, next investigation, stabilize, remediate, and comms.

Treat a P99 spike or a throughput drop after a metrics change as a *symptom class*, not a closed RCA. Quote *this* pack’s evidence. A lucky label that matches the title does **not** max Diagnostic method.

Dashboard SLO stays **99.9%**. Do not silently paint 99.99% on the panel because Module 14 exists.

---

## Assessment and portfolio

1. Complete BUILD-1300 and INCIDENT-1301 with gated evidence on the incident.
2. Take [Q-13](../../quizzes/Q-13.md) when your cohort opens it.
3. Export **operations dashboard notes and production RCA draft** using [student/worksheets/PF-ops.md](../../../student/worksheets/PF-ops.md).

The worksheet is the Module 13 portfolio artifact. Module 14 will assume you can hold 99.9% as the *operating* SLO while you design toward 99.99% as an *architecture* target.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/19-observability/overview.md` and `docs/27-production-failures/overview.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). They deepen signal design and failure analysis. This module stands alone without them.

---

## Guardrails

- Reuse OBSERVABILITY.md names. Do not invent a second SLI for the same `POST /api/v1/payments`.
- JSON logs: `ts`, `level`, `logger`, `msg`, `correlationId`, `paymentId`, `outcome`. No PAN, CVV, full account numbers, or `BAYPAY_DB_PASSWORD`.
- Metric labels stay low-cardinality: `uri`, `method`, `outcome`, `status`, `exception` (coarse). That is literacy. Lessons do not name INCIDENT-1301’s cause.
- Page on SLO burn and saturation that predicts burn. Do not page on “CPU > 80%” or “log contains ERROR” as the primary page.
- Never set `-Xmx` equal to container memory. Never recommend WebSphere ND in Docker. Never bounce `dmgr-east` as the ops answer.
- Paper Grafana JSON is enough. Do not require a live AMP/Grafana/CloudWatch stack to pass.
- Region is **`us-west-2`** when AWS is named. Do not apply OpenSearch or a second region for this module.
- 99.99% is Module 14. Do not upgrade the dashboard SLO here.
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`.
