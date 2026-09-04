# Module 8 — JVM Troubleshooting

**Duration:** ~3.5 hours of lessons plus 6 incident labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Diagnose live BayPay JVM failures on the Boot canary (`pay-prod-east-2`), not the WAS cell  
**Portfolio artifact:** JVM incident RCA from [student/worksheets/PF-jvm-rca.md](../../../student/worksheets/PF-jvm-rca.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, hostname, dump, histogram, and metric you see is synthetic. Do not treat these packs as a real employer’s JVM estate.

**Delivery note:** this module is **gated simulation**. You diagnose from dashboards, logs, thread-print text, heap *summaries*, GC logs, and container gauges that the packs reveal in order. You do **not** download a multi-gigabyte `heap.hprof`. You do **not** bounce `dmgr-east`, `Pay2`, or anything on `BayPayCell`. Pages in this module land on the Spring Boot canary.

---

## Business context

Module 7 taught you to *observe* a Java 21 / Spring Boot 3.5.5 JVM: heap, stacks, metaspace, native, G1, allocation, container limits. This module asks you to *diagnose* when that JVM is already hurting merchants.

The teaching process is `payment-service` in `reference-apps/baypay`. The synthetic prod-east estate is locked in [datasets/baypay-jvm/RUNTIME.md](../../../datasets/baypay-jvm/RUNTIME.md):

| Instance | Role |
|---|---|
| `pay-prod-east-1` | Stable `payment-service` 3.8.0 — usually healthy |
| `pay-prod-east-2` | **Canary** — first place Module 8 pages land |
| `fx-east.baypay.example` | Downstream quote service (only when a pack mentions it) |
| Container (when named) | cgroup memory limit stated in that pack |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |

On-call names in the packs: **Riley Okonkwo** (application), **Priya Nair** (SRE), **Jordan Voss** (release). A canary page is a Boot JVM problem until evidence says otherwise. Module 5’s cell (`dmgr-east`, `PaymentCluster`, FFDC, PMI) is a different estate.

Payment happy path is still `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. Finance cares that Avery Chen’s authorize completes. Actuator `liveness` UP is not that sentence.

---

## Learning objectives

After this module you can:

- Capture and read a thread dump (`jstack` / `jcmd Thread.print`) and separate RUNNABLE, BLOCKED, WAITING, and safepoint effects.
- Reason from a class histogram and a retained-size story without opening a 2 GB binary dump.
- Attribute CPU saturation to runnable application work, GC, or native — not “CPU means GC.”
- Separate a leak (growth + dominators) from a heap that is simply too small for the live set.
- Read `-Xlog:gc` and tell allocation-rate pain from pause-time pain from a leak.
- Diagnose thread-pool starvation (HTTP threads waiting on an executor or a downstream) without assuming every hang is Hikari.
- Distinguish Java heap `OutOfMemoryError` from a cgroup OOMKill, and leave native headroom.
- Write a portfolio RCA from gated evidence. A lucky label (leak, deadlock, OOM) does **not** max Diagnostic method.

---

## Prerequisites

- Modules 1–6, especially L-2.6 (race vs hang *shapes*), L-4.3 (pool gauges), and L-5.6 (smallest bounce on the *cell*).
- Module 7 JVM internals: heap vs native, G1, allocation, container awareness. If Module 7 labs are unfinished, read L-7.1, L-7.4, L-7.5, and L-7.6 before the first incident.
- JDK 21 locally if you want to practice `jcmd` on the reference app. See [GETTING_STARTED.md](../../../GETTING_STARTED.md) and [RUNTIME.md](../../../datasets/baypay-jvm/RUNTIME.md).
- Comfort with the incident habit from INCIDENT-402: dashboard first, then logs, then deeper JVM evidence.

You do **not** need VisualVM, Eclipse MAT, or a production attach to `pay-prod-east-2`. Packs ship text summaries.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional. Lessons teach **method**. They do not name the root cause of any INCIDENT-80x pack.

| Id | Title | What it unlocks |
|---|---|---|
| [L-8.1](lessons/L-8.1.md) | Thread-dump analysis | States, locks, safepoints, `jcmd Thread.print` |
| [L-8.2](lessons/L-8.2.md) | Heap-dump reasoning | Histogram vs leak; summaries, not binary dumps |
| [L-8.3](lessons/L-8.3.md) | CPU saturation | Runnable stacks and flame-ish attribution |
| [L-8.4](lessons/L-8.4.md) | Memory leaks | Growth, dominators, ThreadLocal, unbounded caches |
| [L-8.5](lessons/L-8.5.md) | GC pauses | Allocation rate vs heap too small vs leak; `-Xlog:gc` |
| [L-8.6](lessons/L-8.6.md) | Thread starvation | Exhausted pools, queued work, HTTP waiting on work |
| [L-8.7](lessons/L-8.7.md) | Container OOM | cgroup kill vs Java heap OOM; native headroom |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [INCIDENT-801](../../../labs/INCIDENT-801/README.md) | INCIDENT | CPU 98 percent | L-8.3 |
| [INCIDENT-802](../../../labs/INCIDENT-802/README.md) | INCIDENT | Memory leak | L-8.2, L-8.4 |
| [INCIDENT-803](../../../labs/INCIDENT-803/README.md) | INCIDENT | Deadlock | L-8.1 |
| [INCIDENT-804](../../../labs/INCIDENT-804/README.md) | INCIDENT | Thread-pool exhaustion | L-8.6 |
| [INCIDENT-805](../../../labs/INCIDENT-805/README.md) | INCIDENT | Excessive GC | L-8.5 |
| [INCIDENT-806](../../../labs/INCIDENT-806/README.md) | INCIDENT | Container OOM | L-8.7 |

Time-box each incident at 45–75 minutes. Student guides show **symptoms only**. Work the pack’s gates (`timeline.json`). Do not open `solutions/INCIDENT-80x/` until the worksheet has hypothesis, evidence, next investigation, stabilize, remediate, and comms.

INCIDENT-202 (Module 2) was a *different* hang on a canary worker pair. INCIDENT-402 was Hikari. Do not paste those RCAs into these packs. Quote *this* pack’s evidence.

A one-word guess that happens to match the title does **not** max Diagnostic method. Instructors score the path.

---

## Assessment and portfolio

1. Complete all six incidents with gated evidence in order.
2. Take [Q-08](../../quizzes/Q-08.md) when your cohort opens it.
3. Export the JVM incident RCA using [student/worksheets/PF-jvm-rca.md](../../../student/worksheets/PF-jvm-rca.md).

The worksheet is the Module 8 portfolio artifact. Later container and Kubernetes modules assume you can tell a heap OOM from a cgroup kill and a deadlock dump from a starved pool.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/27-production-failures/failure-analysis-methodology.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). It deepens evidence order and stabilize-versus-remediate. This module stands alone without it.

---

## Guardrails

- Diagnose the **Boot canary** (`pay-prod-east-2`). Do not restart `BayPayCell` for a payment-service page.
- Simulation first: text dumps and summaries. Never require a 2 GB `hprof` in the course.
- Do not set `-Xmx` equal to the container memory limit. Leave room for metaspace, stacks, and native (L-8.7).
- A class histogram is not a closed leak without a growth story (L-8.2, L-8.4).
- Do not treat BayPay as a real employer architecture. No confidential dumps.
- Local incident packs cost **$0**.
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`.
