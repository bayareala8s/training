# Chaos scenarios

| ID | Break | Observe | Recover |
|----|-------|---------|---------|
| C1 | Set Lambda reserved concurrency 0 | Queue depth / iterator | Restore concurrency; drain |
| C2 | Client timeout shorter than work | Duplicate posts | Idempotency keys |
| C3 | Stop consumer | DLQ or visibility | Restart; replay |
| C4 | Invalid JSON | DLQ + error code | Fix producer or quarantine |
| C5 | Replay same event id | Second projection? | Conditional put |
| C6 | PUT same file twice | DuplicateDetected | Catalog hash |
| C7 | IAM deny on DynamoDB | 5xx + no silent 200 | Fix policy; alarm |

Minimum: complete four with notes in submissions/lab-11/notes.md.
