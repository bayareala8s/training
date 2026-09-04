# Rubric — BUILD-302 Refund API

Score each dimension 0–100, then apply the weight. An over-refund that returns `201` is not a high Technical score even if replay works.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `RefundApiIT` green; remaining-amount `422`; full refund → `REVERSED`; replay `200` | Partial + replay; missing reverse or over-refund | Over-refund `201` or no key |
| Diagnostic method | 20% | Isolated sum versus state transition from failing assertions | One large rewrite after the IT failed | Guessed HTTP codes |
| Production awareness | 15% | `REFUND_CREATE` operation; ledger refund row; event is in-process | Resource works; shared payment key store | Refund as a payment field hack |
| Trade-off analysis | 15% | Discusses own resource, `422` vs `409`, when to leave the HTTP transaction | Preference with little why | No trade-off |
| Security / reliability | 10% | No refund of `DECLINED`/`FAILED`; no double-credit | Remaining check only | Refunds anything |
| Communication | 10% | Excerpt states remaining rule and `REVERSED` condition | Incomplete | Empty |
| Efficiency | 5% | Reused payment create on BayPay | Finished; extra unused API | Second HTTP app |

**Pass guideline:** weighted score ≥ 70 and over-refund is `422`.
