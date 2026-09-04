# Rubric — CHALLENGE-104 Optimize transaction processing

Do not reveal the index-based algorithm while students are still timing the starter. A lucky faster program with a different checksum fails Technical.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Same checksum and posted count; cents not `double` in the result path | Faster and almost-equal; off-by-one on duplicates | Wrong answers, or still nested scans |
| Diagnostic method | 20% | Names N×M scan, boxing, per-row `new String` before changing code | “It was slow” plus a rewrite | No baseline time |
| Production awareness | 15% | Relates batch backfill to `PaymentPostingService`; warns about shipping naive to EOD | Mentions “batch job” | Treats as a puzzle only |
| Trade-off analysis | 15% | In-memory index vs SQL at some N; concurrency preview | One sentence trade-off | None |
| Security / reliability | 10% | Duplicate payment ids cannot double-post; amounts exact | Duplicates handled, still `double` add | Can double-apply |
| Communication | 10% | Before/after ms, N, checksum recorded | Times without checksum | No numbers |
| Efficiency | 5% | O(N+M+A); no leftover nested scan | Faster but still one inner scan | Capacity tweaks only |

**Pass guideline:** weighted score ≥ 70, checksum matches, and complexity is no longer nested full-list scans.
