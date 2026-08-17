# Lab 005: Architecture

## Overview

Three-tier simulation: **client session layer**, **replica cluster**, and **background convergence** — mirroring Cassandra, DynamoDB (eventual mode), and Riak patterns.

```mermaid
flowchart TB
    subgraph Clients
        C1[Client A sticky=R1]
        C2[Client B quorum read]
    end
    subgraph Cluster
        R1[Replica 1 Primary for A]
        R2[Replica 2]
        R3[Replica 3]
    end
    subgraph Background
        AE[Anti-Entropy Worker]
        RR[Read Repair on demand]
    end
    C1 --> R1
    C2 --> R1 & R2 & R3
    R1 --> RR
    AE --> R1 & R2 & R3
```

## Write Path

```mermaid
sequenceDiagram
    participant C as Client
    participant L as Local Replica
    participant P as Peer Replicas

    C->>L: PUT key (W=1 fast path)
    L->>L: apply + version++
    L-->>C: ack + version token
    L->>P: async REPLICATE (delayed)
    Note over P: Peers apply when message arrives
```

**Safety:** With `W=1`, acknowledged write may be lost if sole replica fails before replication — document this tradeoff.

**Liveness:** Writes succeed during partition if client targets reachable replica (AP behavior).

## Read Path with Session Token

```mermaid
sequenceDiagram
    participant C as Client
    participant R as Sticky Replica
    participant P as Peer

    C->>R: GET key + session_token
    R->>R: compare token vs local version
    alt token stale locally
        R->>P: quorum read R=2
        P-->>R: latest version
        R->>R: read repair if needed
    end
    R-->>C: value + new token
```

## Consistency Modes

| Mode | Behavior | Use case |
|------|----------|----------|
| Eventual | Any replica may serve stale read | High read availability |
| Read-your-writes | Sticky + token | User sees own updates |
| Monotonic reads | Token prevents time travel | Feed pagination |
| Quorum (R+W>N) | Overlapping read/write sets | Stronger per-key guarantees |

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `Replica` | Local KV + version vector per key |
| `ReplicationBus` | Delayed, lossy message delivery |
| `SessionRouter` | Sticky replica + token management |
| `ReadRepair` | On-read divergence healing |
| `AntiEntropy` | Background checksum sync |

## Docker Topology

3 containers (`replica-1`, `replica-2`, `replica-3`) each running `src/main.py --replica-id N`. Optional `simulator` container drives chaos.

## Data Model

```
Key: string
Value: bytes
VersionVector: {replica_id: counter}
SessionToken: opaque client-held version summary
Tombstone: deleted keys replicate as tombstones
```

## Related Documentation

- [Eventual Consistency](/docs/consistency/eventual-consistency)
- [Conflict Resolution](/docs/replication/conflict-resolution)
- [Vector Clocks](/docs/time-ordering-and-coordination/vector-clocks)
