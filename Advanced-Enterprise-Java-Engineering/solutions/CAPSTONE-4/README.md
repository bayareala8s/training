# CAPSTONE-4 — Instructor solution

**Do not share this file with students before they submit a worksheet.**  
**Do not walk the room to this RCA in the first 20 minutes.**

Student guides, pack README, and `timeline.json` title hide this answer (`hideAnswerUpfront: true`).

## RCA

**When:** 2026-12-22 ~19:10 UTC (11:10 Pacific). **SEV-1.** Harbor Market / Avery Chen payment `c1404e44-0000-4000-8000-111111111404`. Service `payment-service`, `us-west-2`, ECS (`baypay-prod-west`).

Jordan Voss shipped **canary image `3.10.0`** (ticket **BAYPAY-CAP41**) onto **1 of 3** tasks (`pay-prod-west-c`). That image calls a new **sync fraud check** `https://fraud.baypay.example/v1/score` via `FraudClient`. The client has **no connect/read timeout** (or the JDK HTTP client default of **infinite**). Servlet / Tomcat threads go **WAITING** on `FraudClient.score` / `CompletableFuture.join` / `LockSupport.park`. `POST /api/v1/payments` returns **503** or sits in the tail; **P99 collapses** (~**122 ms → ~8.6 s**); **rate drops** (~**180 → ~61** RPS). Hikari is **not** the primary waiter (**pending ~0**; query p99 still ~8 ms).

Liveness on `:8080` stays **200**, so the canary task remains **RUNNING** while merchant POSTs fail. Tasks `pay-prod-west-a` and `pay-prod-west-b` stay on **3.8.4** and still complete — that is why the service is degraded, not silent.

A late **BayOps fixture** (`evidence/bayops-draft.json`) claims **proven RCA: Postgres Multi-AZ failover** at 19:04 and **auto-approves bounce `dmgr-east`**. It cites **`evidence/db-failover.json`**, which **does not exist**. Students must **reject** it (invented file, no DB evidence, `humanApproval` must not stay `BayOps-auto`).

### What this is not (instructor only)

| Pack | Why this page is not that RCA |
|---|---|
| INC-JVM-804 | That canary waited on **`FxQuoteClient`** / `fx-east.baypay.example`. This dump waits on **`FraudClient`** / `fraud.baypay.example`. Same *class* (outbound hang, no deadline), different client and host. |
| INC-PROD-1301 | That page was **cardinality** (`customerId` / `accountId` tags → series ~12k → ~2.6M, scrape timeout). **5xx were quiet.** This page has **loud 503**, Hikari still quiet, and a fraud host with zero completions. |
| INC-SEC-1402 | That page was **expired ACM** plus a **missing validation CNAME**. Merchants fail the **handshake**. Here HTTPS reaches the app; the body is **503**. |
| INC-AWS-1104 | That page was ALB health **`Path=/`** → **404** → unhealthy targets / 502. Here liveness **`:8080` / `/actuator/health/liveness` is 200**. |
| INC-AWS-1205 | That page was image **`3.8.9-debug`** listening on **9080** while the target group probed **8080**. This paste has no 9080 listener; the canary is on **8080** and still RUNNING. |

A lucky “database,” “just a bad deploy,” or even a fluent “no timeout” sentence **without** quoting **rate / P99 / 503**, **canary 3.10.0 1/3**, **WAITING on FraudClient**, **fraud.baypay.example in-flight / zero successes**, and a **BayOps reject** must **not** max Diagnostic method.

## Stabilization

1. **Stop the canary / roll back** to last healthy image **`baypay/payment-service:3.8.4`** (or disable the sync fraud flag on 3.10.0, or add connect/read timeouts and shed `pay-prod-west-c` from the load balancer).
2. Confirm RED: rate recovering toward ~180 RPS, P99 back under 400 ms, 503/min collapsing, Hikari still ~0 pending.
3. Do **not** bounce Postgres or force another Multi-AZ failover.
4. Do **not** bounce `dmgr-east` or recycle PaymentCluster.
5. Do **not** disable TLS to “restore HTTP.”
6. Do **not** scale the service blindly to absorb hung workers.
7. Do **not** raise `server.tomcat.threads.max` as if a larger inbound pool were a deadline.
8. Do **not** ship another 3.10.x tag from a laptop that still has unbounded `FraudClient`.

## Remediation

