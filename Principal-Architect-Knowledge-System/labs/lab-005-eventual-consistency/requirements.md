# Lab 005: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Multi-replica KV with async replication | Must |
| FR-2 | Configurable replication delay and loss | Must |
| FR-3 | Version vector per key | Must |
| FR-4 | Read-your-writes via sticky routing | Must |
| FR-5 | Monotonic reads via session token | Should |
| FR-6 | Read repair on version mismatch | Should |
| FR-7 | Background anti-entropy (checksum diff) | Should |
| FR-8 | CLI chaos: partition, replica-down | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Convergence time after heal | < 10s for 1k keys (local) |
| NFR-2 | Idempotent replication apply | Duplicate msgs safe |
| NFR-3 | Deterministic simulation seed | Reproducible tests |

## Acceptance Criteria

### AC-1: Eventual convergence

Write to one replica; after replication completes, all replicas return same value.

### AC-2: Stale read demonstration

Without session stickiness, read from lagging replica returns older value; document version.

### AC-3: Read-your-writes

Client writes then reads via same session — never sees pre-write value.

### AC-4: Conflict detection

Concurrent writes on partitioned replicas produce sibling version vectors detectable by `compare()`.

## Out of Scope

- Multi-region geo-replication
- Strong linearizability
- Automatic conflict resolution policy (LWW, CRDT merge)

## Related Documentation

- [Session Guarantees](/docs/consistency/session-guarantees)
- [Leaderless Replication](/docs/replication/leaderless-replication)
