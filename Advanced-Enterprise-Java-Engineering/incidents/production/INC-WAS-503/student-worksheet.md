# INC-WAS-503 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** JDBC pool exhaustion on ND  
**Cell / cluster:** `BayPayCell` / `PaymentCluster`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Exhaustion is on **Pay1 only** (`jdbc/baypay` 50/50, 36 waiters, p99 9.4s, 44×5xx). Pay2/Pay3 are fine (~230 ms). `db-east` CPU **17%**, `max_connections` 400 — Postgres is not down. Timeline + console: Jordan installed **`reporting.ear` on Pay1** at 09:55; it binds **cell-scoped** `jdbc/baypay`; settlement preview started 10:20 on that JVM. Slow query still running 11 minutes. Other members do not run `reporting.ear`. First guess: reporting on the payment JVM is occupying the scarce pool so `payment.ear` cannot checkout. Not “the database is 50.” PMI 50 is **this server’s** pool, not `3 × 50` on Postgres (was-pay-1 sessions = 50). Next: logs — which **app** is checking out.

Gate 2: Confirmed occupant **name**, not yet a full holder split. `reporting.ear` started and `bound resource-ref jdbc/baypay to cell DataSource`. Preview: `connectionHeld=true`, `checkoutMs=1391220`, `statementsOpen=14`, “not closing until merchant scan completes.” `payment.ear` then `J2CA0045E` / `ConnectionWaitTimeoutException` (Avery `c503b222-…`). Holders **sample**: `reporting-preview-1 x14`, `reporting-preview-2 x9`, `WebContainer x27`. Pay2 retry of the same key is 201. Cell scope is what let a new ear on `node-pay-1` share the payment pool. Next: PMI — do those 23 reporting + 27 payment threads add to 50, and are closes returning?

Gate 3: Yes. Pay1: PoolSize 50, PercentUsed 100, **CloseCount 0 since 09:55**, WaitingThreadCount 36, last WaitTime 180000. Holders: reporting **23** (14+9), payment WebContainer **27**. 36 threads in `createOrWaitForConnection`. Heap/GC fine. `connLeakReclaim` false. Morgan can **stop `reporting.ear`** without uninstalling payment. Per-server PMI — do not multiply by three.

## Supporting evidence

(File, timestamp, quote. Include Pay1 vs Pay2/Pay3 and any ear names you can support.)

| File | Quote |
|---|---|
| timeline.json 16:55 | Jordan: `reporting.ear` on `node-pay-1` (Pay1 only); binds `jdbc/baypay` (cell-scoped) |
| timeline.json 17:47 | Morgan: Pay1 runs `payment.ear` and `reporting.ear`; both look up `jdbc/baypay` |
| dashboard.md 10:45 | Pay1 p99 9.4s, 44×5xx; Pay2/Pay3 ~230 ms |
| dashboard.md JDBC | Pay1 **50/50** waiters 36; Pay2 11; Pay3 10; Ref1 3 |
| dashboard.md DB | CPU 17%; sessions `was-pay-1` = 50; slow query reporting preview 11 min |
| logs.txt 9:55 | `Application started: reporting.ear` / bound to cell `jdbc/baypay` |
| logs.txt 10:36–10:43 | `connectionHeld=true` / `checkoutMs=1391220` / `not closing connection until merchant scan completes` |
| logs.txt 10:41 | Avery `c503b222-…` `ConnectionWaitTimeoutException` on Pay1 |
| logs.txt 10:44 | holders sample reporting 14+9, WebContainer 27; Pay2 retry **201** |
| pmi-pool.md | CloseCount **0** since 09:55; reporting holds 23; payment 27; waiters 36 |

No javacore in this pack. I would have looked for `ReportingJob` vs `PaymentServlet` in `getConnection`.

## Next investigation

After gate 2: PMI holder table — who owns the 50, and is CloseCount moving? Gate 3 answered. If live: stop `reporting.ear` (Morgan already offered), then re-check waiters. Do not start with `maxConnections=200`.

## Stabilization action

(What restores payment capacity *now*? What do you explicitly not do?)

- **Stop `reporting.ear` on Pay1** (Morgan). That returns reporting’s 23 checkouts without bouncing `payment.ear` or losing Pay1 capacity if threads unwind. If waiters stay, drain Pay1 and recycle **Pay1 only**.
- Keep Pay2/Pay3 in rotation (they already 201 Avery’s retry).
- Do **not** raise `maxConnections` to 200 (Riley: not until we know the occupant). That would push more sessions into `db-east` and hide the shared-name bug.
- Do **not** page/bounce Postgres (Priya: CPU 17%).
- Do **not** stop `RefundCluster` (quiet; not the occupant on Pay1).
- Harbor Market: same Idempotency-Key; `c503b222-…` already succeeded on Pay2.

## Remediation

- Reporting / settlement must **not** share `jdbc/baypay` or live on a payment JVM (same as INC-EE-402 / ARCHITECT-501). Dedicated DataSource or a batch host.
- Application-scoped `jdbc/baypay-payment` vs cell-wide name (Module 6: `jdbc/baypay-payment`, `jdbc/baypay-refund`). Cell scope is what let this morning’s ear steal the pool.
- `try-with-resources` / close the preview cursor; do not hold 14 statements for 23 minutes.
- First durable split: **move reporting off PaymentCluster**. Then split JNDI names. Keep a cell-scoped name during a Liberty wave only as a temporary alias with a written sunset.
- Alert on PercentUsed / WaitingThreadCount per member, not only 5xx.

Hikari analog (INCIDENT-402): `active=50`, `pending>0`, `timeout_total` climbing, DB CPU low — same gauge, WAS names `inUse` / waiters / `J2CA0045E`.

## Communication update

(Five lines max. Audience: merchant success + platform lead. Do not name an occupant you have not shown.)

SEV-2 is **Pay1 only**. Pay2 and Pay3 still complete Harbor Market / Avery creates (retry of `c503b222-…` 201). `db-east` is not down (CPU 17%). Pay1’s `jdbc/baypay` pool is 50/50; a settlement preview in `reporting.ear` (installed on that JVM this morning) is holding connections and not closing them. We are stopping `reporting.ear` on Pay1, not bouncing the database. Next update in 15 minutes when Pay1 waiters are back to zero.
