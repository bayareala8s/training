# INC-CAP-4 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** SEV-1 payment create  
**Your name / cohort:**  
**Time started / submitted:** 2026-09-07

## Current hypothesis

Gate 1: After Jordan’s BAYPAY-CAP41 canary (18:52 UTC), Harbor Market gets **HTTP 503** on `POST /api/v1/payments`. Avery `c1404e44-…1404` waited **8.14 s** then 503; same `Idempotency-Key` retry **16 s / 503**. Last healthy image named: **3.8.4**. This is evening volume, not a ping. Sam: no student RDS; leftover ND out of path. Not a TLS-off or laptop scale. Next: RED — rate, P99, whether 5xx stepped, Hikari pending.

Gate 2: Rate **181 → 61 RPS**. P99 **122 ms → 8.62 s**. **5xx/503 are loud** (~0.9 RPS, 51–53 / min) — not INC-PROD-1301’s quiet-5xx class. Hikari pending **0** (14/50). Servlet **198/200**. Heap 1.28 G / 2.00 G — small step. Not a writer stall. Something after 3.10.0 canary is holding request threads and returning 503. Next: canary board — how many tasks on 3.10.0 vs 3.8.4, target health vs liveness.

Gate 3: Canary is **1 of 3**: `pay-prod-west-c` **3.10.0** RUNNING, “draining / 5xx on POST.” `a`/`b` **3.8.4** healthy. Liveness **200 on all three** — 503 is the **app** path, not probe/`Path=/` theater. Circuit breaker `rollback=false`. Ticket: “**sync score call on create**”; no outbound-client smoke. Last all-healthy revision: **3.8.4** (task def 101). Next: thread dump on the canary — what are servlet threads waiting on? (Not a heap dump.)

Gate 4: Canary dump: ~**190** `http-nio-8080-exec` threads **WAITING** in `FraudClient.score` → `CompletableFuture.join`. Host on frames: **`fraud.baypay.example`**. `fraud-client-*` RUNNABLE in `HttpClientImpl.send` / `doPost`. Hikari housekeeper idle. Liveness thread RUNNABLE. 3.8.4 tasks not dumped. Next: dependency latency — in-flight age and successes on `https://fraud.baypay.example/v1/score`. Then evaluate BayOps; do not obey a proven stamp.

Gate 5: Score calls: **in-flight 47**, oldest since **18:52:44Z** (~25 min), **successes / min = 0**. No client deadline column. 3.8.4 had **no** score timer. Hikari pending **0**, query p99 8–9 ms. ACM/ALB Path=/ / 9080 not this page. BayOps draft cites **`evidence/db-failover.json`** (not shipped), `provenRootCause` Multi-AZ at 19:04, bounce `dmgr-east` + Postgres, **BayOps-auto** approved. **Reject.** Mechanism: 3.10.0 sync `FraudClient.score` with no deadline starved servlet threads → merchant **503**.

## Supporting evidence

Gate 1 — `evidence/comms-and-impact.txt`: Avery 503 at 19:10:56Z duration 8.14 s; retry 503 16.02 s. Window closes 19:25 UTC. Riley: no db-east / dmgr-east / TLS-off / laptop scale.

Gate 2 — `evidence/dashboards-red.txt`: rate 181→61; P99 122 ms→8.62 s; 503/min 0→51; Hikari pending **0**; servlet **198/200**.

Gate 3 — `evidence/deployment-history.txt`: 1/3 on **3.10.0**; last healthy **3.8.4**; liveness 200 all tasks; `rollback=false`; “sync score call on create.”

Gate 4 — `evidence/thread-dump.txt` (19:16:08Z, 3.10.0): `FraudClient.score` / `join`; host **fraud.baypay.example**; ~190 WAITING; Hikari idle.

Gate 5 — `evidence/dependency-latency.txt`: in-flight **47**, oldest **18:52:44Z**, **0** successes. `evidence/bayops-draft.json`: invented `db-failover.json`, proven failover 19:04, auto-approve cell bounce.

## Next investigation

Gates used. If still omitted: heap dump not needed (heap small step). Do not invent `db-failover.json`. Do not attach a profiler to prod.

## Stabilization action

Drain/remove canary **3.10.0**; restore **all three** to last healthy **`baypay/payment-service:3.8.4`**. Jordan: no second tag. Sam: **do not bounce** `db-east`, Postgres, or `dmgr-east`. Do not disable TLS. Do not scale to 20 from a laptop.

## Remediation

`FraudClient`: deadline / cancel; do not unbounded `join` on the servlet thread. Canary policy: **rollback=true**; outbound-client smoke on the score host. Pipeline must fail the soak if score successes stay 0. `humanApproval` on mutates. Do not ship “sync score” without a budget.

## BayOps evaluation

**Reject** the draft. `source: evidence/db-failover.json` is **not shipped**. `provenRootCause`: “Postgres Multi-AZ writer failover in us-west-2 at 19:04” — Hikari pending 0; no RDS event. Bounce `dmgr-east` / PaymentCluster — leftover ND out of path. `BayOps-auto` is not a human.

## Communication update

SEV-1 `payment-service` `us-west-2`: Harbor Market **503** on create (Avery `c1404e44-…1404`, 8.14 s). Rate ~181→61; P99 ~122 ms→8.6 s; 5xx loud. Hikari pending 0 — not bouncing Postgres or `dmgr-east`. Canary **3.10.0** 1/3; last healthy **3.8.4**. Stabilizing by rolling off the canary. Score host `fraud.baypay.example` has 0 completions since 18:52 — follow-up after creates recover.

## RCA draft / prevention

3.10.0 added a **sync** `FraudClient.score` to `https://fraud.baypay.example/v1/score` with no deadline. Calls never completed; servlet threads parked on `join`; ALB/clients saw **503**. 3.8.4 tasks stayed healthy. Prevent: client timeout, canary rollback, outbound smoke, named human on mutates. AEJE-D-071 cell is not tonight’s path.
