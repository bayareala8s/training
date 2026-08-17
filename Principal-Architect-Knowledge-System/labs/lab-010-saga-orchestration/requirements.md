# Lab 010: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Saga orchestrator with state machine | Must |
| FR-2 | Payment reserve/compensate | Must |
| FR-3 | Inventory reserve/release | Must |
| FR-4 | Shipping create/cancel | Must |
| FR-5 | Persistent saga log | Must |
| FR-6 | Crash recovery from log | Must |
| FR-7 | Idempotent participant handlers | Must |
| FR-8 | Step timeout and retry | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Happy path latency (local) | < 2s |
| NFR-2 | Recovery after crash | < 30s resume |
| NFR-3 | No duplicate side effects | Idempotent steps |

## Acceptance Criteria

### AC-1: Happy path

Create order saga → `completed` with all reservations committed.

### AC-2: Compensation

Force inventory failure → payment compensated, saga `compensated`.

### AC-3: Recovery

Kill orchestrator after payment step → restart → saga completes.

## Out of Scope

- Distributed 2PC
- Cross-region saga
- Visual workflow designer

## Related Documentation

- [Transactional Outbox](/docs/transactions/transactional-outbox)
