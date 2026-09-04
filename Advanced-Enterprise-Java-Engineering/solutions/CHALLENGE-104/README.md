# CHALLENGE-104 — Instructor solution

**Do not reveal this algorithm in the student channel.**

## What the starter does

For each inbound payment (N):

1. Scan the entire ledger (M, and M grows as rows are appended).
2. Scan the list of already-posted ids in this batch.
3. Scan the entire balance list (A) to find the account.
4. Allocate new `String` and `Double` objects on every copy and every post.

That is O(N × (M + N + A)) plus heavy boxing. It is correct enough for the checksum and unusable at 50_000 rows.

`double` addition is used as the working amount. The checksum rounds, so integer-valued fixtures hide drift. Still treat `Double` balances as a finance defect.

## Optimized approach

See `FasterPostingLoop.java`.

1. Build `HashSet<String> seenPaymentIds` from existing ledger ids (O(M)).
2. Build `HashMap<String, Long> centsByAccount` from starting balances (O(A)).
3. Walk inbound once (O(N)):
   - `seenPaymentIds.add(paymentId)` is false → already posted, skip.
   - missing account → do not keep the id in `seen` (matches starter: unknown account is not recorded as posted).
   - else add long cents and record the posted id.
4. Emit balances in the original account order so the checksum matches.

Expected complexity O(N + M + A). No nested scans. Cents stay `long`.

## How to grade

- Same checksum and posted count on `SEED = 20260903` for N = 8_000 (default `main`).
- Wall clock should drop by an order of magnitude on the same laptop; do not grade absolute milliseconds.
- A student who micro-tunes `ArrayList` capacity but keeps the nested loops fails the Technical and Efficiency dimensions.
- Mention of “move this to SQL at some N” is Trade-off credit, not a substitute for the index.

## Verify locally

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
OUT=/tmp/aeje-challenge-104
mkdir -p "$OUT"
javac --release 21 -d "$OUT" \
  labs/CHALLENGE-104/starter/NaivePostingLoop.java \
  solutions/CHALLENGE-104/FasterPostingLoop.java
java -cp "$OUT" com.baypay.labs.challenge104.NaivePostingLoop 4000
java -cp "$OUT" com.baypay.labs.challenge104.FasterPostingLoop 4000
```

Checksums must match; elapsed ms must not.
