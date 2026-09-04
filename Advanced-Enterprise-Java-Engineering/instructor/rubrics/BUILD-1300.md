# Rubric — BUILD-1300 BayPay operations dashboard

**Type:** BUILD  
**awsLab:** no  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. Grafana / Prometheus / AMP absence must not fail the lab. A rate-only JSON is not a high Technical score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | RED rate + **5xx** + **P99** for `POST /api/v1/payments`; USE heap + **Hikari** `jdbc/baypay` active/pending + servlet threads; SLO **99.9%** + error-budget / burn | Rate plus one of P99 or SLO; Hikari still missing or 99.99% tile | Starter unchanged (rate only) |
| Diagnostic method | 20% | Listed missing errors, P99, SLO/burn, and Hikari **before** editing | Added panels until the file “looked full” | Opened `solutions/` first |
| Production awareness | 15% | 99.9% not 99.99%; page on burn / saturation not CPU>80%; AEJE-D-061; paper file is enough | Panels present; SLO upgraded or CPU is the page | Invented a live AMP/Grafana grade gate |
| Trade-off analysis | 15% | Histogram vs summary; recording rules vs raw scrape; paper vs AMP; 99.9 vs 99.99 | Preference with little why | No trade-off |
| Security / reliability | 10% | Labels only `uri` / `method` / `outcome` / `status` (optional coarse `exception`); no `customerId`, `accountId`, `Idempotency-Key`, `paymentId`, PAN | Allowed labels; one extra identifier in a comment | Merchant or PAN label in an `expr` |
| Communication | 10% | PF-ops dashboard + SLO + refused-labels sections readable | Incomplete excerpt | Empty worksheet |
| Efficiency | 5% | File checklist; JSON parse optional | Finished in session | Required paid Grafana Cloud or an AWS apply |

A dashboard that is complete except it sets the SLO tile to **99.99%** loses Technical accuracy and Production awareness even if every other panel is present.

A dashboard that adds `customerId` or `accountId` as a series label fails Security / reliability even if RED/USE/SLO are complete.

**Pass guideline:** weighted score ≥ 70, P99 present, Hikari active/pending present, SLO is 99.9% with a burn or budget panel, no merchant identifiers on labels. Live Grafana neither raises nor lowers the score.
