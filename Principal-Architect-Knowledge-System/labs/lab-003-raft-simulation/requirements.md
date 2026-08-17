# Lab 003: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Node roles: Follower, Candidate, Leader | Must |
| FR-2 | `RequestVote` with log up-to-date check | Must |
| FR-3 | `AppendEntries` heartbeat and replication | Must |
| FR-4 | Conflict resolution: delete conflicting suffix, append | Must |
| FR-5 | `commitIndex` advances on majority replication | Must |
| FR-6 | Deterministic `KVStore` apply from log | Must |
| FR-7 | Client redirect on non-leader | Should |
| FR-8 | Chaos CLI for leader kill / partition | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Election completion | < 2s after leader crash (3 nodes, local Docker) |
| NFR-2 | RPC idempotency | Duplicate AppendEntries safe |
| NFR-3 | Race detection | `go test -race` clean |
| NFR-4 | Log durability | Survive process restart (file persist) |

## Acceptance Criteria

### AC-1: Single leader

In 10s simulation with 3 nodes, never two leaders in same term (instrumented test).

### AC-2: Commit safety

Write `k=v` committed on leader; kill leader; new leader `get k` returns `v`.

### AC-3: Partition behavior

Under majority/minority split, minority cannot commit new writes.

### AC-4: Log convergence

After healing partition, all nodes have identical logs.

## Out of Scope

- Byzantine fault tolerance
- Snapshot / compaction (extension)
- Joint consensus membership changes (extension)
- Linearizable reads without leader contact

## Related Documentation

- [Raft](/docs/consensus/raft)
- [FLP Impossibility](/docs/consensus/flp-impossibility)
