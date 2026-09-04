# INCIDENT-503 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Cell-scoped **`jdbc/baypay`** (`maxConnections = 50`) is shared by `PaymentCluster` and a newly installed **`reporting.ear` on `node-pay-1`** (same JVM as `Pay1`). Settlement preview / reporting holds connections (14 + 9 in the PMI holder trace) and does not close them until the merchant scan finishes. PMI on Pay1 is **50/50** with waiters. `db-east` CPU is **17%** — the database is not down. `Pay2` and `Pay3` still have spare connections because `reporting.ear` was not installed there.

Payment HTTP threads on Pay1 fail with `ConnectionWaitTimeoutException` (`J2CA0045E`). Avery Chen’s retry succeeds on Pay2.

This is the ND form of the INCIDENT-402 smell: reporting inside the payment process, on the payment pool.

## Stabilization

1. **Stop `reporting.ear` on payment nodes** (Pay1). That is the occupant.
2. Recycle **Pay1 only** if checkouts do not return after the ear stops.
3. Leave Pay2/Pay3 and `db-east` alone.
4. Do **not** raise `maxConnections` to “give reporting room” on the payment DataSource.
5. Do not uninstall `payment.ear`.

## Remediation

- Isolate DataSources: payment uses a payment-only bind (Liberty target `jdbc/baypay-payment`); reporting gets its own pool and its own JVM or cluster.
- Move reporting **off payment JVMs**. Do not target `reporting.ear` at `Pay1` again to “use spare heap.”
- Add PMI `PercentUsed` / waiters on the payment SLO dashboard.
- Close preview cursors incrementally (try-with-resources); do not hold 23 connections across an 8k-merchant scan.
- Treat cell-scoped `jdbc/baypay` as a modernization smell on the ARCHITECT-501 page.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | Pay1 p99 9.4s and 50/50; Pay2/Pay3 healthy; `reporting.ear` started on Pay1; DB CPU 17%; one long reporting query |
| Logs | `reporting.ear` started 09:55 and bound `jdbc/baypay`; preview holds a connection; J2CA0045E on `payment.ear`; holder sample names reporting threads |
| PMI | 50/50 on Pay1 only; reporting-preview threads hold 23 connections; validation unset; Morgan can stop the ear |

A worksheet that says only “pool exhausted” with no occupant and no gate order must not max Diagnostic method.

## Comms (acceptable example)

SEV-2 on `/payment` for merchants routed to Pay1. `jdbc/baypay` on that JVM is 50/50 with waiters. Pay2 and Pay3 are serving. Database CPU is low. We are stopping the reporting application on the payment node and will recycle Pay1 if connections do not return. Creates should recover on `was-pay-1`. We will keep reporting off the payment pool. Next update 20 minutes.
