# INCIDENT-1301 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

Deploy **`3.9.0`** (Jordan Voss, ticket **BAYPAY-13011**, commit message `observability: richer payment labels`) registered Micrometer timer tags **`customerId`** and **`accountId`** (and **`Idempotency-Key`**) on `payment.create`. Prometheus **series count** exploded (about **12,440 → 2.6 million**). **Scrape duration** jumped from ~**200 ms** to multi-second and then **timeout** (10 s). Request threads stall on meter updates and on the scrape handler. **Throughput collapses** (~**180 RPS → ~22**) and **P99 spikes** (~**120 ms → ~4.8 s**). **5xx are not** the primary signal.

JVM heap and CPU are up because the process is doing more meter work and holding more series state. This is **not** INC-JVM-805 (DEBUG `toString` / allocation storm / 420 ms G1 pauses). This is **not** a database outage (Hikari pending stayed 0; writer CPU was never in the pack).

A lucky guess of “database,” “GC,” or “just a bad deploy” without quoting **series count**, **scrape duration**, and the **two label names** (`customerId`, `accountId`) must not max Diagnostic method.

## Stabilization

1. **Roll back** to last healthy image **`baypay/payment-service:3.8.4`** (or disable the extra tags on 3.9.0 if a config flag exists — this pack shows a code registration, so image rollback is the clean path).
2. Confirm RED: rate recovering toward ~180 RPS, P99 back under 400 ms, scrape duration back near 200 ms.
3. Do **not** bounce Postgres or `dmgr-east`.
4. Do **not** scale the service to absorb a scrape storm.
5. Do **not** take a heap dump as the first stabilize step.
6. Do **not** “tune G1” as if this were INC-JVM-805.
7. Do **not** ship another 3.9.x tag from a laptop that still has the three tags.

## Remediation

- **Low-cardinality labels only** on Micrometer timers: `uri`, `method`, `outcome`, `status` (optional coarse `exception`). Never `customerId`, `accountId`, `Idempotency-Key`, raw `paymentId`, or PAN.
- Find one payment in **logs / traces** (`correlationId`, `paymentId`), not on a time series.
- **Recording rules** for the home-board PromQL (rate, 5xx, P99) so dashboards do not scrape every raw timer.
- **Scrape budget:** alert when `scrape_duration_seconds` leaves the ~200 ms band or when series count for `job=payment-service` steps by an order of magnitude.
- **Review checklist** on meter-tag PRs: every new `.tag(` / `@Timed` extra tag must be a finite enum. Sam Okada’s PR comment should have been a blocker.
- BUILD-1300 home board stays at **99.9%** SLO; do not “fix” this incident by changing the SLO tile.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| dashboards-red.txt | Rate **~182 → ~22** RPS; P99 **~118 ms → ~4.82 s**; 5xx still ~0.05 RPS; Hikari pending **0**; servlet threads busy |
| scrape-and-jvm.txt | scrape_duration **0.187 s → 4.21 s → 10 s timeout**; series **12440 → 2611088**; heap/CPU up; G1 p99 still tens of ms |
| meter-registration.txt | 3.9.0 adds **`customerId`**, **`accountId`**, **`Idempotency-Key`** on `payment.create`; 3.8.4 had uri/method/outcome/status only |

A worksheet that says only “bad deploy” or “GC” or “database” without quoting **series count / scrape duration / the two label names** scores poorly on Diagnostic method even if the lab title matches.

## Comms (acceptable example)

SEV-2 on payment-service us-west-2. Completions dropped ~180 to ~22 RPS; P99 ~4.8 s; 5xx not the page. After 3.9.0 (BAYPAY-13011). Scrape duration left ~200 ms and series count jumped past two million. Rolling back to image 3.8.4. Not bouncing the database or dmgr-east. Next update 20 minutes.

## Diagram

AEJE-D-062: 3.9.0 meter tags → series growth → scrape stall → threads busy → throughput down / P99 up.
