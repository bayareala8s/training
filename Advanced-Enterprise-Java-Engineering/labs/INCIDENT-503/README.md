# INCIDENT-503 — JDBC pool exhaustion on ND

**Type:** INCIDENT  
**Module:** 05 — WebSphere Network Deployment  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/production/INC-WAS-503](../../incidents/production/INC-WAS-503/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

10:41 Pacific on a synthetic prod-east morning in September 2026. Creates against `/payment` queue, then fail with connection-wait timeouts. Priya Nair’s first look at `db-east` shows CPU that would not explain a database outage. PMI on at least one payment JVM sits at the locked `jdbc/baypay` ceiling. You are the engineer on call. The incident pack is synthetic BayPay data for `BayPayCell`.

---

## Business context

Avery Chen (`11111111-1111-1111-1111-111111111111`) is one of the customers whose client retries. Each retry asks the same cell-scoped DataSource for another connection. Settlement and reporting teams also have work scheduled against the `baypay` database. Finance will accept a delayed preview. They will not accept a payment API that cannot check out a connection because something else on the node is holding the pool.

`RefundCluster` may be quiet. Do not assume a cell-wide name is innocent just because refund volume is low.

---

## Learning objectives

- Follow gated evidence: dashboard first, then logs, then the PMI pool snapshot.
- Separate pool exhaustion as a **symptom** from the occupant that produced it.
- Read cell-scoped `jdbc/baypay` (`maxConnections = 50`) as a shared scarce resource, not as “the database is 50.”
- Write stabilization that restores payment capacity without raising the pool as the first move.
- Produce a comms update that does not name an ear you have not shown from evidence.

---

## Architecture

```text
ihs-east → PaymentCluster (Pay1 / Pay2 / Pay3)
              → JNDI jdbc/baypay   (cell-scoped historically, max 50)
                 → db-east.baypay.example:5432 / baypay
                    → Reporting (same database — must not share the payment pool)

RefundCluster (Ref1 / Ref2) also knows the name jdbc/baypay.
```

You do not need a live cell. The contracts are JNDI, the WAS JDBC pool, and PMI. Traditional ND is the source estate. Isolated names (`jdbc/baypay-payment`, `jdbc/baypay-refund`) are the Module 6 direction, not a change you make during this page.

---

## Prerequisites

- L-5.3 and L-5.4 completed (JNDI scope, PMI, thread-to-connection ratio).
- Incident worksheet: [student-worksheet.md](../../incidents/production/INC-WAS-503/student-worksheet.md).
- Locked names from [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md).

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/production/INC-WAS-503/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset** of the eleven evidence kinds the course catalog lists. The pack README documents what shipped and what was omitted. Do not invent queue depth or a container cgroup file.

Do not open `solutions/INCIDENT-503/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note who changed what on `node-pay-1` and when the pager fired.
2. **Gate 1:** open `evidence/dashboard.md` only. Record PMI-style pool numbers, which JVM is at the ceiling, and what `db-east` CPU is doing. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote wait-timeout and application names; do not close the RCA on a single class name.
4. **Gate 3:** open `evidence/pmi-pool.md` only if it answers a question you already wrote about *who* holds the 50 connections.
5. Write stabilization, remediation, and a 5-line comms update on the worksheet.
6. Optional: one sentence mapping this PMI row to the Hikari gauges you used in INCIDENT-402 — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “it’s the pool” with no occupant and no gate order scores low on Diagnostic method (see rubric).

---

## Troubleshooting

- You jumped to PMI first: stop, write the question PMI should answer, then open it.
- DB CPU is low and the pool is full: that is data. Do not diagnose “Postgres is down.”
- You want to set `maxConnections` to 200: write why that would or would not help *this* occupant, then pick a stabilization that does not start there.
- You cannot tell cell scope from per-JVM PMI: say so, and use the per-server snapshot you have.
- A thread dump would be nice: it is omitted on purpose. Write what you would have looked for.

---

## Expected outcome

A written diagnosis path an instructor can score. Exhaustion is the symptom you are given; the worksheet must show how you decided what was holding `jdbc/baypay`.

---

## Interview questions

1. Why is “the database is down” a weak first sentence when `db-east` CPU is low and `max_connections` is far from the WAS pool size?
2. What does cell-scoped `jdbc/baypay` let a newly installed ear on `node-pay-1` do that an application-scoped DataSource would have prevented?
3. Why can raising `maxConnections` make the next outage worse for `db-east`?
4. How is PMI 50/50 different from “three members times 50 equals 150 sessions on Postgres”?

---

## Architecture/trade-off questions

1. Should reporting SQL share the payment DataSource on a payment JVM?
2. Stop-the-ear now versus bounce `Pay1`: which restores merchant capacity with less collateral, and what do you lose?
3. Application-scoped pools versus moving reporting off `PaymentCluster` entirely — which do you do first, and which is the durable split?
4. When would you keep a cell-scoped name during a Liberty wave anyway?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live WAS install.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-503/` and `instructor/rubrics/INCIDENT-503.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

A full JDBC pool is a gauge, not a story. On ND the story often includes *who else* learned the JNDI name. Stabilization stops the occupant or isolates the JVM; remediation splits DataSources and keeps reporting off payment JVMs.

---

## Portfolio deliverable

Attach the completed INC-WAS-503 worksheet to your notes. The Module 5 portfolio artifact remains the ARCHITECT-501 cell brief; this incident is evidence you can read PMI without installing ND.
