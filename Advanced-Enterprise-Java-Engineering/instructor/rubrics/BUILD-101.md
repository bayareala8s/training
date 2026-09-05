# Rubric — BUILD-101 Build BayPay transaction domain model

Score each dimension 0–100, then apply the weight. A lucky paste of `shared` without tests is not a high Diagnostic or Communication score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `Money`, statuses, and transitions match the reference table; illegal edges throw | Most rules present; one missing terminal or `equals` uses `BigDecimal.equals` | Setters, string statuses, or `double` money |
| Diagnostic method | 20% | Tests name zero, `JPY`, mismatch, `RECEIVED → COMPLETED`, declined terminal | Happy-path tests only plus one negative | No tests / “it compiled” |
| Production awareness | 15% | Mentions idempotency key on `Payment`, `LedgerTransaction` naming, Avery demo ids | Domain works; no production names | Treats the model as a DTO dump |
| Trade-off analysis | 15% | Discusses immutable money vs mutable status / JPA, and names a SOLID seam (`PaymentAuthorizer`) versus a needless `MoneyReader` | States a preference with little why | No trade-off |
| Security / reliability | 10% | Fail-closed constructors; no public `setStatus` | Validates amount only | Silent illegal transition |
| Communication | 10% | Worksheet is readable in five minutes | Incomplete excerpt | Empty worksheet |
| Efficiency | 5% | `EnumSet` / typed sets; no wasted raw collections | Fine for N=1 | Raw lists of status strings |

**Pass guideline:** weighted score ≥ 70 and no public `setStatus`.
