# Lab 11 notes (sample)

Minimum four scenarios. Students replace this with their own evidence.

## C3 — Stop consumer / poison

Hypothesis: amount=POISON raises and lands on the DLQ after maxReceiveCount.

Observe: CloudWatch errors + DLQ ApproximateNumberOfMessages.

Recover: fix payload; replay from DLQ only after poison is quarantined.

## C4 — Invalid JSON

Hypothesis: non-JSON body fails parse and does not silently 200.

Observe: DLQ depth, error code in logs.

Recover: producer contract test.

## C5 — Duplicate / idempotent put

Hypothesis: same messageId conditional put does not double-post.

Observe: one POSTED item.

Recover: ConditionExpression attribute_not_exists(pk).

## C6 — Duplicate file

Hypothesis: second PUT of identical bytes is DuplicateDetected.

Observe: catalog HASH# status.

Recover: do not treat as a new accepted file.

Alarms: DLQ visible > 0. Silent failure would be a PASS that always prints PASS — that is why validate_lab.py actually sends poison.
