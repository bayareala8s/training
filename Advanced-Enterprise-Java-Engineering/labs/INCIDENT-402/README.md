# INCIDENT-402 — Connection pool exhaustion

**Type:** INCIDENT  
**Module:** 04 — Jakarta EE and Enterprise Runtime Concepts  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/jvm/INC-EE-402](../../incidents/jvm/INC-EE-402/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

14:05 Pacific on a synthetic prod-east day. Merchants report `POST /api/v1/payments` hanging, then failing. Pager names payment-service. Actuator still returns up. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client retries when a create payment does not return. Each retry is another thread asking the runtime for a database connection. Finance does not care that the JVM process is alive. They care that authorizations are not completing.

---

## Learning objectives

- Follow gated evidence: dashboard first, then logs, then JVM metrics.
- Separate pool exhaustion as a **symptom** from the story that produced it.
- Write stabilization that restores capacity without pretending a bounce is a cure.
- Produce a comms update that does not invent a cause you have not supported.

---

## Architecture

```text
Clients → load balancer → payment-service (Hikari pool, max 50)
                              → PostgreSQL-compatible baypay DB
```

One replica is in the pack (`pay-prod-east-2`). Other replicas exist but are not the first place you look. You do not need WebSphere for this lab; the contracts are `DataSource` and the pool.

---

## Prerequisites

- L-4.3 completed.
- Incident worksheet: [student-worksheet.md](../../incidents/jvm/INC-EE-402/student-worksheet.md).

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/jvm/INC-EE-402/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

Do not open `solutions/INCIDENT-402/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note the gate rules.
2. **Gate 1:** open `evidence/dashboard.md` only. Record a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote evidence; do not promote a log phrase to a closed RCA.
4. **Gate 3:** open `evidence/jvm-metrics.md` only if it answers a question you already wrote.
5. Write stabilization, remediation, and a 5-line comms update on the worksheet.
6. Optional: sketch how the same gauges would appear on a JNDI-bound server DataSource (literacy only).

---

## Validation

A complete worksheet has all six fields: hypothesis, evidence, next investigation, stabilization, remediation, comms. A lucky one-word guess with empty evidence scores low on Diagnostic method (see rubric).

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Dashboard and logs seem to disagree: that is data. Write the contradiction.
- You want a thread dump: it is not in this pack. Say so and work with what you have.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates.

---

## Interview questions

1. Why is “the database is down” a weak first sentence when Actuator is up and DB CPU is low?
2. What is the difference between a leak-detection **candidate** and a proven leak?
3. Why can raising `maximum-pool-size` make the next outage worse?

---

## Architecture/trade-off questions

1. Should reporting SQL share the payment DataSource?
2. Where would you put `leak-detection-threshold` relative to p99 statement time?
3. When would you bounce a replica as stabilization versus waiting for checkouts to return?

---

## Cleanup

None. Do not delete the evidence pack.

---

## Cost estimate

**$0.** Synthetic files only.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-402/` and `instructor/rubrics/INCIDENT-402.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

Pool gauges are first-class production signals. Exhaustion is a symptom. Logs can name candidates. Stabilization and remediation are different sentences.

---

## Portfolio deliverable

Attach the completed INC-EE-402 worksheet to your notes. The Module 4 portfolio artifact remains the ARCHITECT-401 mapping brief; this incident is evidence you can diagnose a runtime, not only map it.
