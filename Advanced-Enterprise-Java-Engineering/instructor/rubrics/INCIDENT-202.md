# Rubric — INCIDENT-202 Deadlocked Payment Workers

**Lab type:** INCIDENT  
**Max:** 100  
**Standard weights** from COURSE_MASTER_SPEC §24.

The lab title names a symptom class. Guessing “deadlock” or “lock order” from the title, without a pre-dump hypothesis and dump quotes, must **not** max Diagnostic method.

| Dimension | Weight | 5 (exceeds) | 3 (meets) | 1 (below) | 0 |
|---|---|---|---|---|---|
| Technical accuracy | 25 | Names both threads, both monitors (`accountLock` / `ledgerLock`), both orders; policy is one lock or a single documented order or tryLock+retry | Identifies circular wait and a workable policy | “They are blocked” without monitors | Wrong cause (GC, JDBC) as final RCA |
| Diagnostic method | 20 | v1 before dump; order timeline → dashboard → logs → dump; dump quotes; updates v2 | Dump used well but v1 missing or late | Dump-only or title-only | Opens `solutions/` first |
| Production awareness | 15 | Drain/bounce after dump; health ≠ completions; JDBC 0 used to rule out DB | Bounce plus “fix the code later” | Bounce as the only close-out | N/A |
| Trade-off analysis | 15 | One lock vs ordered two locks vs tryLock; names the cost of each | One policy with one cost | Policy with no cost | N/A |
| Security / reliability | 10 | Availability; readiness vs liveness; no over-claim to merchants | Mentions hung refunds/checkouts | Ignores customer hang | N/A |
| Communication | 10 | Know / don’t know / next update; does not invent “DB down” | Usable bridge update | Blames a dependency the dashboard contradicts | Missing |
| Efficiency | 5 | Stops when dump confirms; no extra invented evidence | Completes in session | Rereads dump for an hour without a policy | N/A |

## Diagnostic method — hard rule

Do **not** award 16–20 on Diagnostic method if any of these are true:

- Hypothesis v1 is missing or timestamped after the dump.
- No quoted stacks / monitor addresses / lock names from `thread-dump.txt`.
- Student writes the instructor phrase “lock-order inversion” with no evidence table.
- Solution file used before the worksheet comms box.

Technical accuracy may still be high if the final policy is correct.

## Anchor answers (instructor)

See `solutions/INCIDENT-202/README.md`. Payment: account then ledger. Refund: ledger then account. Remediate with one lock or one order.
