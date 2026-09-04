# INCIDENT-801 — CPU 98 percent

**Type:** INCIDENT  
**Module:** 08 — JVM Troubleshooting  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/jvm/INC-JVM-801](../../incidents/jvm/INC-JVM-801/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

10:18 Pacific on a synthetic prod-east morning in October 2026. Harbor Market reports that `POST /api/v1/payments` is taking many seconds on some requests and then succeeding or timing out. The pager names `payment-service` on `pay-prod-east-2`. Process CPU on that instance is **98 percent**. Actuator still returns up. `pay-prod-east-1` is quiet. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry is another HTTP thread on whichever replica the load balancer still considers healthy. Finance does not care that the JVM process is alive. They care that authorizations are not completing for the merchants who landed on the hot canary.

`pay-prod-east-1` remaining healthy is part of the first sentence you write, not a footnote. Do not widen the page to Postgres or to `dmgr-east`. This estate is the Boot canary described in [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).

---

## Learning objectives

- Follow gated evidence: dashboard first, then logs, then the thread dump.
- Treat **98 percent CPU** as a symptom that still needs a stack story, not as a finished RCA.
- Separate “the process is busy” from “the process is waiting” before you pick a stabilize move.
- Write stabilization that restores capacity on the canary without bouncing the database or the whole region.
- Produce a comms update that does not invent a cause you have not quoted.

---

## Architecture

```text
Merchants / Avery Chen
  → load balancer
       → pay-prod-east-1   payment-service 3.8.0   (stable)
       → pay-prod-east-2   payment-service canary  (first place this page lands)
            → baypay DB
            → optional downstreams named in the pack
```

One process composition root (`payment-service`). You do not need a live JVM. The contracts are HTTP threads, process CPU, and whatever the dump shows those threads doing. Module 5 WAS cells are a different estate.

---

## Prerequisites

- L-8.1 (thread-dump analysis) and L-8.3 (CPU saturation) completed, or read in the same sitting.
- Locked runtime names from [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).
- Incident worksheet: [student-worksheet.md](../../incidents/jvm/INC-JVM-801/student-worksheet.md).
- Optional PAKS: `docs/27-production-failures/failure-analysis-methodology.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/jvm/INC-JVM-801/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset** of the evidence kinds the course catalog lists. The pack README documents what shipped and what was omitted. Do not invent a heap histogram or a GC death spiral that the dashboard contradicts.

Do not open `solutions/INCIDENT-801/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note the gate rules, who deployed, and which instance paged.
2. **Gate 1:** open `evidence/dashboard.md` only. Record CPU, latency, error rate, and whether `pay-prod-east-1` shares the page. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote correlation ids and durations; do not promote a log phrase to a closed RCA.
4. **Gate 3:** open `evidence/thread-dump.txt` only if it answers a question you already wrote about what the hot threads are doing.
5. Write stabilization, remediation, and a 5-line comms update on the worksheet. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Jordan Voss).
6. Optional: one sentence on how you would confirm the same stacks with `jcmd <pid> Thread.print` on the local `reference-apps/baypay` process — literacy only; you do not need to reproduce the page.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky one-word guess with empty evidence scores low on Diagnostic method (see rubric). Skipping to the dump before a written question also scores low.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- CPU is high and merchants still get some 200s: that is data. Write the contradiction.
- You want a heap histogram: it is not in this pack. Say so and work with dashboard, logs, and the dump.
- You are about to bounce Postgres or `dmgr-east`: re-read RUNTIME.md. This is a Boot canary page.
- Dashboard says east-1 is healthy and you still want a region failover: write why that would or would not help Avery Chen.
- Many threads look `RUNNABLE`: quote the frames; do not stop at the state word.
- You recognized a JDK class in the dump and wrote the answer in one word: keep going — Diagnostic method still needs gate order and quotes.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you the mechanism.

---

## Interview questions

1. Why is “the CPU is high” a weak first sentence when `pay-prod-east-1` is at 12 percent and still completing Avery Chen’s payment?
2. What is the difference between a `RUNNABLE` thread and a proven hot method?
3. Why can Actuator liveness stay UP while p99 on `POST /api/v1/payments` is several seconds?
4. When do you remove a canary from the load balancer versus bouncing the process in place?
5. What would a second dump one minute later confirm or refute that a single dump cannot?

---

## Architecture/trade-off questions

1. Should a request-body inspection run on the HTTP thread that also talks to the ledger, or on a bounded sidecar with a size cap?
2. Where would you put a body-size limit relative to a legitimate Harbor Market checkout payload?
3. If the canary is 3.8.1 and the stable replica is 3.8.0, what do you learn from that split that a single-instance page would hide?
4. Why is “add more replicas” a weak first stabilize when only the canary is hot?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live profiler attach.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-801/` and `instructor/rubrics/INCIDENT-801.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

Process CPU is a first-class production signal and still only a symptom. A dump turns “busy” into call sites. Stabilization (who you take out of rotation) is a different sentence from remediation (what you change so the next canary cannot burn a core on every POST).

---

## Portfolio deliverable

Attach the completed INC-JVM-801 worksheet to your notes if this is the Module 8 incident you will write up. The Module 8 portfolio artifact is [student/worksheets/PF-jvm-rca.md](../../student/worksheets/PF-jvm-rca.md): you pick **one** of INCIDENT-801 through INCIDENT-806 and write the scored RCA there.
