# Module 3 — Spring Boot Engineering

**Duration:** ~3 hours of lessons plus 5 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Production Spring Boot for BayPay APIs  
**Portfolio artifact:** Payment and refund API from [BUILD-301](../../../labs/BUILD-301/README.md) and [BUILD-302](../../../labs/BUILD-302/README.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, amount, and log you see is synthetic.

---

## Business context

Module 1 taught the Java that protects money. Module 2 taught the concurrency that must not double-post it. Module 3 is where those types become an HTTP service operators can run.

BayPay’s merchant app retries. A flaky mobile client will `POST /api/v1/payments` twice with the same `Idempotency-Key`. Finance will ask why a refund returned `201` when the ledger has no matching row. Kubernetes will kill a pod that answers liveness while the DataSource is still down. None of those are “Spring tutorials.” They are production contracts on one modular monolith: **Spring Boot 3.5.5**, Java 21, five Maven modules, H2 locally, PostgreSQL in the `prod` profile.

The APIs already exist in `reference-apps/baypay/`. This module does not invent a second stack. You will implement, rebuild, and extend against that app until you can defend every status code and every transaction boundary.

| HTTP contract | Behavior you must be able to explain |
|---|---|
| `POST /api/v1/payments` | `Idempotency-Key` required; `201` create, `200` replay, `422` declined |
| `GET /api/v1/payments/{id}` | `200` or ProblemDetail `404` |
| `POST /api/v1/refunds` | Same idempotency rules; cannot over-refund Avery Chen |
| `GET /api/v1/refunds/{id}` | `200` or ProblemDetail `404` |
| `/actuator/health`, `/liveness`, `/readiness` | Process alive versus ready to take traffic |
| `/v3/api-docs` | OpenAPI published from the running app |

Errors are RFC 7807 `ProblemDetail` with a BayPay `code`. Local profile uses H2 in PostgreSQL compatibility mode. Production profile points at PostgreSQL and hides health details.

---

## Learning objectives

After this module you can:

- Wire BayPay services with constructor injection and explain what the IoC container owns versus what the domain owns.
- Design REST write endpoints that validate input, require `Idempotency-Key`, and distinguish create, replay, and decline.
- Map domain exceptions to `ProblemDetail` without leaking stack traces, and separate local versus `prod` configuration.
- Persist `Payment`, `Refund`, and ledger rows with JPA, choose a transaction boundary, and say when rollback must happen.
- Expose Actuator liveness and readiness that a load balancer can trust.
- Test the payment and refund contracts with `@SpringBootTest`, MockMvc, and an optional Testcontainers PostgreSQL check.
- Produce a portfolio-ready payment and refund API excerpt and defend it in an interview.

---

## Prerequisites

- Modules 1 and 2, or equivalent comfort with the BayPay domain model and the payment state machine.
- Working Java 21, Git, and REST vocabulary.
- JDK 21 on `PATH` or `JAVA_HOME`. See [GETTING_STARTED.md](../../../GETTING_STARTED.md).

You do **not** need a global Maven install. The reference app ships `./mvnw`. You do not need a second framework, a second database product for the happy path, or a microservice mesh.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional.

| Id | Title | What it unlocks |
|---|---|---|
| [L-3.1](lessons/L-3.1.md) | IoC and dependency injection | How `PaymentController` gets a service without `new` |
| [L-3.2](lessons/L-3.2.md) | REST APIs and validation | Idempotent POST, Bean Validation, OpenAPI |
| [L-3.3](lessons/L-3.3.md) | Exception handling and configuration | ProblemDetail, profiles, correlation ids |
| [L-3.4](lessons/L-3.4.md) | JPA and transaction management | Entities, H2 versus Postgres, rollback |
| [L-3.5](lessons/L-3.5.md) | Actuator and production health | Liveness, readiness, what not to expose |
| [L-3.6](lessons/L-3.6.md) | Testing | MockMvc ITs and Testcontainers discipline |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [BUILD-301](../../../labs/BUILD-301/README.md) | BUILD | Payment REST API | L-3.1, L-3.2 |
| [BUILD-302](../../../labs/BUILD-302/README.md) | BUILD | Refund API | L-3.2 |
| [BUILD-303](../../../labs/BUILD-303/README.md) | BUILD | Persistence | L-3.4 |
| [FIX-304](../../../labs/FIX-304/README.md) | BREAK/FIX | Transaction rollback bug | L-3.4 |
| [BUILD-305](../../../labs/BUILD-305/README.md) | BUILD | Health and readiness endpoints | L-3.5 |

Time-box BUILD labs at 60–90 minutes. L-3.6 applies to every lab: write or run the tests that prove the contract. Do not open `solutions/` until you have attempted the lab. FIX-304 does **not** include the answer in the student guide.

---

## Assessment and portfolio

1. Complete the five labs.
2. Take [Q-03](../../quizzes/Q-03.md) (eight questions).
3. Export the payment and refund API excerpt as the Module 3 portfolio artifact: controller contracts, idempotency behavior, and the transaction boundary you would defend in Capstone 1.

Later modules assume you can point at `PaymentController`, `ApiExceptionHandler`, and `@Transactional` on `PaymentApplicationService.create` and explain `201` versus `200` versus `422` without opening a tutorial.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/15-api-and-integration-architecture/overview.md` and `docs/14-microservices/overview.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). They are supplemental background on API contracts and when not to split a monolith. This module stands alone without them.

---

## Guardrails

- Do not treat BayPay as a real employer architecture.
- Do not invent a second application stack. Work in `reference-apps/baypay/`.
- Do not commit secrets. Local labs cost **$0**. PostgreSQL via Testcontainers is optional and destroyed with the JVM.
- Instructor rubrics live under `instructor/rubrics/`. Students should not need them to finish the work.
