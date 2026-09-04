# Rubric — BREAKFIX-201 Duplicate Payment Incident

**Lab type:** BREAK/FIX  
**Max:** 100  
**Standard weights** from COURSE_MASTER_SPEC §24.

A student who names the root cause without a harness run, without INC-JVM-201 quotes, or after opening `solutions/` has **not** earned a high Diagnostic method score. Lucky guess ≠ disciplined diagnosis.

| Dimension | Weight | 5 (exceeds) | 3 (meets) | 1 (below) | 0 |
|---|---|---|---|---|---|
| Technical accuracy | 25 | Both cases pass three consecutive runs; journal sum equals balance; no single-thread cheat | Both cases pass at least once; small leftover (e.g. `size()` races) documented | Only one case fixed | No repair or broken compile |
| Diagnostic method | 20 | Timeline → dashboard → logs; hypothesis written before edits; disproof criteria | Evidence used but order skipped once | Jumps to a fix, then backfills quotes | Copies instructor RCA or guesses with no evidence |
| Production awareness | 15 | Stabilize (drain canary) vs remediate (map verbs + unique DB key); CI harness | Names canary vs JPA path | “Add synchronized and ship” only | No production talk |
| Trade-off analysis | 15 | Atomic verbs vs one lock vs DB unique; crash window named | One alternative compared | No alternatives | N/A |
| Security / reliability | 10 | Duplicate debit as integrity; metric so merchants are not first detector | Mentions customer impact | Ignores integrity | N/A |
| Communication | 10 | Worksheet comms: know / don’t know / next update; no invented cause | Clear RCA paragraphs | Vague or blames “the JVM” | Missing |
| Efficiency | 5 | Time-boxed; no extra cloud; cleanup class files | Completes in session | Long wander with no hypothesis | N/A |

## Diagnostic method — hard rule

Do **not** award 16–20 on Diagnostic method if any of these are true:

- Hypothesis is missing or written after the repair.
- INC-JVM-201 evidence order was skipped (logs before timeline with no note).
- Solution/rubric files were used as the first step.
- The student states the three racy operations with no Case A/B numbers and no log quotes.

They may still receive Technical accuracy for a correct `putIfAbsent` / `merge` / concurrent journal.

## Anchor answers (instructor)

See `solutions/BREAKFIX-201/README.md`. Expected repair: `putIfAbsent`, `merge`, `ConcurrentLinkedQueue` (or one exclusive lock around all three). Production containment: unique `idempotency_key`.
