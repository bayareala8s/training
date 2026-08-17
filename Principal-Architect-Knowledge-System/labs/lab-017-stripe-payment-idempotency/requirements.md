# Lab 017: Requirements

## Functional

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | `POST /v1/charges` requires `Idempotency-Key` | Must |
| FR-2 | Duplicate key + same body replays identical 201 | Must |
| FR-3 | Duplicate key + different body returns 409 | Must |
| FR-4 | Concurrent duplicates → one order | Must |
| FR-5 | Stripe mock dedupes PaymentIntents per key | Must |
| FR-6 | Webhook `event_id` deduplication | Must |
| FR-7 | Sweeper heals stuck `processing` | Should |
| FR-8 | Fail closed when store down (503) | Must |

## Non-functional

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Runs without AWS | 100% local |
| NFR-2 | Tests pass without Docker | SQLite path |
| NFR-3 | Docker stack starts in < 2 min | Compose healthchecks |

## Acceptance criteria

### AC-1: Ambiguous timeout

Client sends same `Idempotency-Key` twice → identical `payment_intent_id`, one order row.

### AC-2: Webhook at-least-once

Duplicate webhook delivery → `webhook_events` has one row; second returns `duplicate: true`.

### AC-3: Scenario traceability

Every FR maps to a pytest in `tests/test_stripe_idempotency_lab.py`.

## Out of scope

- PCI DSS certification
- Multi-region Aurora Global Database
- Real Stripe live charges
