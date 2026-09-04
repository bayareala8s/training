# Module 7 — JVM Internals and Performance

**Duration:** ~3 hours of lessons plus 4 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** How the JVM spends memory and CPU for BayPay payments  
**Portfolio artifact:** JVM memory and GC observation notes from [student/worksheets/PF-jvm-observe.md](../../../student/worksheets/PF-jvm-observe.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, amount, dump, and metric you see is synthetic.

---

## Business context

When Harbor Bike Co charges Avery Chen `$84.00`, `payment-service` does not “use some RAM.” The HotSpot JVM that runs `BayPayApplication` spends **heap** on `Payment` and `Money`, **stack** frames on Tomcat and Hikari threads, **metaspace** on loaded `com.baypay` and Spring classes, and **native** memory on the code cache, GC structures, and direct buffers. CPU is spent interpreting, then JIT-compiling, then collecting the garbage those allocations become.

The teaching runtime is the same modular monolith as Modules 1–3: **Java 21**, **Spring Boot 3.5.5**, **G1 by default**, one process whose composition root is `payment-service`. Five Maven modules share that process. Local work uses `jcmd`, JFR, and GC logs. Docker is optional and appears only in LAB-704. There is no AWS lab and no cloud bill. Cost is **$0**.

This module is **observe and explain**. You will learn what `-Xmx` is (and is not), why RSS is larger than the heap, how Spring Boot’s fat-JAR loader sits on the application class loader, why C1/C2 need warmup, how G1 young and old collections differ, how `Money.plus` and a logging storm allocate, and why a container cgroup limit is not a heap size. You will not chase a 1% GC pause win.

Demo identities stay locked:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |

Synthetic prod-east names you may see in examples (not live hosts): `pay-prod-east-1` (stable `payment-service` 3.8.0), `pay-prod-east-2` (canary). On-call: Riley Okonkwo. SRE: Priya Nair. Release: Jordan Voss. Teaching notes: [datasets/baypay-jvm/RUNTIME.md](../../../datasets/baypay-jvm/RUNTIME.md).

Module 8 will later page you with **symptom classes** — high CPU, a growing retained set, long GC, a heap `OutOfMemoryError`, a container OOM kill. This module gives you the map. It does not hand you those incident RCAs.

---

## Learning objectives

After this module you can:

- Name heap, stacks, metaspace, and native memory in a running `payment-service`, and contrast `-Xmx` with process RSS using NMT.
- Explain how `Payment` is loaded (application class loader vs Spring Boot’s launched loader) and why metaspace is not the Java heap.
- Describe HotSpot tiered JIT (interpreter, C1, C2), warmup, and deoptimization — and why `-Xcomp` is not a production warmup plan.
- Read a G1 young vs old story from `-Xlog:gc` without treating every pause as a defect.
- Connect TLAB allocation, escape analysis, `Money` copies, and boxing or logging storms to allocation rate.
- Size a containerized JVM so the cgroup limit has headroom for non-heap memory. Never set `-Xmx` equal to the container limit.

---

## Prerequisites

- Modules 1–3: `Money`, `Payment`, the state machine, and the Boot `payment-service` API.
- L-1.1 (JDK vs JVM) and L-4.4 (class loaders and sessions) help; this module still stands alone.
- JDK 21 on `PATH` or `JAVA_HOME`. `jcmd` ships with that JDK. See [GETTING_STARTED.md](../../../GETTING_STARTED.md).
- A terminal. You do **not** need a global Maven install (`./mvnw` is in the reference app).
- Docker or Podman is **optional** and used only if you run LAB-704. Labs 701–703 are local process work.

You do **not** need AWS, a heap-dump service, or production JMX.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional.

| Id | Title | What it unlocks |
|---|---|---|
| [L-7.1](lessons/L-7.1.md) | Heap, stacks, metaspace and native memory | What `-Xmx` covers and why RSS is larger |
| [L-7.2](lessons/L-7.2.md) | Class loading | App loader, Spring Boot launched loader, metaspace |
| [L-7.3](lessons/L-7.3.md) | JIT compilation | C1/C2, warmup, deopt; do not `-Xcomp` in prod |
| [L-7.4](lessons/L-7.4.md) | Garbage collection | G1 young/old, pause vs throughput, `-Xlog:gc` |
| [L-7.5](lessons/L-7.5.md) | Allocation behavior | TLAB, escape analysis, `Money`, logging/boxing |
| [L-7.6](lessons/L-7.6.md) | JVM in containers | cgroup vs `-Xmx`, `MaxRAMPercentage`, native headroom |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [LAB-701](../../../labs/LAB-701/README.md) | PERFORMANCE | Observe JVM memory | L-7.1 |
| [LAB-702](../../../labs/LAB-702/README.md) | PERFORMANCE | Controlled object allocation | L-7.5 |
| [LAB-703](../../../labs/LAB-703/README.md) | PERFORMANCE | Observe GC | L-7.4 |
| [LAB-704](../../../labs/LAB-704/README.md) | PERFORMANCE | JVM and container memory experiment | L-7.6 |

Time-box each PERFORMANCE lab at 60–90 minutes. Use local `jcmd`, JFR, and GC logs. Docker is optional and only for LAB-704. Do not open `solutions/` until you have recorded your own numbers. Cost **$0**. No AWS.

---

## Assessment and portfolio

1. Complete LAB-701, LAB-702, LAB-703, and LAB-704 (704 on paper or with local Docker).
2. Take [Q-07](../../quizzes/Q-07.md) (eight questions).
3. Export observation notes using [student/worksheets/PF-jvm-observe.md](../../../student/worksheets/PF-jvm-observe.md).

The worksheet is the Module 7 portfolio artifact. Later modules assume you can point at a `payment-service` process and say which memory pool a number came from, and that you will not set `-Xmx` to the container limit.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/01-computer-architecture/cpu-and-memory-fundamentals.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). It is background on caches and RAM. This module stands alone without it.

---

## Guardrails

- Do not treat BayPay, `pay-prod-east-*`, or Avery Chen as a real employer estate.
- Observe and explain. Do not tune G1 for a 1% win.
- Do not set `-Xmx` equal to the container (cgroup) memory limit. Leave headroom for metaspace, stacks, and native.
- Do not treat a single heap histogram as a closed leak without a growth story.
- Local `jcmd` / JFR / GC logs only. Docker optional for LAB-704. No AWS. Cost **$0**.
- Module 5 WAS cells are a different estate. Do not bounce `dmgr-east` for a Boot canary page.
- Instructor rubrics live under `instructor/rubrics/`. Students should not need them to finish the work.
