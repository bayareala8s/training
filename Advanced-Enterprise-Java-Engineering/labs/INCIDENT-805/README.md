# INCIDENT-805 — Excessive GC

**Type:** INCIDENT  
**Module:** 08 — JVM Troubleshooting  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/jvm/INC-JVM-805](../../incidents/jvm/INC-JVM-805/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

15:33 Pacific on a synthetic prod-east afternoon in October 2026. Harbor Market reports that `POST /api/v1/payments` p99 jumped into the hundreds of milliseconds and some requests stall during long pauses. The pager names G1 pause time on `pay-prod-east-2`. Actuator still returns up. Heap used sawtooths but old generation is not the two-day climb you may have seen in another Module 8 pack. `pay-prod-east-1` is quiet. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry is more work on a JVM that is already spending a large fraction of time in garbage collection. Finance does not care that G1 is “working as designed.” They care that authorizations miss the SLO while someone is “just looking at logs.”

`pay-prod-east-1` remaining healthy is part of the first sentence. Do not bounce Postgres. Do not bounce `dmgr-east`. Runtime names: [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).

---

## Learning objectives

- Follow gated evidence: dashboard first, then the GC log excerpt, then the heap histogram.
- Treat **long G1 pauses** as a symptom of allocation or a retained set, not as a collector bug by default.
- Separate a short-lived allocation storm from INCIDENT-802’s old-generation climb.
- Write stabilization that restores latency without a region failover.
- Produce a comms update that does not announce a leak before the histogram supports one.

---

## Architecture

```text
Merchants / Avery Chen
  → load balancer
       → pay-prod-east-1   payment-service 3.8.0   (stable)
       → pay-prod-east-2   payment-service canary  (first place this page lands)
            G1 (default in RUNTIME.md)
            application + framework logging
            → baypay DB
```

One process composition root. You do not need a live `gc.log` from your laptop. The contracts are pause time, allocation rate, and whether the histogram is ephemeral `String`/`char[]` or a retained domain class. Module 7 taught you to observe; this lab asks you to act.

---

## Prerequisites

- L-8.5 (GC pauses) completed, or read in the same sitting. Module 7 observation labs help but are not a substitute for gate order.
- Locked runtime names from [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).
- Incident worksheet: [student-worksheet.md](../../incidents/jvm/INC-JVM-805/student-worksheet.md).
- Optional PAKS: `docs/27-production-failures/failure-analysis-methodology.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/jvm/INC-JVM-805/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 2 is a **GC log excerpt**, not `logs.txt`. The pack README documents what shipped and what was omitted. Do not invent a thread dump.

Do not open `solutions/INCIDENT-805/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note what changed in the hour before the page (deploy, flag, or config).
2. **Gate 1:** open `evidence/dashboard.md` only. Record pause p99, allocation rate, old gen, and whether `pay-prod-east-1` shares the pause. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/gc.log`. Update the hypothesis. Quote pause lines; do not promote “G1 is broken” to a closed RCA.
4. **Gate 3:** open `evidence/heap-histogram.md` only if it answers a question you already wrote about what is being allocated or retained.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Jordan Voss).
6. Optional: one sentence on how `-Xlog:gc*` on the local `reference-apps/baypay` process relates to this teaching excerpt — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “excessive GC” or “leak” with no allocation-versus-retained story scores low on Diagnostic method (see rubric). Skipping to the histogram before a written question also scores low.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Pauses are long and old gen is flat: that is data. Write it.
- You want application `logs.txt`: it is not in this pack. Use the timeline plus dashboard plus GC log.
- You are about to bounce Postgres or `dmgr-east`: re-read RUNTIME.md.
- You want to switch collectors in the incident: write what that would prove in the next ten minutes.
- Histogram is `String` / `char[]`: say whether instances look retained (802-shaped) or churned (young).
- You copied INCIDENT-802’s cache story: check whether `IdempotencyRecord` dominates **this** histogram.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which config change lit the allocation rate.

---

## Interview questions

1. Why is “G1 is broken” a weak first sentence when east-1 on the same collector is fine?
2. What is the difference between a 400 ms pause and a leak you can only see after two days?
3. Why can allocation rate of gigabytes per second still leave old gen flat?
4. When is a DEBUG flag an incident trigger rather than a support convenience?
5. What would you refuse to log on a hot payment path even at INFO?

---

## Architecture/trade-off questions

1. Structured field logging versus dumping a whole payment object on a hot path — which belongs in production?
2. Rate-limit DEBUG per logger versus a global `com.baypay` level?
3. If someone needs to “trace Avery,” what correlation-id sampling would you rather ship?
4. Why is tuning `-XX:MaxGCPauseMillis` a weak remediation if allocation rate is the thing that changed?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live GC log from a profiler vendor.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-805/` and `instructor/rubrics/INCIDENT-805.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

Pause time is a first-class signal and still only a symptom. Allocation rate plus a young histogram tells a different story than an old-gen climb. Stabilization (revert the config that changed) is a different sentence from remediation (what you allow on the hot path next week). A lucky “GC” label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-JVM-805 worksheet to your notes if this is the Module 8 incident you will write up. The Module 8 portfolio artifact is [student/worksheets/PF-jvm-rca.md](../../student/worksheets/PF-jvm-rca.md): you pick **one** of INCIDENT-801 through INCIDENT-806 and write the scored RCA there.
