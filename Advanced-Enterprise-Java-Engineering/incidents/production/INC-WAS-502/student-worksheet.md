# INC-WAS-502 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Cluster members stop processing  
**Cell / cluster:** `BayPayCell` / `PaymentCluster`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: The cluster is **not** down. `Pay1` still completes 184 × 201 / 5m at 210 ms. `Pay2`/`Pay3` are **STARTED** with `payment.ear` started but almost no completions (2 and 0), p99 >12s, web-container **100/100**, CPU 5–6%, `jdbc/baypay` **50/50** with ~40 waiters. Timeline: 92s packet loss `was-pay-2` ↔ `db-east`; `node-pay-1` stayed clean. `db-east` is up (CPU 21%); 50 sessions from `was-pay-2` idle-in-transaction / awaiting client. IHS still splits traffic (0 connect failures). First guess: after the blip, Pay2 and Pay3 held JDBC/work and stopped finishing `/payment`, while the plugin still thinks they are up because the port answers. STARTED ≠ processing.

Gate 2: Same members, now named. Pay2/Pay3: `SQLRecoverableException` / `Connection reset` / `Socket closed` on `jdbc/baypay` at 14:08. Then `J2CA0045E` wait 180s, `inUse=50, max=50`. Hung-thread **WSVR0605W** is a **candidate**: some stacks still in `PaymentBean.create` on `socketRead` / `prepareStatement` (~600s); others blocked in `FreePool.createOrWaitForConnection`. Pay1 control: 201 for Avery `c502a111-…`. I have no javacore (omitted). Next: why does `ihs-east` still send ~180 req/5m to Pay2/Pay3 if they cannot finish?

Gate 3: Plugin is RoundRobin, all three **PrimaryServers**, **TCP connect** health only, no `/payment` readiness URI. Affinity off. Pay2/Pay3 stay **Connectable / in rotation**; last HTTP from plugin is **504 / 120s** (`ServerIOTimeout` 120). Priya can `nc` 9080/9081. TCP-up is why retries look flaky (same Idempotency-Key → Pay1 201 or Pay2 timeout).

## Supporting evidence

(File, timestamp, quote. Name the member: Pay1 vs Pay2 vs Pay3.)

| File | Quote |
|---|---|
| timeline.json 21:08 | Packet loss `was-pay-2` ↔ `db-east:5432` 92s; `node-pay-1` clean |
| timeline.json 21:17 | Priya: IHS still forwarding to all three; Pay1 still 201 |
| dashboard.md 14:20 | Pay1 184×201 / 210 ms; Pay2 2; Pay3 0; all STARTED |
| dashboard.md 14:22 | Pay2/Pay3 web 100/100, hung 47/51, JDBC 50/50 waiters; Pay1 9/50 |
| dashboard.md DB | `was-pay-2` 50 sessions idle in transaction / awaiting client; writer up |
| dashboard.md IHS | Pay2/Pay3 ~180 req, 71–80 timeouts, **0 connect failures** |
| logs.txt Pay2 14:08 | `J2CA0056I` fatal `Connection reset` on `jdbc/baypay` |
| logs.txt Pay2 14:16 | `J2CA0045E` `Waited 180000 ms` `inUse=50, max=50` |
| logs.txt Pay2 14:18 | `WSVR0605W` 612044 ms; stack `PaymentBean.create` / socket or `createOrWaitForConnection` |
| logs.txt Pay1 14:18 | `POST /payment status=201 paymentId=c502a111-…` |
| plugin-status.md | Health probe = TCP only; Pay2/Pay3 Connectable yes; last HTTP 504 / 120s |

No thread dump / heap / deploy history in this pack.

## Next investigation

After gate 2: open the IHS plugin view — is Pay2/Pay3 still in rotation, and is the probe TCP or an HTTP check that exercises `/payment`? Gate 3 answered that.

If live I would still want a javacore on Pay2 (omitted) to count threads in `socketRead` vs `createOrWaitForConnection`, and `pg_stat_activity` for the 50 `was-pay-2` sessions. I would **not** bounce `db-east` to collect that.

## Stabilization action

(What restores customer capacity *now*? Which members do you touch? What do you explicitly not do?)

- Drain **Pay2 and Pay3 together** from `ihs-east` (same host, same blip, both at 50/50). Leaving one in rotation keeps sending ~1/3 of Avery retries into a 120s 504. Pay1 already serves.
- Recycle Pay2, then Pay3 (or both after drain). Confirm `STARTED` **and** a 201 on `/payment` **and** JDBC waiters 0 before re-add.
- Do **not** bounce `dmgr-east` (Morgan: healthy, no deploy) or `db-east` (CPU 21%, blip already cleared).
- Do **not** raise `maxConnections` on the stuck members as the first move.
- Tell Harbor Market: retry with the **same** Idempotency-Key; Pay1 already 201’d `c502a111-…`.

## Remediation

- Plugin health must be an HTTP check that fails when `/payment` cannot get a connection (readiness), not `nc` to 9080.
- After a reset: `validateNewConnection` / purge policy so stale sockets are not returned to `jdbc/baypay`.
- Hung-thread threshold above a worst legitimate create; **do not interrupt** a money thread (partial commit). Warning ≠ bounce button.
- Web-container max 100 vs pool 50: the extra 50 become waiters and hung warnings (Pay2/Pay3). Size them together.
- Recycling without changing the TCP probe is **stabilization only** — tomorrow’s blip will look the same.

Spring Boot analog: Hikari 50/50 + ALB target healthy on TCP while `/actuator/health/readiness` would have gone DOWN (INCIDENT-402 / BUILD-305).

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)

SEV-2 is **Pay2 and Pay3** on `was-pay-2`, not “PaymentCluster down.” Pay1 still completes Harbor Market / Avery creates (example `c502a111-…` 201). Those two members are STARTED but not finishing `/payment` after a short `was-pay-2`↔`db-east` blip; IHS still sends them traffic because the plugin only checks TCP. We are draining Pay2/Pay3 and recycling those JVMs. Do not bounce the database or the DMGR. Next update in 15 minutes when Pay1-only p99 is back under SLO.
