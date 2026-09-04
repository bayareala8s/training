# Rubric — BUILD-301 Payment REST API

Score each dimension 0–100, then apply the weight. A lucky single `201` curl without replay, conflict, and decline is not a high Technical or Diagnostic score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `PaymentApiIT` green; `201` / `200` / `409` / `422`+`DECLINED` / `400` / GET `404`; canonical hash | Happy path + replay; missing conflict or decline body | Replay `201` or no key check |
| Diagnostic method | 20% | Used IT status/`$.code`/paymentId to fix the next miss | Flipped statuses until green with little notes | Rewrote the controller after each red bar |
| Production awareness | 15% | Decline persisted; `Location`; correlation echo; OpenAPI path present | API works; no OpenAPI or no `Location` | Demo-only happy path |
| Trade-off analysis | 15% | Defends header key, `required = false`, `422`+body vs ProblemDetail-only | States a preference with little why | No trade-off |
| Security / reliability | 10% | Writes require a key; no second ledger post; `reference` size-capped | Key present; ledger count not checked | Skips key or logs payload secrets |
| Communication | 10% | Portfolio note explains `201` / `200` / `422` in five minutes | Incomplete excerpt | Empty note |
| Efficiency | 5% | Worked in `reference-apps/baypay/` inside 60–90 minutes | Finished; unused second module | Second Spring app |

**Pass guideline:** weighted score ≥ 70 and replay is `200`.