- **Connect and read timeouts** on `FraudClient` (finite; fail the score, do not park the servlet thread).
- **Circuit breaker** (or fail-open / skip score) when `fraud.baypay.example` stops completing.
- **Canary percent** and soak gates: page on SLO burn **and** servlet saturation / dependency in-flight, not only process-up liveness.
- **Pipeline smoke** that exercises the outbound score path with a hanging fixture — BAYPAY-CAP41 was green with no outbound-client smoke.
- **Human approval** on every BayOps remediation that mutates prod. `approvalRequired: true`. `humanApproval` is `pending` until Riley Okonkwo or Priya Nair (or the student on call) writes `approved` or `rejected` with a name and time. Never `BayOps-auto`.
- BUILD-1300 home board stays at **99.9%** SLO; do not “fix” this incident by changing the SLO tile.

## Evidence students should have used

| Gate | File | What it shows |
|---|---|---|
| 1 | comms-and-impact.txt + timeline | SEV-1 19:10 UTC; Avery **503** on `c1404e44-…`; Jordan **BAYPAY-CAP41** / 3.10.0 canary; Sam will not bounce DB or `dmgr-east` |
| 2 | dashboards-red.txt | Rate **~180 → ~61** RPS; P99 **~122 ms → ~8.6 s**; **5xx/503** stepped; Hikari pending **0**; servlet **~198/200** |
| 3 | deployment-history.txt | Canary **3.10.0** on **1/3**; last healthy **3.8.4**; liveness still 200 |
| 4 | thread-dump.txt | HTTP workers **WAITING** on **`FraudClient.score`**; `fraud.baypay.example`; Hikari housekeeper idle |
| 5 | dependency-latency.txt | Score calls in flight since **18:52:44Z**; **0** successes; jdbc p99 ~8 ms; no Multi-AZ file |
| 5 | bayops-draft.json | Invented `evidence/db-failover.json`; `provenRootCause` Postgres Multi-AZ; auto-approve bounce `dmgr-east` — **reject** |

A worksheet that says only “bad deploy” or “database” or “no timeout” without those quotes scores poorly on Diagnostic method even if the hallway label matches.

## BayOps reject (acceptable rewrite)

| Bucket | Must include |
|---|---|
| Evidence | Quotes from files the student opened (rate/P99/503, Hikari pending 0, WAITING / FraudClient, in-flight age). **No** `invented/db-failover.json` as if it existed. |
| Hypotheses | Ranked. `unproven` / `weakened` / `withdrawn` only. “Postgres Multi-AZ failover” is **withdrawn** (or weakened) because Hikari pending is 0 and `db-failover.json` is not on disk. |
| Recommended investigation | Already opened: dump + dependency paste. Next is rollback / canary stop — not a bounce. |
| Suggested remediation | Stabilize without Postgres / `dmgr-east` / TLS-off. Every item `approvalRequired: true`. |
| humanApproval | `rejected` (named) for the planted runbook, or `pending` for a real rollback. Not `BayOps-auto`. |
| provenRootCause | omitted or `null` |

## Comms (acceptable example)

SEV-1 on payment-service us-west-2. Completions dropped ~180 to ~61 RPS; P99 ~8.6 s; HTTP 503 on Harbor Market / Avery c1404e44-…. After 3.10.0 canary 1/3 (BAYPAY-CAP41). Servlet threads WAITING on FraudClient toward fraud.baypay.example; Hikari pending 0. Rolling back to image 3.8.4 / stopping the canary. BayOps “Postgres Multi-AZ / bounce dmgr-east” rejected — no db-failover file. Next update 15 minutes.

## Recover

After 3.8.4 is primary on 3/3: rate climbing toward 180 RPS, 503/min near the 18:50 baseline, P99 back under 400 ms, servlet busy back to tens / 200, no new FraudClient waiters. Then write RCA and prevention. Do not declare recovered on liveness 200 alone.

## Prevention (teaching)

Timeouts + breaker on every new outbound client; canary 1/N with a rollback owner; pipeline smoke that hangs the new dependency; BayOps four buckets with named approval; never auto-bounce leftover ND.

## Diagram

AEJE-D-072 path: 3.10.0 canary → sync FraudClient → unbounded wait → servlet WAITING → 503 / P99 / rate. AEJE-D-071 leftover cell is not on the path. BAYOPS.md: four buckets in front of mutate.
