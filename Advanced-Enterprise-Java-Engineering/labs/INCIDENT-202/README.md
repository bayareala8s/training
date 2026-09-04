# INCIDENT-202 — Deadlocked Payment Workers

**Lab type:** INCIDENT  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Case study:** BayPay Financial Services (fictional)  
**Incident pack:** [INC-JVM-202](../../incidents/jvm/INC-JVM-202/README.md)

This incident lab does not include the root cause in this guide. Do not skip to `solutions/`. Request evidence in the order given by the incident pack. A lucky guess will not max **Diagnostic method**.

## Scenario

On 21 August 2026, BayPay’s on-call (Riley Okonkwo) received SEV-2 pages: payment completions dropped toward zero, refund completions dropped toward zero, and the posting queue depth climbed. The `payment-service` process stayed up. `/actuator/health` stayed `UP`. CPU on the canary worker node sat near idle. Harbor Bike Co’s refund for `invoice-8841` hung in the merchant dashboard. New checkouts hung after `AUTHORIZED`.

You are the incident commander for the JVM worker. You will work the timeline, request evidence, stabilize, and propose a remediation. You will not be handed a root-cause sentence in this README.

## Business context

Payment workers post authorized captures to the in-memory / canary ledger. Refund workers apply reversals for the same accounts. Both paths must move money or the merchant support line becomes the monitoring system. BayPay’s Saturday sale leftover traffic plus a refund burst after duplicate-charge complaints (see BREAKFIX-201) hit this canary during a weekday catch-up window.

Customer Avery Chen and account `22222222-2222-2222-2222-222222222221` appear in the logs. All names and ids are synthetic.

## Learning objectives

- Practice gated evidence: timeline first, then dashboards, logs, then the thread dump.
- Write a hypothesis that can be *wrong* and then update it when the dump arrives.
- Separate stabilization (restore completions) from remediation (prevent the next hang).
- Produce a communication update that does not invent a cause.

## Architecture

```text
POST /payments  → payment-worker threads  → shared in-process locks / ledger
POST /refunds   → refund-worker threads   → same process, same heap
Actuator        → separate request threads (health may still succeed)
```

Diagram **AEJE-D-007** (deadlocked payment workers) is the course incident picture. Use it as a map of *components*, not as a statement of the bug.

The production modular monolith posts inside a JPA transaction. This incident is the extracted canary worker that took in-process locks around account and ledger updates.

## Prerequisites

- Lessons L-2.1, L-2.2, and L-2.6.
- BREAKFIX-201 attempted (same weekend, related traffic) is recommended but not required.
- Ability to read a `jstack`-style dump.

No extra process to start. This lab is evidence-driven.

## Environment setup

```bash
cd incidents/jvm/INC-JVM-202
```

Read `README.md` in that folder. Do **not** open every evidence file at once. Follow the request order. Keep [student-worksheet.md](../../incidents/jvm/INC-JVM-202/student-worksheet.md) open in a second editor.

Optional: confirm the reference app still boots so you remember what “healthy actuator” looks like when workers are *not* stuck — `cd reference-apps/baypay && ./mvnw -pl payment-service -am test` — but that app is not the broken canary.

## Challenge/tasks

1. Read the timeline only. Write hypothesis v1 on the worksheet.
2. Request the dashboard. Update the hypothesis or the “next investigation” line.
3. Request the logs. Note timestamps where progress stops.
4. Request the thread dump. Quote the stacks that support or kill hypothesis v1.
5. Decide a **stabilization** action that restores completions without claiming a final RCA in the customer comms.
6. Propose a **remediation** (code or lock policy) in your own words. Do not copy an instructor sentence.
7. Write the comms box: what we know, what we do not know, next update time.
8. Transfer the incident half into [PF-concurrency-rca.md](../../student/worksheets/PF-concurrency-rca.md).

If you think you “already know” from the lab title, you still need dump quotes. The title is a symptom class, not a diagnosis.

## Validation

Your instructor (or self-check against the rubric after the attempt) looks for:

- Evidence requested in order, with timestamps on the worksheet.
- At least one hypothesis that cites a dashboard or log line *before* the dump.
- Dump quotes that name the waiting threads and the monitors they wait on.
- Stabilize ≠ remediate.
- Comms that do not over-claim.

There is no green JUnit bar for this lab. The deliverable is the worksheet and RCA.

## Troubleshooting

| Observation | What to try |
|---|---|
| Health is UP, so “nothing is wrong” | Health is not completions. Use the dashboard. |
| You only read the dump | Go back. Your Diagnostic method score needs the earlier gates. |
| You cannot find a circle | List every `BLOCKED` / `WAITING` thread and who owns the monitor. |
| You want a class name to search | Use the dump. Do not open `solutions/`. |
| Logs just stop | That is a clue about progress, not a cause by itself. |

## Expected outcome

- A completed INC-JVM-202 worksheet.
- A lock *policy* proposal (you choose the words) that would prevent a repeat.
- Portfolio RCA sections for INCIDENT-202 filled.

## Interview questions

1. How do you tell deadlock from a thread pool that is only saturated on a slow JDBC call?
2. What should a readiness probe do that liveness does not?
3. Why is “restart the pod” incomplete as a close-out?

## Architecture/trade-off questions

1. One coarse lock versus several locks with a rule — when is each acceptable for a canary ledger?
2. Should refund and payment share a worker pool or stay isolated? What do you lose either way?
3. Where should this invariant live once BayPay runs two JVM instances?

## Cleanup

No cloud resources. Close the evidence files. Do not commit annotated dumps with customer-like data if you ever replace the synthetic pack with a real one — this pack is already synthetic.

## Cost estimate

**$0.** Markdown and a JDK on disk if you optionally run the reference app.

## Hidden/revealable solution

Do not open the instructor pack until your worksheet has hypothesis, evidence quotes, stabilize, remediate, and comms.

Reference RCA and policy:

- [`solutions/INCIDENT-202/`](../../solutions/INCIDENT-202/README.md)
- [`instructor/rubrics/INCIDENT-202.md`](../../instructor/rubrics/INCIDENT-202.md)

A guess that matches the solution file without dump evidence is not a high Diagnostic method score.

## What you learned

- Idle CPU plus a full queue is a waiting problem until proven otherwise.
- Actuator UP is not a payment SLO.
- Evidence order is part of the craft.
- Remediation is a policy, not only a bounce.

## Portfolio deliverable

Complete the INCIDENT-202 half of [student/worksheets/PF-concurrency-rca.md](../../student/worksheets/PF-concurrency-rca.md).
