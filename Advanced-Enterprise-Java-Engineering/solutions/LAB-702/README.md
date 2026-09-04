# LAB-702 — Instructor solution

**Do not reveal this file as a substitute for student timings.**

The starter already implements `retain` vs `die`. The class in this folder is a **reference** with optional third argument `gc` or `money`, plus comments. Students can pass using **only** the starter.

## Retained vs garbage

| Mode | Reachability | Live set | Typical used-heap delta |
|---|---|---|---|
| `retain` | Each `PaymentLike` sits in an `ArrayList` | ~N records + backing array + id strings | Grows with N (often tens of MiB at 250_000) |
| `die` | Local ref dropped; `sinkCents` keeps the loop live | Almost no PaymentLike retained | End-of-run used heap often near the start (GC may have reused Eden) |

`Runtime.totalMemory() - freeMemory()` is sampled twice. It is **not** allocated-bytes. A collection mid-loop can make die’s “after” smaller than “before.” That is not a leak disproof and not a leak.

`dieSinkCents` exists so javac/JIT cannot delete the loop as dead code.

## Why Money-like records still allocate

A `record PaymentLike(String id, long amountCents, String currency)` is still a heap object in the interpreter and usually after C1. Fields:

- `id` — a **new** `String` from `"pay-" + i` every iteration (char/byte array + String).
- `amountCents` — `long` in the record, but the record header still exists when the object is allocated.
- `currency` — interned `"USD"` may be shared; the **record** is not free.

Production `com.baypay.shared.domain.Money` wraps `BigDecimal` + `String`. `BigDecimal.valueOf` / `new BigDecimal` allocates. `Money.plus` returns a **new** Money. Cents-as-`long` in the harness is already cheaper than `BigDecimal` and **still** not “zero allocation” once you have a record + id string.

The reference `money` variant allocates `MoneyLike` (`long` + `String` + `BigDecimal`) and a `PaymentLike` so the extra objects are visible in elapsed time and used-heap under `retain`.

## Escape analysis (do not over-claim)

In `die` mode a `PaymentLike` that does not escape the loop **might** be scalar-replaced after C2: the JIT can keep `amountCents` in a register and never emit `new`.

It does **not** always do that:

- Before warm-up, the interpreter allocates.
- Escape analysis can be disabled or bail out.
- Debug JVMs, uncommon flags, and large methods change the outcome.
- **String concatenation still allocates** even when the record is eliminated.

Do not let a student score 100 on Technical if they wrote “records are stack allocated” as a universal rule.

## How to grade

- Both modes, same N, numbers recorded.
- Write-up names live set vs garbage.
- Escape analysis is a **maybe**.
- `System.gc()` (`gc` extra) is a hint, not a contract — extra credit only.
- Absolute milliseconds do not matter; retain OOM at huge N is a valid observation.

## Verify locally

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
OUT=/tmp/aeje-lab702
mkdir -p "$OUT/starter" "$OUT/sol"
"$JAVA_HOME/bin/javac" --release 21 -d "$OUT/starter" \
  labs/LAB-702/starter/AllocationHarness.java
"$JAVA_HOME/bin/javac" --release 21 -d "$OUT/sol" \
  solutions/LAB-702/AllocationHarness.java
"$JAVA_HOME/bin/java" -cp "$OUT/starter" com.baypay.labs.lab702.AllocationHarness retain 50000
"$JAVA_HOME/bin/java" -cp "$OUT/starter" com.baypay.labs.lab702.AllocationHarness die 50000
"$JAVA_HOME/bin/java" -cp "$OUT/sol" com.baypay.labs.lab702.AllocationHarness retain 50000 money
```
