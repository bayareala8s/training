# Module 1 — Enterprise Java Engineering

**Duration:** ~4 hours of lessons plus 4 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Modern Java foundations for the BayPay Enterprise Payment Platform  
**Portfolio artifact:** Java domain model excerpt from [BUILD-101](../../../labs/BUILD-101/README.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, amount, and log you see is synthetic.

---

## Business context

BayPay moves money for small and mid-size merchants. A payment is not a row you insert and forget. It is a **lifecycle**: the request is received, validated, authorized, posted to a ledger, and only then marked complete. A retry from a flaky mobile client must not debit Avery Chen twice. A frozen account must not authorize. A USD payment must not post against a GBP account.

The platform that does this work is a **modular monolith** on **Java 21** and **Spring Boot 3.5.5**. Five Maven modules share one process and one database today:

| Module | Responsibility |
|---|---|
| `shared` | Domain types, state machine, JPA, idempotency |
| `payment-service` | HTTP API and composition root |
| `refund-service` | Refund use cases |
| `transaction-worker` | Ledger posting after authorization |
| `notification-service` | Completion notifications |

Module 1 does not yet teach Spring, concurrency, or Kubernetes. It teaches the Java that those later modules assume: a JDK you can trust, objects that protect invariants, collections that stay type-safe, exceptions that mean something, and coding habits that survive a production on-call rotation.

Demo identities used in every lab:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |

Payment happy path: `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. Failure and reversal states: `DECLINED`, `FAILED`, `REVERSED`. Writes require an `Idempotency-Key`.

---

## Learning objectives

After this module you can:

- Explain how the JDK, bytecode, and JVM relate, and why BayPay pins Java 21 LTS.
- Design value objects and entities so money and payment state cannot be mutated into an illegal combination, and apply SOLID as a review vocabulary on those types.
- Choose collections and generic types that keep a payment state machine and currency set honest at compile time.
- Use exceptions, records, streams, and `Optional` without hiding failures or inventing nulls.
- Apply enterprise practices — package boundaries, idempotency, correlation ids, structured logs — to code you would merge on a payments team.
- Produce a portfolio-ready excerpt of the BayPay domain model and defend its invariants in an interview.

---

## Prerequisites

- Working Java knowledge (classes, methods, basic collections).
- Git and a terminal.
- REST vocabulary (`POST`, headers, JSON). You do not need Spring experience yet.
- JDK 21 on `PATH` or `JAVA_HOME`. See [GETTING_STARTED.md](../../../GETTING_STARTED.md).

You do **not** need a global Maven install. The reference app ships `./mvnw`.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional.

| Id | Title | What it unlocks |
|---|---|---|
| [L-1.1](lessons/L-1.1.md) | Modern Java, JDK and JVM overview | How BayPay’s runtime is assembled and why version pinning matters |
| [L-1.2](lessons/L-1.2.md) | Object design, SOLID and immutability | SOLID letters on BayPay types; why `Money` is a value and `Payment` owns transitions |
| [L-1.3](lessons/L-1.3.md) | Collections and generics | `EnumSet` transitions, currency sets, and type-safe ledgers |
| [L-1.4](lessons/L-1.4.md) | Exceptions, records, streams and Optional | Fail loudly, model decisions as records, query without nulls |
| [L-1.5](lessons/L-1.5.md) | Enterprise coding practices | Idempotency, correlation, packages, and review habits |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [BUILD-101](../../../labs/BUILD-101/README.md) | BUILD | Build the BayPay transaction domain model | L-1.2, L-1.3 |
| [BUILD-102](../../../labs/BUILD-102/README.md) | BUILD | Implement payment validation | L-1.4, L-1.5 |
| [FIX-103](../../../labs/FIX-103/README.md) | BREAK/FIX | Refactor deliberately poor Java | L-1.4, L-1.5 |
| [CHALLENGE-104](../../../labs/CHALLENGE-104/README.md) | PERFORMANCE | Optimize transaction processing | L-1.5 |

Time-box BUILD labs at 60–90 minutes. Do not open `solutions/` until you have attempted the lab. FIX-103 and CHALLENGE-104 do not include the answer in the student guide.

---

## Assessment and portfolio

1. Complete the four labs.
2. Take [Q-01](../../quizzes/Q-01.md) (eight questions).
3. Export the domain model excerpt using [student/worksheets/PF-domain-model.md](../../../student/worksheets/PF-domain-model.md).

The excerpt is the Module 1 portfolio artifact. Later modules assume you can point at `Money`, `PaymentStatus`, and the state machine and explain why an illegal transition is rejected in the domain, not in a controller.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/09-transactions/overview.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). It is supplemental background on transactional consistency. This module stands alone without it. Course index: [PAKS_LINKS.md](../../../PAKS_LINKS.md).

---

## Guardrails

- Do not treat BayPay as a real employer architecture.
- Do not commit secrets. Local labs cost **$0**.
- Instructor rubrics live under `instructor/rubrics/`. Students should not need them to finish the work.
