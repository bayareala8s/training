# BREAKFIX-201 — Duplicate Payment Incident

**Lab type:** BREAK/FIX  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Case study:** BayPay Financial Services (fictional)  
**Incident pack:** [INC-JVM-201](../../incidents/jvm/INC-JVM-201/README.md)

Challenge labs do not include the root cause in this guide. Write a hypothesis before you edit. Instructor materials live under `solutions/BREAKFIX-201/` and `instructor/rubrics/BREAKFIX-201.md` — open them only after you have attempted the lab.

## Scenario

Harbor Bike Co reported two `$84.00` captures for `invoice-8841` during the Saturday flash sale. The checkout client sent one `Idempotency-Key: harbor-8841`. BayPay’s in-memory authorize worker — a teaching slice used by a canary before the JPA path — still posted more than once. A load-test harness against the same worker also shows account totals that do not match the number of distinct keys.

You are the payments engineer on call. The starter class is the canary ledger. Your job is to reproduce the mismatch, diagnose it from evidence and the code, repair the ledger, and write an RCA for the portfolio worksheet.

## Business context

Avery Chen (`11111111-1111-1111-1111-111111111111`) pays from active USD account `22222222-2222-2222-2222-222222222221`. Merchants retry when the mobile client times out. BayPay’s product promise is **at most one ledger post per idempotency key**, and **account totals equal the sum of accepted posts**. A duplicate debit is a customer-trust and integrity incident, even when HTTP returned 201 both times.

This canary does not talk to PostgreSQL. The production modular monolith still needs the unique `idempotency_key` row. This lab is the JVM-side failure that made the canary unsafe to promote.

## Learning objectives

- Reproduce a concurrency failure with a parallel harness, not a single-thread test.
- Separate symptoms (wrong totals, extra journal rows) from a root cause you must discover.
- Repair shared authorize state so Case A and Case B in the starter match expected values on every run.
- Write stabilize vs remediate and a customer-safe communication note.

## Architecture

```text
Checkout retry ─┐
Load harness  ─┼─► UnsafePaymentLedger.authorize ─► balances map
               │                                      journal list
               └─► same idempotency key or many keys    seen-keys map
```

See diagram **AEJE-D-006** (duplicate payment race) when the course diagram pack is available. Treat the starter as the canary worker inside `transaction-worker`, not as the full Spring service.

## Prerequisites

- JDK 21 (`java` and `javac` on `PATH`).
- Lessons L-2.1, L-2.2, and L-2.6.
- Willingness to use the incident pack in order (timeline first).

## Environment setup

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd labs/BREAKFIX-201/starter
javac UnsafePaymentLedger.java
java UnsafePaymentLedger
cd ../..
../reference-apps/baypay/mvnw -pl BREAKFIX-201 test
```

Record Case A and Case B actuals from the starter. Implement `src/main/java/com/baypay/labs/breakfix201/SafePaymentLedger.java`. Then open [INC-JVM-201](../../incidents/jvm/INC-JVM-201/README.md) and request evidence in the listed order. Fill [student-worksheet.md](../../incidents/jvm/INC-JVM-201/student-worksheet.md) as you go.

## Challenge/tasks

1. Run the starter at least three times. Note whether actuals are stable or flicker.
2. Request INC-JVM-201 evidence in order. Log a hypothesis *before* you change code.
3. Identify every shared structure that `authorize` touches and how two threads can interleave.
4. Repair the ledger (copy the starter to a working file in this folder, or edit a local copy). Keep the public `authorize` / `balanceCents` / `journalSize` behavior.
5. Re-run both cases until they match expected values on three consecutive runs.
6. Write the portfolio RCA using [PF-concurrency-rca.md](../../student/worksheets/PF-concurrency-rca.md).

Do not “fix” the harness by running one thread.

## Validation

A passing repair shows, on three consecutive runs:

| Case | Expected |
|---|---|
| A — 1000 distinct keys, amount 100 | balance `100000`, journal size `1000` |
| B — 1000 retries of `harbor-8841` | balance `8400`, journal size `1` |

`journalSumCents()` must equal the account balance in both cases.

Optional: after you are done with the canary, explain in the RCA how `IdempotencyService` plus a unique database key in `reference-apps/baypay` would have contained this in production. You do not need to change the Spring app for this lab.

## Troubleshooting

| Observation | What to try |
|---|---|
| Actuals change every run | The failure is timing-dependent. Keep the 8-thread harness. |
| `ConcurrentModificationException` or missing journal rows | The journal is shared. Read who writes it. |
| Case B looks fine, Case A does not (or the reverse) | You are not done. Both invariants are required. |
| Single-thread run is always green | That does not validate the lab. |
| You want the answer | Stop. Re-read the dump of Case A/B and the logs in INC-JVM-201. |

## Expected outcome

- A repaired ledger that meets the validation table.
- A worksheet with hypothesis, evidence, next step, stabilize, remediate, and comms — filled in your words.
- An RCA that a staff engineer could review without opening your editor.

## Interview questions

1. How would you prove a duplicate debit is the same customer click and not two legitimate orders?
2. Why might a unit test that calls `authorize` twice on one thread miss this incident?
3. What metric would you add so Harbor Bike Co is not the first detector?

## Architecture/trade-off questions

1. When is an in-memory seen-keys map acceptable, and when must the unique constraint live in the database?
2. If you add a lock to stop duplicates, what new failure mode must you consider?
3. Should the HTTP API return 201 for a replay or 200 with the original resource? Why?

## Cleanup

No cloud resources. Delete any extra class files you compiled:

```bash
rm -f labs/BREAKFIX-201/starter/*.class
```

## Cost estimate

**$0.** Local JDK only. Do not create AWS resources for this lab.

## Hidden/revealable solution

Do not open this until you have a written hypothesis, three harness runs, and a proposed fix.

The root cause and reference implementation are in the instructor pack only:

- [`solutions/BREAKFIX-201/`](../../solutions/BREAKFIX-201/README.md)
- [`instructor/rubrics/BREAKFIX-201.md`](../../instructor/rubrics/BREAKFIX-201.md)

Opening those files before you attempt the lab will cap your **Diagnostic method** score. A lucky guess is not a complete diagnosis.

## What you learned

- Parallel reproduction is part of the diagnosis, not a nicety.
- A concurrent map does not make a multi-step authorize atomic.
- Stabilize (stop the canary, replay-protect in the API) is different from remediate (correct the compound update).
- Evidence order matters more than a fast answer.

## Portfolio deliverable

Export [student/worksheets/PF-concurrency-rca.md](../../student/worksheets/PF-concurrency-rca.md) with the BREAKFIX-201 sections completed. INCIDENT-202 fills the rest of the same artifact.
