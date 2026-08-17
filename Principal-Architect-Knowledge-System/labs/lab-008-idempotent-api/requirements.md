# Lab 008: Requirements

## Functional requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-1 | `POST /v1/payments` with `Idempotency-Key` | Must | Implemented |
| FR-2 | Replay identical response on duplicate | Must | Implemented |
| FR-3 | Reject same key + different body (`409`) | Must | Implemented |
| FR-4 | Single ledger entry under concurrent dupes | Must | Implemented |
| FR-5 | Webhook `event_id` deduplication | Should | Implemented |
| FR-6 | Key TTL expiration | Should | Implemented |
| FR-7 | `GET /health` endpoint | Should | Implemented |
| FR-8 | Swagger UI at `/docs` | Should | Implemented |

## Non-functional requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Runs without database | In-memory only |
| NFR-2 | Tests pass without Docker | Yes |
| NFR-3 | Startup time | < 5s |

## Acceptance criteria

### AC-1: Retry safety

Same key, same body, 5 retries → 1 payment, 5 identical `201` responses.

### AC-2: Payload mismatch

Same key, different amount → `409` with clear error.

### AC-3: Webhook dedup

Duplicate `event_id` → single side effect.

## Out of scope

- Durable persistence (see Lab 017)
- PCI DSS compliance
- Multi-region idempotency store
