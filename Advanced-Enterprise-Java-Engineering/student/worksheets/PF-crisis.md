# Portfolio worksheet — Production crisis RCA draft

**Artifact:** CAPSTONE-4 / [capstones/04-production-crisis/README.md](../../capstones/04-production-crisis/README.md) · [INC-CAP-4](../../incidents/production/INC-CAP-4/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-071 (initial WebSphere topology) · AEJE-D-072 (cloud-native target)  
**Ops notes:** [datasets/baypay-ops/OBSERVABILITY.md](../../datasets/baypay-ops/OBSERVABILITY.md)  
**BayOps contract:** [datasets/baypay-ai/BAYOPS.md](../../datasets/baypay-ai/BAYOPS.md)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste instructor solution text. Do not put PAN, CVV, access keys, or `BAYPAY_DB_PASSWORD` values in this file. Live Grafana, Prometheus, AMP, and Bedrock are optional — say whether you used them. The grade path is the gated pack.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | 2026-09-07 |
| Path (`files only` / other) | **files only** — no AMP / Grafana / Bedrock / apply |
| Incident pack used (INC-CAP-4) | **Yes** — gates 1→5. `solutions/CAPSTONE-4/` not opened. |
| Region (must be `us-west-2`) | **`us-west-2`** |
| Demo customer (Avery Chen `11111111-1111-1111-1111-111111111111`, account `…221`) | Avery `…1111` / `…221` |
| Example payment you cited (`c1404e44-0000-4000-8000-111111111404`) | **`c1404e44-0000-4000-8000-111111111404`** |
| Reference commit or branch | Downloads; starter pack left as shipped |

---

## 2. Gate quotes (from *your* INC-CAP-4 worksheet)

Cite AEJE-D-072 as the merchant path. Copy **your** worksheet words. Do not paste `solutions/CAPSTONE-4/`.

| Field | Your answer |
|---|---|
| Gate 1 quote (comms / Harbor Market 503 / payment id) | Avery `c1404e44-…1404` **HTTP 503** at 19:10:56Z, **8.14 s**; retry 503 **16.02 s**. Same Idempotency-Key. Window 19:25 UTC. |
| Gate 2 quote (RED: rate, P99, 5xx/503, Hikari pending) | Rate **181 → 61**. P99 **122 ms → 8.62 s**. 503/min **0 → 51**. Hikari pending **0**. Servlet **198/200**. 5xx **loud** (not 1301’s quiet tile). |
| Gate 3 quote (images / canary fraction / last healthy) | **1/3** on **3.10.0** (`pay-prod-west-c`, 5xx on POST). **2/3** **3.8.4** healthy. Liveness **200** all. Last healthy **3.8.4**. `rollback=false`. |
| Gate 4 quote (thread state and waiter frames) | ~190 exec threads **WAITING** `FraudClient.score` / `CompletableFuture.join`. Host **`fraud.baypay.example`**. Hikari idle. Liveness RUNNABLE. |
| Gate 5 quote (dependency in-flight / successes) | Score in-flight **47**, oldest **18:52:44Z**, **0** successes. No deadline column. Hikari query p99 **8–9 ms**. |
| What you still treated as unproven after gate 3 | *Why* 3.10.0 5xx’s — ticket said “sync score” but I waited for dump + latency before closing. |

---

## 3. Stabilize, remediate, recover

| Field | Your answer |
|---|---|
| Stabilize (what restores the path *now*) | Roll all tasks to last healthy **`baypay/payment-service:3.8.4`**. Drain 3.10.0 canary. |
| What you did **not** bounce or disable | Postgres / `db-east`, `dmgr-east` / PaymentCluster, TLS. No 20-task scale. |
| Remediate (what you will not ship next time) | No unbounded `FraudClient.join`. Deadline on `fraud.baypay.example`. Canary **rollback=true**. Outbound smoke. Named human. |
| Recover check (what tiles must heal before you leave the bridge) | Rate back toward ~180; P99 < 400 ms; 503/min ~0; servlet busy off the wall; canary 0/3. |

Stabilize is **3.8.4 now**. Remediate is the client budget + canary/pipeline so the next “sync score” cannot eat the servlet pool. Recover is watching RED until Harbor Market creates succeed again — not leaving when Actuator is 200. Last healthy image named on the board: **3.8.4**.

---

## 4. BayOps reject (four buckets)

Cite BAYOPS.md. Evaluate `evidence/bayops-draft.json`. Do not accept an uncited proven RCA.

| Fabricated claim | Quote from the draft | Pack quote that contradicts it | Your sentence |
|---|---|---|---|
| Invented file `evidence/db-failover.json` | `"source": "evidence/db-failover.json"` — “Writer endpoint moved. This is the proven root cause.” | Pack inventory / dep-latency: **`db-failover.json` not shipped.** | Missing `source` is a hallucination. |
| Proven RCA: Postgres Multi-AZ failover | `"provenRootCause": "Postgres Multi-AZ writer failover in us-west-2 at 19:04"` | Hikari pending **0**; query p99 **8–9 ms**. | Fluent proven stamp fails BAYOPS.md. |
| Bounce `dmgr-east` | “Bounce dmgr-east and recycle PaymentCluster” | Sam/Riley: leftover ND **not on the merchant path**. | AEJE-D-071 is not tonight’s stabilize. |
| Auto-approved (`BayOps-auto`) | `"status": "approved", "by": "BayOps-auto"` | Riley: evaluate; do not auto-approve. | BayOps-auto is not a human. |

| Field | Your answer |
|---|---|
| Evidence bucket (your rewrite) | RED 503 + canary 1/3 3.10.0 + `FraudClient.score` WAITING + score **0** successes / 47 in-flight since 18:52:44Z. |
| Hypotheses (ids + `unproven` / `weakened` / `withdrawn`) | H1 **withdrawn** (writer failover). H2 **withdrawn** (cell bounce). H3 **unproven→supported by files** (sync score hang) — still not a `status: proven` field. |
| Recommended investigation | Confirm 3.8.4 rate/P99 after drain. Do not invent `db-failover.json`. |
| Suggested remediation (`approvalRequired` must be true) | Restore **3.8.4**; then deadline + rollback=true. `approvalRequired: true`. |
| Your `humanApproval.status` (must be `rejected` for the planted runbook) | **`rejected`** |
| By / at / note | Riley Okonkwo · 2026-12-22T19:19:00Z · `db-failover.json` **not in pack**; Hikari pending 0. |

A row that only says “the AI is wrong” without the missing-file quote and the proven-RCA quote is incomplete.

---

## 5. RCA draft and prevention (your words)

| Field | Your answer |
|---|---|
| RCA draft (files + quotes; no instructor paste) | BAYPAY-CAP41 3.10.0 added **sync** `FraudClient.score` to **`fraud.baypay.example`**. Dump: `join` on ~190 servlet threads. Latency: **0** successes, oldest in-flight **18:52:44Z**. Merchants **503**. 3.8.4 stayed healthy. Not 1301 (5xx loud), not 1104 (`Path=/` — liveness 200), not 1205 (9080). |
| Prevention (canary policy, client budgets, pipeline, approval) | Deadline on the score client. Canary **rollback=true**. Outbound smoke. Named `humanApproval`. No laptop second tag during soak. |
| Why leftover ND (AEJE-D-071) was not a stabilize target | Tonight is **AEJE-D-072** ECS. Cell is source estate. Morgan’s bounce does not unblock `FraudClient`. |

---

## 6. Interview snippet (Staff, 6–8 sentences)

Gates 1→5. Harbor **503** on Avery `c1404e44-…1404` before anyone touched Postgres. RED: rate **181→61**, P99 **8.6 s**, 5xx **loud**, Hikari pending **0** — not a writer outage. Canary **3.10.0** 1/3; last healthy **3.8.4**; liveness still 200. Dump: `FraudClient.score` / `join` on **`fraud.baypay.example`**. Latency: **0** successes, 47 in-flight since 18:52. Stabilize on **3.8.4**. BayOps `db-failover.json` + proven Multi-AZ + `BayOps-auto` **rejected**. After the canary is gone we still owe Harbor Market a deadline on score and `rollback=true` — Actuator 200 is not recover.

---

## Honesty

- [x] I did not open `solutions/CAPSTONE-4/` before attempting the work
- [x] I requested INC-CAP-4 evidence in the documented gate order
- [x] Every metric or incident claim has a source (OBSERVABILITY.md, BAYOPS.md, or a pack file I opened)
- [x] I did not paste an instructor RCA
- [x] I quoted `evidence/db-failover.json` as **missing** and I quoted the planted **proven-RCA** field
- [x] I did not put PAN, an access key, or a live password in this file
- [x] I did not bounce Postgres or `dmgr-east` and I did not disable TLS
- [x] I did not create `db-failover.json` to match the model
- [x] I did not apply AWS, AMP, a paid Grafana, or Bedrock to pass this capstone
- [x] If I invoked extra-credit Bedrock, I say so above and I destroy tagged `us-west-2` leftovers the same day
