# Portfolio worksheet — Operations dashboard and production RCA draft

**Artifact:** Module 13 / [BUILD-1300](../../labs/BUILD-1300/README.md) · [INCIDENT-1301](../../labs/INCIDENT-1301/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-061 (operations dashboard) · AEJE-D-062 (throughput / P99 page)  
**Ops notes:** [datasets/baypay-ops/OBSERVABILITY.md](../../datasets/baypay-ops/OBSERVABILITY.md)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste instructor solution text. Do not put PAN, CVV, access keys, or `BAYPAY_DB_PASSWORD` values in this file. Live Grafana, Prometheus, and AMP are optional — say whether you used them. The grade path is paper JSON plus the incident pack.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | 2026-09-07 |
| Dashboard work (`files only` / local Grafana import / other) | **files only** — `labs/BUILD-1300/work/dashboard.json` (JSON parse ok). No Grafana/AMP. |
| Incident pack used (INC-PROD-1301) | **Yes** — gates 1→2→3; worksheet filled through remediation. `solutions/INCIDENT-1301/` not opened. |
| Reference commit or branch | Downloads workspace; starter left rate-only |

---

## 2. Dashboard panels (BUILD-1300)

Cite **AEJE-D-061**. List the panels you added or completed. The starter had rate only.

| Field | Your answer |
|---|---|
| Rate panel (`expr` or title) | `sum(rate(http_server_requests_seconds_count{uri="/api/v1/payments",method="POST"}[5m]))` |
| Errors panel (5xx — not ordinary 4xx as burn) | `status=~"5.."` on that URI — not 4xx |
| P99 duration (histogram quantile, not average) | `histogram_quantile(0.99, sum by (le) (rate(http_server_requests_seconds_bucket{…}[5m])))` |
| JVM heap used / max | `jvm_memory_used_bytes{area="heap"}` / `jvm_memory_max_bytes{area="heap"}` |
| Hikari `jdbc/baypay` active **and** pending | `hikaricp_connections_active` + `pending` + `max` `{pool="jdbc/baypay"}` |
| Servlet / Tomcat threads busy / max | `tomcat_threads_busy_threads` / `tomcat_threads_config_max_threads` |
| What the starter was missing | Errors, P99, heap, Hikari, threads, 99.9% SLI, burn (rate only) |

In 4–6 sentences, explain how this home board matches AEJE-D-061 and why rate alone cannot brief Priya Nair.

AEJE-D-061 is RED (rate / 5xx / P99) + USE (heap / Hikari `jdbc/baypay` / servlet threads) + **99.9%** SLI and burn on `POST /api/v1/payments`. Rate alone cannot tell Priya whether Harbor Market is failing (5xx), slow (P99), or just quiet. Hikari **pending** is the saturation that predicts burn; CPU > 80% is a ticket, not the page. Paper JSON is enough — AMP / Grafana Cloud is a bill this lab refuses. A per-`paymentId` label is worse than a missing panel: cardinality and a compliance incident.

---

## 3. SLO and error budget (99.9%)

Cite OBSERVABILITY.md. Do **not** upgrade the target to 99.99% (that is a later architecture lab).

| Field | Your answer |
|---|---|
| SLI definition (your words) | Successful `POST /api/v1/payments` / (successful + **server** failures). Server = 5xx, timeout, or dependency that becomes 5xx. |
| SLO target (must be 99.9%) | **99.9%** monthly. Not 99.99% (ARCHITECT-1401). |
| Window | 30 days rolling (SLO tile). Burn uses short windows. |
| Error-budget size you would quote (~43 minutes / 30d if you use the teaching number) | **~43 minutes** equivalent downtime / 30d at 99.9% |
| Burn panel (fast / slow windows you used) | Fast **1h**, slow **6h**: `(5xx rate / total rate) / 0.001` |
| What you would **page** on versus ticket | **Page:** SLO burn + Hikari pending / thread pool maxed. **Ticket:** scrape down, dashboard errors, CPU > 80%. |

In 4–6 sentences, explain why 4xx stay off default burn and why a 99.99% tile would be the wrong edit on this board.

Most 4xx are **Avery’s client** (validation, frozen account `…222`) — not our error budget. Burning on 400s would page Riley for Harbor Market typos. 429 can be called capacity if the cohort agrees; default is exclude. A 99.99% tile is a **Module 14 architecture** pledge (~4 minutes/month). Putting it on this home board without a design change is lying to Finance. This file may not silently upgrade OBSERVABILITY.md.

---

## 4. Labels you refused

Names you would **not** put on a Micrometer / Prometheus label for `POST /api/v1/payments`. Allowed teaching labels are `uri`, `method`, `outcome`, `status`, and coarse `exception`.

| Label or field | Why you refused it |
|---|---|
| `customerId` (Avery `11111111-1111-1111-1111-111111111111`) | Unique per merchant → unbounded series; PCI-adjacent teaching surface |
| `accountId` (`…2221`) | Same; frozen vs active is a **log** field, not a metric label |
| `Idempotency-Key` | Unique per create attempt — worst cardinality |
| raw `paymentId` (e.g. `c1300a11-0000-4000-8000-111111111300`) | One series per payment forever |
| PAN / full account number | Must never be logged or labeled |
| Other you refused | Average-only latency; 99.99% SLO tile; CPU>80% as the page |

Where does a single merchant create belong instead (logs, traces)? One paragraph.

Avery’s create lives in **JSON logs** (`correlationId`, `paymentId`, `outcome`) and a **W3C `traceparent`** — not on `http_server_requests_*` labels. Allowed labels stay `uri`, `method`, `outcome`, `status`, coarse `exception`. Debug `c1300a11-…-111300` in logs/traces after the board shows burn or P99.

---

## 5. INCIDENT-1301 quotes (from *your* worksheet)

Cite AEJE-D-062. Copy **your** INC-PROD-1301 worksheet words. Do not paste `solutions/INCIDENT-1301/`.

| Field | Your answer |
|---|---|
| Gate 1 quote (RED: rate, P99, 5xx) | Rate **182 → 22 RPS**; P99 **118 ms → 4.82 s**; 5xx stayed ~0.05 RPS. Hikari pending **0**; servlet **187/200**. Avery `c1300a11-…-111300` 201 in **5.14 s**. |
| Gate 2 quote (scrape duration and series count) | scrape_duration **0.187 s → 10.00 s timeout**; series **12 440 → 2 611 088**. G1 P99 **41 ms** (not 805). Actuator scrape handler P99 **4.6 s**. |
| Gate 3 quote (meter tag names you actually opened) | 3.9.0 `payment.create` added **`customerId`**, **`accountId`**, **`Idempotency-Key`**. 3.8.4 had `uri`/`method`/`outcome`/`status` only. |
| Stabilize (last healthy image or tag removal — your words) | Roll `pay-prod-west` to **`baypay/payment-service:3.8.4`**. No second tag from Jordan. |
| Remediate (what you will not register next time) | Never put `customerId` / `accountId` / `Idempotency-Key` / `paymentId` on a timer. Avery is logs + `traceparent`. Cardinality review is a PR blocker. |
| What you did **not** bounce | **`db-east` / Postgres** and **`dmgr-east`**. No 20-task scale, no heap dump, no GC tune on 3.9.0. |

---

## 6. Interview snippet (Staff, 6–8 sentences)

The home board (AEJE-D-061) is RED for `POST /api/v1/payments` (rate, **5xx**, **P99**), USE (heap, Hikari `jdbc/baypay` active/**pending**, Tomcat busy/max), and a **99.9%** 30d SLI plus 1h/6h burn — not Jordan’s rate-only draft, not a 99.99% banner. Avery’s `customerId` stays off labels; one payment is logs + `traceparent`. Page on burn, Hikari pending, and **scrape duration / series budget**; ticket CPU>80% and quiet scrape gaps. Paper JSON is the grade — no AMP bill. INC-PROD-1301 (AEJE-D-062): after 3.9.0, rate **182→22**, P99 **118 ms→4.8 s**, 5xx quiet, Hikari pending **0**. Scrape **0.19 s→10 s timeout**, series **12k→2.6M**, because `payment.create` tagged **`customerId` / `accountId` / `Idempotency-Key`**. Stabilize on **3.8.4**. Do not bounce Postgres or `dmgr-east`. GC P99 stayed **41 ms** — not INCIDENT-805.

---

## Honesty

- [x] I did not open `solutions/BUILD-1300/` or `solutions/INCIDENT-1301/` before attempting the work
- [x] I requested INC-PROD-1301 evidence in the documented gate order
- [x] Every metric or incident claim has a source (OBSERVABILITY.md, my `dashboard.json`, or a pack file)
- [x] I did not paste an instructor RCA
- [x] I did not put PAN, an access key, or a live password in this file
- [x] My SLO tile is 99.9%, not 99.99%
- [x] I did not apply AWS, AMP, or a paid Grafana to pass these labs
- [x] If I stood up a local Grafana, I say so above and I did not scrape prod
