# Lab 006: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Produce orders to partitioned topic | Must |
| FR-2 | Enrichment consumer with offset commit | Must |
| FR-3 | 1-minute windowed aggregates | Must |
| FR-4 | Idempotent processing by `order_id` | Must |
| FR-5 | DLT for poison messages | Should |
| FR-6 | DLT replay CLI | Should |
| FR-7 | Consumer lag reporting | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Processing latency (local) | p99 < 500ms per batch |
| NFR-2 | No duplicate metrics on replay | Idempotent aggregate keys |
| NFR-3 | Graceful shutdown | Commit offsets on SIGTERM |

## Acceptance Criteria

### AC-1: Partition ordering

All events for same `customer_id` processed in partition order.

### AC-2: Window accuracy

100 orders in same minute/region → `count=100`, `revenue=sum(amount)`.

### AC-3: At-least-once recovery

Kill consumer mid-batch; restart; no lost orders (may duplicate — deduped).

### AC-4: DLT routing

Malformed message does not block partition; appears in DLT with error header.

## Out of Scope

- Multi-broker Kafka cluster
- Kafka Streams / Flink deployment
- Geo-replicated MirrorMaker

## Related Documentation

- [Stream and Batch Processing](/docs/data-platforms/stream-and-batch-processing)
