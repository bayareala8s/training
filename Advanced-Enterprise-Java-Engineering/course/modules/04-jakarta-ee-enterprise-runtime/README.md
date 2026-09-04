# Module 4 — Jakarta EE and Enterprise Runtime Concepts

**Duration:** ~2.5 hours of lessons plus 3 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Map Spring skills onto the enterprise runtime  
**Portfolio artifact:** Spring-to-Jakarta mapping brief from [ARCHITECT-401](../../../labs/ARCHITECT-401/README.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, amount, log, and metric you see is synthetic.

---

## Business context

BayPay’s **current** teaching runtime is the modular monolith in `reference-apps/baypay/`: Java 21, Spring Boot, an embedded servlet container, HikariCP, JPA, and Spring transactions. That stack is not magic. Almost every annotation you used in Module 3 is a convenience over a **Jakarta EE contract** — `Servlet`, `Filter`, `DataSource`, `EntityManager`, `UserTransaction`, JMS, JNDI.

BayPay is also **modernizing from** a traditional application-server estate. Payment and refund ears once looked up `jdbc/baypay` and `jms/paymentEvents` in a cell-wide JNDI tree. Module 5 covers WebSphere Network Deployment as that current-state topology. This module teaches the concepts those servers implemented so you can read a Spring Boot service *and* a legacy EAR without treating either as folklore.

**Greenfield stance:** do **not** start a new BayPay service on traditional WebSphere ND. Prefer Spring Boot or a modern Liberty / Open Liberty profile with externalized configuration. Learn the old runtime so you can migrate it, operate it until cutover, and interview about it — not so you can recommend it for a blank page.

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |

Payment happy path: `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. Writes require an `Idempotency-Key`. Ledger posting today runs **in-process** on the same Spring transaction as `POST /api/v1/payments`.

---

## Learning objectives

After this module you can:

- Explain the servlet container as the HTTP runtime under Spring MVC, using BayPay’s `CorrelationIdFilter` as a Jakarta `Filter`.
- Map JPA, JTA, JMS, and JNDI to the Spring types you already used (`JpaRepository`, `@Transactional`, application events, `application.yml`).
- Read DataSource and connection-pool metrics, and diagnose exhaustion without guessing.
- Reason about HTTP sessions, sticky routing, and application-server class loaders — including why a leak survives a “fix” that never unloads the old WAR.
- Describe what an application server actually provides (pools, JTA, JNDI, class loading, deployment) versus what Spring Boot embeds, and why traditional WAS is a **source** estate, not a greenfield target.
- Produce a portfolio-ready Spring-to-Jakarta mapping brief and work two gated incidents (pool timeouts; completed payment with a missing ledger row).

---

## Prerequisites

- Modules 1–3, including the BayPay domain model and Spring Boot payment API.
- JDK 21 and the Maven Wrapper. See [GETTING_STARTED.md](../../../GETTING_STARTED.md).
- Comfort reading `PaymentApplicationService`, `PaymentPostingService`, and `application-*.yml`.

You do **not** need a WebSphere installation. Module 5 uses architecture and incident assets for ND. This module uses the reference app plus paper/evidence labs.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional.

| Id | Title | What it unlocks |
|---|---|---|
| [L-4.1](lessons/L-4.1.md) | Servlet and Jakarta EE model | Request thread, `Filter`, `DispatcherServlet` |
| [L-4.2](lessons/L-4.2.md) | JPA, JTA, JMS and JNDI | Persistence, transactions, messaging, lookup |
| [L-4.3](lessons/L-4.3.md) | DataSources and connection pools | Pool math, waiters, leak candidates |
| [L-4.4](lessons/L-4.4.md) | Sessions and class loading | Affinity, parent-first / parent-last, leaks |
| [L-4.5](lessons/L-4.5.md) | Application server fundamentals | What the server owns vs what Spring embeds |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [ARCHITECT-401](../../../labs/ARCHITECT-401/README.md) | ARCHITECT | Map Spring to Jakarta concepts | L-4.1, L-4.2, L-4.5 |
| [INCIDENT-402](../../../labs/INCIDENT-402/README.md) | INCIDENT | Connection pool exhaustion | L-4.3 |
| [INCIDENT-403](../../../labs/INCIDENT-403/README.md) | INCIDENT | Transaction boundary failure | L-4.2, L-4.5 |

Time-box ARCHITECT-401 at 60–90 minutes and incident labs at 45–75 minutes. INCIDENT-402 and INCIDENT-403 do **not** include the root cause in the student guide. Do not open `solutions/` until you have written a hypothesis from evidence.

---

## Assessment and portfolio

1. Complete ARCHITECT-401 and both incidents.
2. Take [Q-04](../../quizzes/Q-04.md) (eight questions).
3. Export the mapping brief using [student/worksheets/PF-spring-jakarta.md](../../../student/worksheets/PF-spring-jakarta.md).

The mapping brief is the Module 4 portfolio artifact. Capstone 2 (after Modules 4–10) will assume you can point at a Spring annotation and name the Jakarta contract underneath it.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/09-transactions/overview.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). Isolation, 2PC, and the outbox pattern deepen L-4.2 and INCIDENT-403. This module stands alone without it.

---

## Guardrails

- Do not treat BayPay as a real employer architecture.
- Historical WebSphere / JNDI appears here for **modernization literacy**. It is not the recommended greenfield runtime.
- Local labs and incident packs cost **$0**.
- Instructor rubrics live under `instructor/rubrics/`. Students should not need them to finish the work.
