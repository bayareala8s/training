# Lab 011: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Token bucket local limiter | Must |
| FR-2 | Redis sliding window global limiter | Must |
| FR-3 | Per-tenant + per-route keys | Must |
| FR-4 | 429 with Retry-After | Must |
| FR-5 | Rate limit response headers | Should |
| FR-6 | Fail-open/fail-closed config | Should |
| FR-7 | Benchmark mode | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Check latency p99 (local) | < 5ms without Redis |
| NFR-2 | Check latency p99 (Redis) | < 20ms local Docker |
| NFR-3 | Accuracy | Sliding window within 1 request |

## Acceptance Criteria

### AC-1: Burst

Rate 10/s, burst 20 → first 20 immediate, then 10/s.

### AC-2: Distributed

Two processes share 100/min tenant limit → combined ≤ 100.

### AC-3: Headers

Denied request includes `Retry-After` and `X-RateLimit-*`.

## Out of Scope

- Global multi-region limit without shared store
- Billing integration
- Priority tiers with weighted fair queuing

## Related Documentation

- [API Platform](/docs/system-design/api-platform)
