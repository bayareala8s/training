# Lab 009: Requirements

## Functional

| ID | Requirement | Status |
|----|-------------|--------|
| FR-1 | Atomic order + outbox insert | Implemented |
| FR-2 | Relay publishes unpublished events | Implemented |
| FR-3 | Mark `published_at` after publish | Implemented |
| FR-4 | Consumer dedupes by `event_id` | Implemented |
| FR-5 | Ordering by `created_at` per relay batch | Implemented |
| FR-6 | HTTP API + Swagger | Implemented |
| FR-7 | `GET /health` with stats | Implemented |

## Acceptance criteria

### AC-1: No dual-write

Order and outbox row appear together or neither (transaction rollback on failure — in-memory simulates commit).

### AC-2: Relay crash-safe

Unpublished events relayed on next `POST /v1/relay/run`.

### AC-3: Duplicate consumer safe

Second `POST /v1/consumer/run` reports duplicates, inventory unchanged.

## Out of scope

- Real Kafka producer (use `--profile full` compose for infra only)
- Debezium CDC (extension exercise)
