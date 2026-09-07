# INC-PROD-1301 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Throughput collapse and P99 spike  
**Service / region:** `payment-service` / `us-west-2`  
**Your name / cohort:**  
**Time started:** 2026-09-07  
**Time submitted:** 2026-09-07

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: After Jordan’s 3.9.0 roll (BAYPAY-13011, 18:08 UTC), `POST /api/v1/payments` still returns **201** — 5xx stayed ~0.05 RPS — but completions fell **182 → 22 RPS** and P99 **118 ms → ~4.8 s**. Hikari pending stayed **0** (14/50 active); servlet threads jumped **18 → 187 / 200**. This is not a Postgres writer stall and not a 5xx page. Something on 3.9.0 is holding request threads (extra per-request work, scrape/metrics, or heap/CPU) so Harbor Market sees late 201s. Avery `c1300a11-…-111300` completed in **5.14 s**. Next: scrape + JVM numbers — duration, series count, heap/CPU — before a bounce or a “bad deploy” close.

Gate 2: Scrape duration **0.187 s → 10.00 s timeout**; series **12 440 → 2 611 088**. `/actuator/prometheus` itself is P99 **4.6 s** and request threads are queued. Heap/CPU are up (1.71 G, CPU 0.68) but G1 pause P99 is **41 ms** — not INCIDENT-805’s 420/640 ms, no OOME, old-gen flat. 3.9.0 exploded the metric series so scrape cannot finish in 10 s; that work starves payment threads. “Bad deploy” is still too weak until I name what 3.9.0 registered.

Gate 3: **Cardinality on `payment.create`.** Commit `9f13a0c1` (BAYPAY-13011) kept `uri`/`method`/`outcome`/`status` and added **`customerId`**, **`accountId`**, and **`Idempotency-Key`**. Those are unique per merchant / per create. Series grew ~12k → ~2.6M; scrape hit the **10 s** timeout; servlet threads sat on the scrape handler. `http_server_requests_*` stayed coarse. Avery still belongs in logs + `traceparent`, not on a timer tag. Sam asked on the PR; Jordan shipped anyway.

## Supporting evidence

Gate 1 — `evidence/dashboards-red.txt` (window 17:50–18:25 UTC):
- Rate: 18:05 **182 RPS** (3.8.4) → 18:10 **171** (3.9.0 in) → 18:16 **61** → 18:22 **22** (pager). Still completing, not silent.
- P99: 18:05 **118 ms** → 18:10 **340 ms** → 18:16 **2.1 s** → 18:22 **4.82 s** (SLO P99 < 400 ms missed).
- 5xx: 18:05 ~0.03 RPS → 18:22 ~0.07. “5xx did not step with the throughput drop.”
- USE 18:22: heap **1.69 G / 2.00 G** (was 1.08 G); Hikari **14/50, pending 0**; servlet **187/200**.
- Avery payment `c1300a11-0000-4000-8000-111111111300`: COMPLETED, HTTP 201 at 18:23:11Z, **5.14 s**. Same Idempotency-Key, no duplicate.

Gate 2 — `evidence/scrape-and-jvm.txt` (18:10 and 18:22 UTC):
- scrape_duration_seconds: 18:05 **0.187** success / 12 440 samples → 18:10 **1.64** / 411 208 → 18:16 **4.21** / 1 844 022 → 18:21 **7.88** / 2 481 090 → 18:22 **10.00 timeout** (scrape_timeout_seconds = 10). Head series **2 611 088**.
- JVM 18:22: heap **1.71 G / 2.00 G**, CPU **0.68**, live threads **214**, gc_pause_p99 **41 ms** (18:05: 14 ms). No OOME. Old-gen 412 M → 448 M.
- Actuator scrape handler P99 **22 ms → 4.6 s**; servlet **187/200**, request queue **14**.

Gate 3 — `evidence/meter-registration.txt` (ticket BAYPAY-13011, Jordan Voss):
- 3.8.4 (`c8e38404`): `Timer.builder("payment.create")` tags `uri`, `method`, `outcome`, `status` only.
- 3.9.0 (`9f13a0c1`): same plus `.tag("customerId", …)`, `.tag("accountId", …)`, `.tag("Idempotency-Key", idempotencyKey)`.
- Sample line: `payment_create_seconds_count{Idempotency-Key="8f0c1300-demo-key",accountId="…2221",customerId="…1111",…} 1`
- Sam Okada PR: “Do these two extra tags stay unique per merchant? Also the header?” Jordan: “Need them to find Avery's create on the dashboard. Ship 3.9.0.”
- Last healthy image still in ECR: `baypay/payment-service:3.8.4`

Optional contrast (literacy): INCIDENT-805 was DEBUG overlay / allocation with large GC pauses. This file’s G1 P99 is **41 ms**; the scrape series count is what 805 would not show.

## Next investigation

Gates used in order. If I still wanted an omitted kind: a **thread dump** would likely show scrape/actuator threads + Tomcat workers in `prometheus` text format — I would not invent stack frames. Heap dump remains out of scope (heap used is already a number). Database metrics omitted on purpose (Hikari pending = 0). Do not create AMP.

## Stabilization action

Roll `pay-prod-west` back to last healthy image **`baypay/payment-service:3.8.4`** (or strip the three tags and stay on 3.9.0 only if that ship is faster *and* still named on the board). Jordan: no second tag. Sam: **do not bounce `db-east` or `dmgr-east`**. Do not scale to 20 tasks from a laptop. Do not heap-dump or “tune GC” on 3.9.0. Do not attach a profiler to a paid JVM.

## Remediation

Do **not** register `customerId`, `accountId`, `Idempotency-Key`, or raw `paymentId` on a Micrometer timer. Avery’s create is JSON logs + `traceparent`. Meter review: cardinality check before merge; Sam’s question is a blocker, not a comment. Page on scrape duration / series budget (or SLO burn + Hikari pending); a scrape-gap ticket is not enough if series can hit 2M in 15 minutes. BUILD-1300 home board already refused those labels.

## Communication update

SEV-2 `payment-service` `us-west-2`: Harbor Market late 201s, not 5xx. Completions ~182 → ~22 RPS; P99 ~118 ms → ~4.8 s after 3.9.0 (BAYPAY-13011). Hikari pending stayed 0 — we are not bouncing Postgres or `dmgr-east`. Scrape duration 0.19 s → 10 s timeout; series ~12k → ~2.6M. Stabilizing on image **3.8.4**. Avery payment `c1300a11-…-111300` completed (201, 5.14 s); no duplicate capture. Follow-up: remove unique merchant/header tags from `payment.create`.
