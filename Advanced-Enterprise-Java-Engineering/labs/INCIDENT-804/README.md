# INCIDENT-804 — Thread-pool exhaustion

**Type:** INCIDENT  
**Module:** 08 — JVM Troubleshooting  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/jvm/INC-JVM-804](../../incidents/jvm/INC-JVM-804/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

11:07 Pacific on a synthetic prod-east morning in October 2026. Harbor Market reports that `POST /api/v1/payments` hangs, then times out, for merchants who land on `pay-prod-east-2`. The pager names Tomcat busy threads at the maximum. Actuator liveness is still up. Database CPU is low. `pay-prod-east-1` is completing. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry is another HTTP worker that will sit in the same wait if the canary’s outbound call never returns. Finance does not care that the servlet container still accepts sockets. They care that authorizations are not completing on the replica the load balancer still likes.

`pay-prod-east-1` remaining healthy is part of the first sentence. Do not bounce Postgres. Do not bounce `dmgr-east`. Do not “fix” this by setting Tomcat max to 2000. Runtime names: [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).

---

## Learning objectives

- Follow gated evidence: dashboard first, then logs, then the thread dump.
- Treat **Tomcat 200/200** as a symptom of where those threads are parked, not as a sizing RCA.
- Separate HTTP-pool exhaustion from Hikari exhaustion (Module 4 already taught the latter).
- Write stabilization that restores capacity without pretending a larger pool is a timeout.
- Produce a comms update that does not invent a database outage the gauges contradict.

---

## Architecture

```text
Merchants / Avery Chen
  → load balancer
       → pay-prod-east-1   payment-service 3.8.0   (stable)
       → pay-prod-east-2   payment-service canary  (first place this page lands)
            Tomcat HTTP workers
            outbound clients named in the pack
            → baypay DB
            → fx-east.baypay.example   (named in RUNTIME.md)
```

One process composition root. You do not need a live Tomcat. The contracts are busy/max workers, Hikari gauges, and dump frames for `WAITING` threads. A downstream hang without a timeout will fill the inbound pool.

---

## Prerequisites

- L-8.1 (thread-dump analysis) and L-8.6 (thread starvation) completed, or read in the same sitting.
- INC-EE-402 (pool exhaustion) is useful contrast: that pack was Hikari 50/50. This pack’s dashboard will tell you whether JDBC is the waiter.
- Locked runtime names from [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).
- Incident worksheet: [student-worksheet.md](../../incidents/jvm/INC-JVM-804/student-worksheet.md).
- Optional PAKS: `docs/27-production-failures/failure-analysis-methodology.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/jvm/INC-JVM-804/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset** of the evidence kinds the course catalog lists. The pack README documents what shipped and what was omitted. Do not invent a heap histogram.

Do not open `solutions/INCIDENT-804/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note which instance paged and whether any downstream is mentioned.
2. **Gate 1:** open `evidence/dashboard.md` only. Record Tomcat busy/max, Hikari, DB CPU, and any dependency latency. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote waiters and timeouts; do not close the RCA on “pool too small.”
4. **Gate 3:** open `evidence/thread-dump.txt` only if it answers a question you already wrote about what the HTTP workers are waiting on.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Jordan Voss).
6. Optional: one sentence on fail-open versus fail-closed for an FX quote on a USD-only Harbor Market checkout — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “thread pool exhausted” with no waiter and no downstream scores low on Diagnostic method (see rubric). Skipping to the dump before a written question also scores low.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Tomcat is 200/200 and Hikari is 8/50: that disagreement is the incident. Table it.
- You want a heap histogram: it is not in this pack. Say so.
- You are about to bounce Postgres or `dmgr-east`: re-read RUNTIME.md.
- You want to set `server.tomcat.threads.max=2000`: write what those extra threads would wait on.
- Many threads are `WAITING` not `RUNNABLE`: quote the park / join / client frame.
- east-1 is healthy: say whether you will fail traffic over or fix the canary’s outbound call.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which client is the waiter.

---

## Interview questions

1. Why is “we need a bigger thread pool” a weak first sentence when Hikari and DB CPU are idle?
2. What is the difference between a busy Tomcat worker and a worker that is making progress?
3. Why can liveness stay UP while every create on that replica is parked?
4. When do you fail open on a quote versus skip the canary entirely?
5. What timeout belongs on the outbound client versus on the inbound HTTP request?

---

## Architecture/trade-off questions

1. Timeouts, bulkhead, and circuit breaker — which one stops 200 workers from joining a pool of 8?
2. Should FX be on the create path for a USD account, or a cached / async step?
3. If the outbound pool is 8 and Tomcat is 200, what is the intended concurrency of quotes?
4. Why is sizing Tomcat to 2000 a reliability smell rather than a capacity plan?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live Tomcat install.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-804/` and `instructor/rubrics/INCIDENT-804.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

An inbound pool at max is often a downstream without a timeout. Hikari can be fine while HTTP workers are all parked. Stabilization (fail open, skip FX, shed the canary) is a different sentence from remediation (timeouts, bulkhead, breaker). Raising Tomcat max is not a strategy.

---

## Portfolio deliverable

Attach the completed INC-JVM-804 worksheet to your notes if this is the Module 8 incident you will write up. The Module 8 portfolio artifact is [student/worksheets/PF-jvm-rca.md](../../student/worksheets/PF-jvm-rca.md): you pick **one** of INCIDENT-801 through INCIDENT-806 and write the scored RCA there.
