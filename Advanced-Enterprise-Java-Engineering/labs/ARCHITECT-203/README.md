# ARCHITECT-203 — Safe concurrent payment processing

**Lab type:** ARCHITECT  
**Duration:** 60–90 minutes  
**Cost:** $0  
**Case study:** BayPay Financial Services (fictional)

Design first, then write a small in-process slice. A summarized reference direction is in a details block at the bottom — expand it only after you have a design of your own.

## Scenario

BayPay wants to promote a canary authorize worker that can survive Harbor Bike Co’s retry pattern and a weekday refund burst without repeating Module 2’s two incidents. You are the staff engineer asked for a design that a senior can implement in a week: in-process concurrency for a single JVM, with a clear story for the day a second instance appears.

You will produce a one-page architecture note, a lock/collection/executor policy, and a small compilable Java slice that authorizes in parallel without losing totals or double-posting a key.

## Business context

Product invariants:

1. At most one post per `Idempotency-Key`.
2. Account totals equal the sum of accepted posts.
3. Payment and refund paths cannot permanently stop each other.
4. A retry storm cannot create unbounded threads or an unbounded queue of money work.
5. When two JVM instances exist, the database unique key is the system of record.

Avery Chen / account `22222222-2222-2222-2222-222222222221` remain the demo identities. Amounts are synthetic.

## Learning objectives

- Choose concurrent collections and executor/virtual-thread policy on purpose.
- Write a lock policy that is one sentence a reviewer can check.
- Implement a small parallel authorize slice that would pass BREAKFIX-201’s two cases.
- State what the slice does *not* guarantee (crash atomicity, multi-instance).

## Architecture

Draw (mermaid or ASCII) a single-JVM worker:

```text
HTTP or harness
    → admission bound (semaphore or bounded queue)
    → authorize tasks (platform pool or virtual threads — pick one and say why)
    → idempotency structure
    → account total + journal (one compound story)
    → metrics (atomics / LongAdder, not inside the money lock unless needed)
```

Show where a refund path enters and which policy keeps both paths moving. Diagram **AEJE-D-008** is the course target picture; your drawing can be simpler.

Do not split payment and refund into microservices for this lab. The modular monolith remains the default.

## Prerequisites

- Lessons L-2.3, L-2.4, and L-2.5.
- BREAKFIX-201 and INCIDENT-202 attempted so your design is a response, not a guess.

## Environment setup

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
mkdir -p labs/ARCHITECT-203/work
cd labs/ARCHITECT-203/work
```

You will create `ConcurrentPaymentProcessor.java` (any reasonable name) in `work/`. Java 21, `javac` only.

## Challenge/tasks

1. Write a design note (`work/DESIGN.md`, 40–80 lines) covering:
   - collection choices and the exact atomic verbs (`putIfAbsent`, `merge`, …);
   - executor or virtual threads, pool/queue/semaphore bounds, rejection behavior;
   - lock policy in one sentence;
   - multi-instance story (one paragraph);
   - what you explicitly will not solve (be honest).
2. Implement `ConcurrentPaymentProcessor` with:
   - `boolean authorize(String paymentId, String idempotencyKey, String accountId, long amountCents)`;
   - `long balanceCents(String accountId)`;
   - `int journalSize()`;
   - a `main` that runs BREAKFIX-201’s Case A (1000 unique keys, 8 threads, 100 cents) and Case B (1000 retries of `harbor-8841`, 8400 cents).
3. Optionally add a `refund` method that cannot hang forever if payment is running — timeout or a policy that needs only one lock.
4. Re-run until Case A and Case B match expected values three times.

## Validation

- `DESIGN.md` exists and states a lock policy in one sentence.
- Case A: balance `100000`, journal `1000`.
- Case B: balance `8400`, journal `1`.
- You can explain why a second JVM would still need the database unique key.

## Troubleshooting

| Observation | What to try |
|---|---|
| Case A flickers | Compound update is still racy. Re-read L-2.3 verbs. |
| Virtual threads plus a global `synchronized` around HTTP | You do not have HTTP here; do not add fake I/O inside a lock. |
| You reintroduced two unordered locks | Revisit your one-sentence policy. |
| Design is “use synchronized on the class” only | That can pass the harness and still fail the architecture questions. |

## Expected outcome

A design note a peer can review in ten minutes, plus a small class that holds the two invariants under parallel load.

## Interview questions

1. Why might you still choose a platform pool after Java 21?
2. How do you show a reviewer that `putIfAbsent` plus `merge` plus `offer` is not crash-atomic?
3. What do you say when someone asks for `newCachedThreadPool` “just for the sale”?

## Architecture/trade-off questions

1. Single lock vs striped per-account locks vs lock-free maps — pick one and name the failure mode you accepted.
2. Where does admission control live: servlet, semaphore, HTTP client, or all three?
3. When does extracting `transaction-worker` to another process become worth the outbox?

## Cleanup

```bash
rm -f labs/ARCHITECT-203/work/*.class
```

Keep `DESIGN.md` and the `.java` file for the portfolio if you want a code appendix. The official Module 2 artifact is still the RCA worksheet.

## Cost estimate

**$0.** Local JDK only.

## Hidden/revealable solution

Attempt the design and the harness first. Then expand the details below.

<details>
<summary>Reference direction (after your attempt)</summary>

**Collections.** `ConcurrentHashMap.putIfAbsent` for idempotency keys; `ConcurrentHashMap.merge` for account totals; `ConcurrentLinkedQueue` (or a list protected by the same exclusive path as the total) for the journal. Do not use a shared `ArrayList` without exclusion.

**Compound story.** `putIfAbsent` first. If the key existed, return `false` and do not add money. If you inserted, `merge` the amount and `offer` the journal row. Document the crash window between those three calls. Production closes the window with one database transaction and a unique index on `idempotency_key`.

**Threads.** Virtual threads are reasonable if you later add blocking HTTP, but this slice is CPU-light: a small fixed platform pool (8) is enough and easier to dump. Put a bound in the design anyway (semaphore or bounded queue + `AbortPolicy`). Never `DiscardPolicy` for money.

**Lock policy (pick one and keep it).** Preferred for this slice: no explicit multi-lock — rely on per-key atomic map operations. If you also need a refund that updates the same journal, either (a) one private `final Object moneyLock` for all money movements, or (b) striped per-account locks with a written order if a second lock ever appears. Do not take two locks in opposite orders on payment vs refund.

**Multi-instance.** The heap map is not the control. `IdempotencyService` + unique constraint remains mandatory.

**What this slice will not do.** Exactly-once after a kill -9 mid-method; cross-JVM exclusion; durable audit.

See also `solutions/ARCHITECT-203/README.md` for a fuller instructor write-up after your attempt.

</details>

## What you learned

- Collection verbs and executor bounds are architecture, not decoration.
- A passing harness can still be a weak design if the multi-instance story is missing.
- Virtual threads do not replace idempotency.

## Portfolio deliverable

Attach `work/DESIGN.md` as an appendix if you wish. The scored Module 2 artifact remains [PF-concurrency-rca.md](../../student/worksheets/PF-concurrency-rca.md). Use one short paragraph there on how ARCHITECT-203 would have prevented the two incidents.
