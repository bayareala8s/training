# Module 2 — Advanced Java Concurrency

**Duration:** ~3 hours of lessons plus 3 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Safe concurrent payment processing  
**Portfolio artifact:** Concurrency RCA from [BREAKFIX-201](../../../labs/BREAKFIX-201/README.md) and [INCIDENT-202](../../../labs/INCIDENT-202/README.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, amount, log, and thread dump you see is synthetic.

---

## Business context

BayPay’s payment API is concurrent the moment a second request arrives. A merchant retry, a mobile double-tap, and a refund that races a capture all hit the same account. Throughput is not the hard part. The hard part is that **money and ledger rows must stay consistent** when eight worker threads, or eight hundred virtual threads, run `authorize` at the same time.

The modular monolith still shares one JVM. `payment-service` authorizes, `transaction-worker` posts the ledger, and `refund-service` reverses. Those modules share in-memory caches, idempotency maps, and — in a bad week — coarse locks. A lost update looks like a successful HTTP 201. A deadlock looks like a healthy process that has stopped completing work.

This module teaches the Java memory model, locks and atomics, concurrent collections, executors, `CompletableFuture`, virtual threads, and the failure modes that show up as duplicate charges or frozen workers. You will diagnose two production-shaped incidents and then design a path that does not repeat them.

Demo identities used in every lab:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |
| Merchant Harbor Bike Co | `merchant-harbor-bike` |
| Payment reference | `invoice-8841` |

Payment happy path: `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. Writes require an `Idempotency-Key`. In-process concurrency does not replace the database unique constraint on that key; it only decides whether the JVM itself lies before the row is written.

---

## Learning objectives

After this module you can:

- Explain happens-before, visibility, and why a worker can loop forever on a non-volatile “authorized” flag.
- Choose among `synchronized`, `volatile`, `Lock`, and atomics for a given BayPay invariant.
- Use concurrent collections for the operations they actually make atomic — and avoid compound check-then-act bugs.
- Structure authorize/post work with executors and `CompletableFuture` without leaking threads or swallowing failures.
- Decide when virtual threads help a blocking payment client and when they pin a carrier or hide overload.
- Diagnose races and deadlocks from logs, dashboards, and thread dumps without guessing the root cause first.
- Produce a portfolio-ready concurrency RCA from the duplicate-payment and hung-worker labs.

---

## Prerequisites

- Module 1 Java foundations (domain model, exceptions, enterprise habits).
- JDK 21 on `PATH` or `JAVA_HOME`. See [GETTING_STARTED.md](../../../GETTING_STARTED.md).
- Comfort reading a stack trace. You do not need prior JVM internals.

You do **not** need a global Maven install for the reference app. BREAKFIX-201’s starter compiles with `javac`.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional.

| Id | Title | What it unlocks |
|---|---|---|
| [L-2.1](lessons/L-2.1.md) | Threads and Java memory visibility | Why one thread’s write is invisible until a happens-before edge exists |
| [L-2.2](lessons/L-2.2.md) | synchronized, volatile, locks and atomics | Which primitive protects which invariant |
| [L-2.3](lessons/L-2.3.md) | Concurrent collections | Safe maps and queues — and the compound actions they do not cover |
| [L-2.4](lessons/L-2.4.md) | Executors and CompletableFuture | Bounded pools, completion stages, timeouts, and shutdown |
| [L-2.5](lessons/L-2.5.md) | Virtual threads | Blocking I/O at scale without a 400-thread platform pool |
| [L-2.6](lessons/L-2.6.md) | Race conditions and deadlocks | How BayPay loses money or stops making progress |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [BREAKFIX-201](../../../labs/BREAKFIX-201/README.md) | BREAK/FIX | Duplicate Payment Incident | L-2.1, L-2.2, L-2.6 |
| [INCIDENT-202](../../../labs/INCIDENT-202/README.md) | INCIDENT | Deadlocked Payment Workers | L-2.1, L-2.2, L-2.6 |
| [ARCHITECT-203](../../../labs/ARCHITECT-203/README.md) | ARCHITECT | Safe concurrent payment processing | L-2.3, L-2.4, L-2.5 |

Time-box BREAK/FIX and INCIDENT labs at 45–75 minutes. Do not open `solutions/` until you have a written hypothesis and a reproduction. BREAKFIX-201 and INCIDENT-202 do **not** include the root cause in the student guide. Request incident evidence in the order given in the incident pack.

---

## Assessment and portfolio

1. Complete the three labs.
2. Take [Q-02](../../quizzes/Q-02.md) (eight questions).
3. Export the concurrency RCA using [student/worksheets/PF-concurrency-rca.md](../../../student/worksheets/PF-concurrency-rca.md).

The RCA is the Module 2 portfolio artifact. Later modules assume you can talk about visibility, idempotency under concurrency, and lock policy without treating “add `synchronized` to the class” as an architecture.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, these notes add hardware and OS background. They are not required to finish the module.

- `docs/01-computer-architecture/memory-ordering-and-concurrency.md`
- `docs/02-operating-systems/processes-threads-and-scheduling.md`

Hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login.

---

## Guardrails

- Do not treat BayPay as a real employer architecture.
- Do not invent confidential runbooks. All dumps and metrics are synthetic.
- Local labs cost **$0**.
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`. A lucky guess does not max Diagnostic method.
