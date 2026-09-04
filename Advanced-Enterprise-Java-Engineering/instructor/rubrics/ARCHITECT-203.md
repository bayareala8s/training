# Rubric — ARCHITECT-203 Safe concurrent payment processing

**Lab type:** ARCHITECT  
**Max:** 100  
**Standard weights** from COURSE_MASTER_SPEC §24.

The details block in the student lab is a *post-attempt* hint. Using it as the first draft of `DESIGN.md` caps Diagnostic method and Trade-off.

| Dimension | Weight | 5 (exceeds) | 3 (meets) | 1 (below) | 0 |
|---|---|---|---|---|---|
| Technical accuracy | 25 | Harness Case A+B pass three times; verbs (`putIfAbsent`, `merge`) or an equivalent exclusive section are real | Passes once; design matches code | Design says concurrent map; code still `get`/`put` | Does not compile or fails both cases |
| Diagnostic method | 20 | Design responds to BREAKFIX-201 and INCIDENT-202 with evidence-backed constraints | Mentions both incidents | Generic “thread-safe” essay | Copied details block only |
| Production awareness | 15 | Bounds, reject policy, multi-instance unique key, shutdown | Bounds or unique key, not both | Unbounded cached pool | N/A |
| Trade-off analysis | 15 | One-sentence lock policy; compares one lock vs map verbs vs two ordered locks | Policy present | “Synchronize everything” | Missing |
| Security / reliability | 10 | No discard of money work; admission control; integrity of at-most-once | Mentions no silent drop | Ignores reject/drop | N/A |
| Communication | 10 | `DESIGN.md` a peer can review in ten minutes | Readable but incomplete | Bullet salad | Missing |
| Efficiency | 5 | Small slice, no extra services | Completes in session | Builds an unused framework | N/A |

## Diagnostic method — hard rule

Do **not** award 16–20 on Diagnostic method if `DESIGN.md` is a restatement of the lab details block with no independent lock sentence or no link to the two incidents the student actually worked.

## Anchor answers (instructor)

See `solutions/ARCHITECT-203/README.md`.
