# Rubric — BUILD-102 Implement payment validation

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Throw vs decline split matches production; ceiling is `>`; currencies exact | Rules mostly right; freeze throws or `usd` accepted | Collapses all failures to `false` |
| Diagnostic method | 20% | Tests Avery active, frozen, mismatch, missing, `JPY`, ceiling | Only approve + one decline | No tests |
| Production awareness | 15% | Uses `ErrorCode`-shaped tokens; mentions authorizer vs `Money` | Works in isolation | Invents HTTP status in the domain |
| Trade-off analysis | 15% | Explains why decline is not an exception | Mentions “cleaner if we always throw” only | None |
| Security / reliability | 10% | Ownership after both Optionals; no `orElse(null)`; no secret logs | Ownership present, null still possible | Skips ownership |
| Communication | 10% | Outcome table in notes | Sparse comments | Cannot explain freeze vs missing |
| Efficiency | 5% | Pure, no scratch caches | Harmless extra lists | Instance caches like FIX-103 |

**Pass guideline:** weighted score ≥ 70 and frozen Avery **declines** rather than throwing when ids are valid.
