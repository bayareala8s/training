# INC-EE-402 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Payment create timeouts under load  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Hikari on `pay-prod-east-2` is exhausted (`50/50` active, pending 27→41, timeouts climbing). The writer is not down (CPU 19%, `max_connections` 400, only 50 sessions from this replica). Other replicas are fine (9–14 / 50, p99 ~200 ms). Liveness UP; readiness flickered on `db`. Timeline: settlement preview started on **this** JVM at 20:40. A 48s settlement query is still running. First guess: the batch is holding payment-pool connections so `POST /payments` waits 2s and dies. Not “Postgres is down.”

Gate 2: Same story, now named. Hikari: `Connection is not available, request timed out after 2000ms (total=50, active=50)`. Avery creates fail with `Failed to obtain JDBC Connection`. Leak-detection (20s) points at `SettlementPreviewJob.openReportingConnection:74` and `streamOpenPayments:91` (`EntityManager.createQuery`). Job log: `still running merchantCount=8400 connectionCheckoutMs=164210`. Exhaustion is the **symptom**. The producer is the settlement job sharing the payment DataSource and not returning connections promptly. Leak warning is a **candidate** (held >20s), not yet “never closed.”

Gate 3: Confirmed waiters, not a GC/heap incident. 44 `http-nio-8080-exec-*` threads `BLOCKED` on `HikariPool.getConnection`. `settlement-preview-1` is `RUNNABLE` on `ResultSet.next` / `streamOpenPayments`. Heap 612/1536 MB, GC p99 18 ms, CPU 18%. The job is still using at least one checkout (long cursor), which matches leak-detection without proving a missing `close()`.

## Supporting evidence

(File, timestamp, quote.)

| File | Quote |
|---|---|
| timeline.json 20:40 | Merchant settlement preview job started on pay-prod-east-2 (same JVM as API). |
| dashboard.md 14:05–14:12 | active **50/50**, idle 0, pending **41**, timeout delta 64 / 5m. Other replicas pending 0. |
| dashboard.md 14:12 | DB CPU 19%, sessions from east-2 = 50, `max_connections` 400. Slow query: settlement preview, 48s, still running. |
| dashboard.md notes | Readiness failed 14:07 and 14:11 (`db` timed out). Liveness UP. |
| logs.txt 21:05:11 | `Connection is not available, request timed out after 2000ms (total=50, active=50, idle=0, waiting=29)` |
| logs.txt 21:05:19 | Leak stack: `SettlementPreviewJob.openReportingConnection(SettlementPreviewJob.java:74)` unclosed 21440ms |
| logs.txt 21:08:15 | Second leak: `streamOpenPayments(SettlementPreviewJob.java:91)` via `EntityManager.createQuery` |
| logs.txt 21:07:44 | `settlement preview still running merchantCount=8400 connectionCheckoutMs=164210` |
| jvm-metrics.md 21:14 | 44 HTTP threads blocked on `HikariPool.getConnection`; `settlement-preview-1` RUNNABLE `ResultSet.next` |

No thread dump in this pack (stated).

## Next investigation

(What would you open or measure next, and why?)

After gate 2 I wanted JVM / thread samples: are payment threads waiting on the pool, and is the settlement thread still in SQL? Gate 3 answered that. If this were live I would next: `jstack` to count checkouts owned by `settlement-preview-*`, and `pg_stat_activity` for that replica’s 50 sessions (query text, idle-in-transaction vs active). I would **not** raise `maximum-pool-size` as the first experiment.

## Stabilization action

(What restores customer capacity *now*? What do you explicitly not do?)

- Pull `pay-prod-east-2` from the load balancer (readiness is already failing `db`). Send Harbor Market / Avery traffic to east-1 and east-3.
- Cancel or kill `SettlementPreviewJob` on east-2 so checkouts can return. If the job ignores cancel, bounce **only that replica** after drain.
- Do **not** set `maximum-pool-size` to 200 on the API. That multiplies sessions into a 400-cap Postgres and hides the shared-pool bug.
- Do **not** tell merchants “the database is down.” Actuator liveness is UP; the writer CPU is 19%.

## Remediation

(What remains after the page is quiet?)

- Settlement / reporting must not use the payment Hikari pool or the API JVM. Separate DataSource (and preferably a batch process).
- `try-with-resources` / close the reporting connection and the streaming `EntityManager` query. Paginate 8400 merchants; do not hold one checkout for 164s.
- Keep `leak-detection-threshold` (20s here) **above** payment p99 (~180 ms) and **below** a forgotten batch cursor. A candidate is not a close-out; prove `close()` in code review.
- Readiness may include `db` (BUILD-305). Liveness must not. Alert on `pending` and `timeout_total`, not only 5xx.

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)

SEV-2 is isolated to `pay-prod-east-2`. Creates there wait on the JDBC pool (50/50, 2s timeout); east-1 and east-3 stay ~200 ms. Liveness is UP; we are not calling this a database outage (writer CPU 19%). A settlement preview job on that JVM has been holding payment-pool connections since 20:40 UTC. We are draining east-2 and stopping that job. Next update in 15 minutes with whether Avery/Harbor retries should use the same Idempotency-Key.
