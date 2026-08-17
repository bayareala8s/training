# Lab 004: Architecture

## Overview

Multi-tier architecture separating **routing**, **sharding**, and **replication** — the pattern used by TiKV, CockroachDB (range-based variant), and Dynamo-family systems.

```mermaid
flowchart TB
    subgraph ClientTier
        C[HTTP/gRPC Client]
    end
    subgraph Gateway
        R[Router + HashRing]
        API[REST API]
    end
    subgraph Shard0["Shard 0 (keys hash to ring segment)"]
        L0[Raft Leader]
        F0[Raft Follower]
    end
    subgraph Shard1["Shard 1"]
        L1[Raft Leader]
        F1[Raft Follower]
    end
    C --> API --> R
    R --> L0 & L1
    L0 --> F0
    L1 --> F1
```

## Write Path

```mermaid
sequenceDiagram
    participant C as Client
    participant R as Router
    participant L as Shard Leader
    participant F as Follower

    C->>R: PUT key=value
    R->>R: hash(key) → shard
    R->>L: Replicate command
    L->>F: AppendEntries
    F-->>L: ACK
    L-->>R: committed version
    R-->>C: 201 + version
```

## Read Path with Repair

```mermaid
sequenceDiagram
    participant C as Client
    participant R as Router
    participant L as Leader
    participant F as Stale Follower

    C->>R: GET key (R=2, N=3)
    R->>L: Read
    R->>F: Read
    F-->>R: stale version
    L-->>R: latest version
    R->>F: ReadRepair push
    R-->>C: latest value
```

## Quorum Configuration

| Mode | N | R | W | Guarantee (with versions) |
|------|---|---|---|---------------------------|
| Strong | 3 | 2 | 2 | R+W>N → overlapping quorum |
| Fast write | 3 | 1 | 2 | Eventual read risk |
| Fast read | 3 | 2 | 1 | Stale write risk |

**Safety:** Version comparison prevents returning arbitrarily stale values when `R+W>N` and versions are checked on read (Dynamo model).

**Liveness:** Sloppy quorum + hinted handoff improves write availability during replica failure at cost of complexity.

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `HashRing` | Key → shard mapping (from Lab 001) |
| `ShardManager` | Shard → peer list, leader hints |
| `RaftGroup` | Per-shard consensus (from Lab 003) |
| `KVStore` | Versioned key-value state machine |
| `ReadRepair` | Anti-entropy on read path |
| `HintedHandoff` | Temporary write buffering |

## Docker Topology

6 containers: `kv-0a`, `kv-0b`, `kv-1a`, `kv-1b`, `kv-2a`, `kv-2b` plus optional `gateway`.

Each node knows `--shard-id`, `--peer-list`, `--node-id`.

## Data Model

```
Key:   string (UTF-8)
Value: bytes (JSON in API)
Version: vector clock OR monotonic hybrid timestamp
Tombstone: for deletes (replication of deletion)
```

## Related Documentation

- [Amazon Dynamo](/docs/distributed-databases/amazon-dynamo)
- [Leaderless Replication](/docs/replication/leaderless-replication)
- [Distributed Cache Design](/docs/system-design/distributed-cache-design)
