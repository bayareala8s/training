# INCIDENT-803 — Deadlock

**Type:** INCIDENT  
**Module:** 08 — JVM Troubleshooting  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/jvm/INC-JVM-803](../../incidents/jvm/INC-JVM-803/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

02:11 Pacific on a synthetic prod-east night in October 2026. Harbor Market reports that `POST /api/v1/payments` hangs after the nightly window starts. Completions on `pay-prod-east-2` drop toward zero. Actuator still returns up. CPU is low. `pay-prod-east-1` continues to complete Avery Chen’s creates. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry is another HTTP thread that will not finish if the canary JVM has stopped making progress on money locks. Finance does not care that the process table is green. They care that authorizations stop for anyone the load balancer still sends to east-2.

This pack is **`payment-service` on `pay-prod-east-2`**, not the Module 2 canary worker estate (`INC-JVM-202`). Do not paste that worksheet here. Do not bounce Postgres. Do not bounce `dmgr-east`. Runtime names: [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).

---

## Learning objectives

- Follow gated evidence: dashboard first, then logs, then the thread dump.
- Treat **completions at zero and CPU idle** as a blocking story you still have to quote, not as a finished deadlock label.
- Separate a Java-level circular wait from “threads are waiting on the database.”
- Write stabilization that restores create capacity without recycling the whole region.
- Produce a comms update that does not invent JDBC or GC as the cause.

---

## Architecture

```text
Merchants / Avery Chen
  → load balancer
       → pay-prod-east-1   payment-service 3.8.0   (stable, still completing)
       → pay-prod-east-2   payment-service canary  (first place this page lands)
            HTTP create path
            scheduled jobs in the same JVM (see timeline)
            → baypay DB
```

One process composition root. You do not need a live `jstack`. The contracts are HTTP threads, any job threads the dump names, and monitors those stacks own. Module 5 WAS cells are a different estate.

---

## Prerequisites

- L-8.1 (thread-dump analysis) completed, or read in the same sitting.
- You may have done INCIDENT-202 in Module 2. That is a **different pack** (payment vs refund workers on a teaching canary). Write this page from **this** dump.
- Locked runtime names from [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).
- Incident worksheet: [student-worksheet.md](../../incidents/jvm/INC-JVM-803/student-worksheet.md).
- Optional PAKS: `docs/27-production-failures/failure-analysis-methodology.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/jvm/INC-JVM-803/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset** of the evidence kinds the course catalog lists. The pack README documents what shipped and what was omitted. Do not invent a heap histogram or a plugin-cfg.

Do not open `solutions/INCIDENT-803/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note when creates dropped relative to any nightly job, and which instance paged.
2. **Gate 1:** open `evidence/dashboard.md` only. Record completions, CPU, pool gauges, and whether `pay-prod-east-1` shares the hang. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote job and create lines; do not close the RCA on the word “deadlock.”
4. **Gate 3:** open `evidence/thread-dump.txt` only if it answers a question you already wrote about who owns which monitor.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Jordan Voss).
6. Optional: one sentence contrasting this estate with INC-JVM-202 (different threads, different deploy) — literacy only; do not import that RCA.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “it’s a deadlock” with no quoted stacks scores low on Diagnostic method (see rubric). Skipping to the dump before a written question also scores low.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- CPU is low and merchants still hang: that is data. Write the contradiction.
- You want a heap histogram: it is not in this pack. Say so.
- You are about to bounce Postgres or `dmgr-east`: re-read RUNTIME.md.
- Dashboard Hikari is not 50/50: do not force INC-EE-402’s story onto this page.
- The dump has a “Found one Java-level deadlock” block: quote the **threads and monitors**; do not stop at the heading.
- You remembered Module 2 and wrote “payment worker vs refund worker”: check whether those thread names exist here.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which two call sites disagree.

---

## Interview questions

1. Why is “the service is down” a weak first sentence when `pay-prod-east-1` still posts Avery Chen’s payment?
2. What is the difference between `BLOCKED (on object monitor)` and a thread waiting on a socket?
3. Why can liveness stay UP while every create on that JVM is stuck?
4. When do you kill a scheduled job versus bounce the whole canary JVM?
5. Why is a bounce stabilization and not remediation if the same two orders still exist tomorrow night?

---

## Architecture/trade-off questions

1. One global lock order versus no nested locks (database transactions only) — what does each choice cost a nightly reversal?
2. Should a nightly job share the API JVM at all?
3. If HTTP create takes account then ledger, what must every other module do?
4. Why is “add more Tomcat threads” a weak response to a circular wait?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live `jstack` attach.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-803/` and `instructor/rubrics/INCIDENT-803.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

Idle CPU plus zero completions is a blocking smell, not a diagnosis. A dump names owners and waiters. Stabilization (stop the job, bounce that JVM, drain the canary) is a different sentence from remediation (one lock order, or no nested locks). A title that says “deadlock” does not replace quoted monitors.

---

## Portfolio deliverable

Attach the completed INC-JVM-803 worksheet to your notes if this is the Module 8 incident you will write up. The Module 8 portfolio artifact is [student/worksheets/PF-jvm-rca.md](../../student/worksheets/PF-jvm-rca.md): you pick **one** of INCIDENT-801 through INCIDENT-806 and write the scored RCA there.
