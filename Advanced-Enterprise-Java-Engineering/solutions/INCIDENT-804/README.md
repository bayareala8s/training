# INCIDENT-804 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Tomcat HTTP workers on `pay-prod-east-2` are **200/200** and `WAITING` on `FxQuoteClient`. The canary enables `fx-quote-on-create`. `FxQuoteClient` has **pool size 8** and **no connect/read timeout**. `fx-east.baypay.example` hung (no successful quotes; jump-host GET exceeds 30s). Eight client threads sit on the socket; the other HTTP workers block in `FxQuoteClient.acquire` / `join`. Creates hang, then hit the inbound 12s timeout.

Hikari is **8/50**. DB CPU is **15%**. This is not pool-leak INC-EE-402. `pay-prod-east-1` does not call FX on create and stays healthy. Avery Chen’s payment is USD; the quote is a preview, not the authorization.

Raising Tomcat to 2000 would only add more waiters on the same eight hung clients.

## Stabilization

1. Fail-open or **skip FX** on the canary (flag off), **or** shed `pay-prod-east-2` from the load balancer.
2. Optionally bounce the canary after the flag is off so parked workers die.
3. Do **not** set `server.tomcat.threads.max=2000`.
4. Do **not** bounce Postgres.
5. Do not bounce `dmgr-east`.
6. Do not page the database team as the first move.

## Remediation

- Put **connect and read timeouts** on `FxQuoteClient`.
- **Bulkhead** the FX pool so it cannot consume the HTTP pool.
- **Circuit breaker** (or fail-open) when `fx-east` stops succeeding.
- Do not call FX on the USD create path if the quote is decorative.
- Canary gate: Tomcat busy and dependency error rate, not only process up.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | Tomcat 200/200; Hikari 8/50; DB CPU 15%; FX no success samples; east-1 healthy |
| Logs | `poolSize=8` `timeout=none`; quotes in flight for minutes; Hikari idle; Avery 12s timeout |
| Thread dump | HTTP threads `WAITING` in `FxQuoteClient.quote` / `acquire`; fx-client threads on the socket |

A worksheet that says only “thread pool exhaustion” with no waiter and no FX scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on payment creates, `pay-prod-east-2` only. All 200 HTTP workers are busy; the database pool is not. A downstream FX quote on the canary is not returning. We are skipping FX and/or taking the canary out of the load balancer. `pay-prod-east-1` still completing. Next update 20 minutes.
