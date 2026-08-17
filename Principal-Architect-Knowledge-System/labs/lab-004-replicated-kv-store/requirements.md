# Lab 004: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | `PUT/GET/DELETE` HTTP API for keys | Must |
| FR-2 | Consistent-hash routing to shards | Must |
| FR-3 | Per-shard Raft replication | Must |
| FR-4 | Configurable N, R, W per shard | Must |
| FR-5 | Version attached to every value | Must |
| FR-6 | Read repair on version mismatch | Should |
| FR-7 | Hinted handoff when replica unavailable | Should |
| FR-8 | Health and readiness endpoints | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Write availability | Majority shards reachable |
| NFR-2 | p99 read latency (local Docker) | < 50ms at RF=2 |
| NFR-3 | No lost committed writes | Raft safety per shard |
| NFR-4 | Idempotent retries | Client `Idempotency-Key` header |

## Acceptance Criteria

### AC-1: Sharded CRUD

Keys `a` and `b` hash to different shards; independent failover does not block unrelated keys.

### AC-2: Quorum read

With N=3, R=2, one stale replica: client still receives latest version.

### AC-3: Failover

Kill shard leader; new leader elected; committed writes readable within 5s.

### AC-4: Read repair

After injecting stale replica, first read triggers repair; second read hits all replicas at same version.

## Out of Scope

- Global secondary indexes
- Cross-shard ACID transactions
- Multi-region active-active
- Automatic shard splitting

## Related Documentation

- [Quorum Systems](/docs/consistency/quorum-systems)
- [Conflict Resolution](/docs/replication/conflict-resolution)
