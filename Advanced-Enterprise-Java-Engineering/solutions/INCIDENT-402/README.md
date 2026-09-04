# INCIDENT-402 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Connections are **not returned** to Hikari on `pay-prod-east-2`. A settlement preview job in the **same JVM** opens JDBC connections and an `EntityManager` without try-with-resources / without closing the manager. Leak-detection logs are **candidates** that the stacks then support: `SettlementPreviewJob.openReportingConnection` and `streamOpenPayments`.

The pool is **50/50 with waiters**. HTTP create threads block in `HikariPool.getConnection` and time out after 2s. The database is not down (CPU 19%, `max_connections` 400, other replicas healthy). One long preview query is a contributor; the unclosed checkouts are why in-use stays at max.

## Stabilization

1. Stop the settlement preview job on `pay-prod-east-2` (disable schedule / kill the executor).
2. Bounce **that replica only** if checkouts do not return within a minute — recovers the 50 connections.
3. Enable or tighten **max checkout** / keep `leak-detection-threshold` on; optionally set Hikari `maxLifetime` already present and add a checkout timeout already at 2s.
4. Do **not** raise `maximum-pool-size` as the first move.
5. Do not bounce Postgres.

## Remediation

- Close connections with try-with-resources; close application-managed `EntityManager`s.
- Move reporting off the payment API JVM and off the payment pool.
- Add pool gauges (`active`, `pending`, `timeout`) to the payment SLO dashboard.
- Add a test or pre-prod check that preview cannot hold a connection across the whole merchant scan.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | 50/50, waiters, other replicas fine, DB CPU low |
| Logs | Acquisition timeout; leak-detection stacks on `SettlementPreviewJob` |
| JVM metrics | HTTP threads blocked on `getConnection`; preview thread in `ResultSet.next` |

A worksheet that says only “leak” with no gate order scores poorly on Diagnostic method even if the word is right.

## Comms (acceptable example)

SEV-2 on payment creates, `pay-prod-east-2` only. Pool exhausted (50/50, waiters). Other replicas serving. We stopped the in-JVM preview job and recycled the replica. Creates should recover on that instance. We will keep reporting off the API pool. Next update 20 minutes.
