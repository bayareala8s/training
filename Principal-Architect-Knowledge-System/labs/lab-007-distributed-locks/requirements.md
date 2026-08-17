# Lab 007: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Redis lock acquire/release | Must |
| FR-2 | Lock TTL and renewal | Must |
| FR-3 | Monotonic fencing token per resource | Must |
| FR-4 | Resource rejects stale fence_id | Must |
| FR-5 | Stale holder demonstration CLI | Must |
| FR-6 | etcd lease lock (optional) | Should |
| FR-7 | Health endpoints | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Lock acquire p99 (local) | < 20ms |
| NFR-2 | Fencing check | O(1) per write |
| NFR-3 | No deadlock on client crash | TTL frees lock |

## Acceptance Criteria

### AC-1: Mutual exclusion

Two workers competing — only one `acquire` succeeds until release/TTL.

### AC-2: Fencing protection

After W2 writes with fence=5, W1 write with fence=4 rejected.

### AC-3: Stale holder demo

CLI chaos produces log line showing fenced rejection.

## Out of Scope

- Byzantine fault tolerance
- Global lock service multi-region
- Full Redlock N-instance algorithm

## Related Documentation

- [ZooKeeper](/docs/consensus/zookeeper)
