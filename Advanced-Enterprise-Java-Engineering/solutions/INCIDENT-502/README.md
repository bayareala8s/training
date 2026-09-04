# INCIDENT-502 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

`Pay2` and `Pay3` stay **STARTED**. IHS plugin health is **TCP-only**, so they remain in rotation on `ihs-east` even though they cannot finish `/payment`. A brief DB network blip (21:08 UTC, `was-pay-2` ↔ `db-east`) left **stale connections** in `jdbc/baypay` on those two JVMs. Web-container threads hang on the dead sockets or block in `createOrWaitForConnection`; thread pools exhaust (100/100). `Pay1` on `node-pay-1` never saw the blip and still serves Avery Chen.

The plugin reports Connectable=yes because a TCP accept is not a working `payment.ear`. Hung-thread warnings (`WSVR0605W`) are candidates that the stacks then support: JDBC receive / `getConnection` on `PaymentBean.create`.

## Stabilization

1. Remove `Pay2` and `Pay3` from the plugin (or mark them down) so `ihs-east` sends `/payment` only to `Pay1`.
2. Recycle **those two JVMs** after capturing SystemOut/FFDC if you still can — do not bounce `Pay1`, `dmgr-east`, or `db-east`.
3. Enable connection validation on `jdbc/baypay` (`preTestSQLString` / test-on-checkout) before they rejoin, or accept that the next blip will refill stale handles.
4. Do **not** raise web-container or pool max as the first move.
5. Do not wait for hung-thread interrupt to “fix” money threads.

`Pay2` and `Pay3` share a host; draining both is a large capacity cut but it is the correct isolation. `Pay1` already proved it can post.

## Remediation

- Change plugin health from TCP connect to an **HTTP** check that exercises application readiness (a cheap `/payment` health URI that touches the pool or fails closed).
- Adopt a stuck-thread / hung-thread **policy**: log and alert, threshold above a worst legitimate payment, do not interrupt posting by default.
- Validate connections after network errors; set `maxLifetime` / aged timeout so a blip cannot pin 50 dead handles.
- Keep batch/reporting off this pool (INCIDENT-503 class). Document the bounce card on the ARCHITECT-501 page.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | Pay1 201s and 210 ms p99; Pay2/Pay3 STARTED, 100/100 threads, jdbc 50/50, IHS still sending equal traffic; DB CPU 21%, blip already cleared |
| Logs | 14:08 SQLRecoverableException / connection reset on Pay2/Pay3; later J2CA0045E waiters; WSVR0605W stacks on JDBC and `FreePool.createOrWaitForConnection`; Pay1 still 201 |
| Plugin status | All three in PrimaryServers; health probe is TCP to the port; HTTP URI for health is none; Connectable yes while plugin sees 504s |

A worksheet that says only “hung threads” or only “plugin” with no gate order scores poorly on Diagnostic method even if a word matches this RCA.

## Comms (acceptable example)

SEV-2 on `/payment`, `PaymentCluster`. Pay1 still completing creates. Pay2 and Pay3 are STARTED but not finishing requests after a short DB path blip on `node-pay-2`; `ihs-east` is still sending them traffic. We are taking Pay2/Pay3 out of the plugin and recycling those JVMs only. Do not expect dmgr or Postgres work. Next update 20 minutes.
