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
| Date | |
| Dashboard work (`files only` / local Grafana import / other) | |
| Incident pack used (INC-PROD-1301) | |
| Reference commit or branch | |

---

## 2. Dashboard panels (BUILD-1300)

Cite **AEJE-D-061**. List the panels you added or completed. The starter had rate only.

| Field | Your answer |
|---|---|
| Rate panel (`expr` or title) | |
| Errors panel (5xx — not ordinary 4xx as burn) | |
| P99 duration (histogram quantile, not average) | |
| JVM heap used / max | |
| Hikari `jdbc/baypay` active **and** pending | |
| Servlet / Tomcat threads busy / max | |
| What the starter was missing | |

In 4–6 sentences, explain how this home board matches AEJE-D-061 and why rate alone cannot brief Priya Nair.

---

## 3. SLO and error budget (99.9%)

Cite OBSERVABILITY.md. Do **not** upgrade the target to 99.99% (that is a later architecture lab).

| Field | Your answer |
|---|---|
| SLI definition (your words) | |
| SLO target (must be 99.9%) | |
| Window | |
| Error-budget size you would quote (~43 minutes / 30d if you use the teaching number) | |
| Burn panel (fast / slow windows you used) | |
| What you would **page** on versus ticket | |

In 4–6 sentences, explain why 4xx stay off default burn and why a 99.99% tile would be the wrong edit on this board.

---

## 4. Labels you refused

Names you would **not** put on a Micrometer / Prometheus label for `POST /api/v1/payments`. Allowed teaching labels are `uri`, `method`, `outcome`, `status`, and coarse `exception`.

| Label or field | Why you refused it |
|---|---|
| `customerId` (Avery `11111111-1111-1111-1111-111111111111`) | |
| `accountId` (`…2221`) | |
| `Idempotency-Key` | |
| raw `paymentId` (e.g. `c1300a11-0000-4000-8000-111111111300`) | |
| PAN / full account number | |
| Other you refused | |

Where does a single merchant create belong instead (logs, traces)? One paragraph.

---

## 5. INCIDENT-1301 quotes (from *your* worksheet)

Cite AEJE-D-062. Copy **your** INC-PROD-1301 worksheet words. Do not paste `solutions/INCIDENT-1301/`.

| Field | Your answer |
|---|---|
| Gate 1 quote (RED: rate, P99, 5xx) | |
| Gate 2 quote (scrape duration and series count) | |
| Gate 3 quote (meter tag names you actually opened) | |
| Stabilize (last healthy image or tag removal — your words) | |
| Remediate (what you will not register next time) | |
| What you did **not** bounce | |

---

## 6. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, Jordan Voss, and Riley Okonkwo, in one sitting, how the paper home board (RED, USE, 99.9% burn) and the gated INC-PROD-1301 path keep Avery Chen’s create visible without putting her identifiers on a time series — and what you do first when throughput and P99 move while 5xx stay quiet.

---

## Honesty

- [ ] I did not open `solutions/BUILD-1300/` or `solutions/INCIDENT-1301/` before attempting the work
- [ ] I requested INC-PROD-1301 evidence in the documented gate order
- [ ] Every metric or incident claim has a source (OBSERVABILITY.md, my `dashboard.json`, or a pack file)
- [ ] I did not paste an instructor RCA
- [ ] I did not put PAN, an access key, or a live password in this file
- [ ] My SLO tile is 99.9%, not 99.99%
- [ ] I did not apply AWS, AMP, or a paid Grafana to pass these labs
- [ ] If I stood up a local Grafana, I say so above and I did not scrape prod
