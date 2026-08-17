# Lab 007: Architecture

## Overview

Separates **coordination plane** (lock/lease) from **data plane** (resource with fencing) — the pattern required for leader election, shard migration, and shared storage writers.

```mermaid
flowchart TB
    subgraph Coordination
        LS[Lock Service]
        FS[Fencing Service]
    end
    subgraph Storage
        R[Resource API]
        DB[(Blob Metadata)]
    end
    W[Worker] --> LS
    W --> FS
    W --> R
    LS --> Redis[(Redis)]
    LS --> Etcd[(etcd)]
    FS --> Etcd
    R --> DB
```

## Lock Acquire Sequence

```mermaid
sequenceDiagram
    participant W as Worker
    participant L as Lock Service
    participant F as Fencing
    participant R as Resource

    W->>L: acquire(resource, ttl)
    L-->>W: lock_token
    W->>F: get_fence(resource)
    F-->>W: fence_id=42
    W->>R: write(resource, fence_id, data)
    R->>R: fence_id > last_fence?
    R-->>W: OK
    W->>L: release(lock_token)
```

## Stale Holder (Safety Violation Without Fencing)

```mermaid
sequenceDiagram
    participant W1 as Worker 1 delayed
    participant W2 as Worker 2
    participant L as Lock
    participant R as Resource

    W1->>L: acquire (expires)
    Note over W1: GC pause
    W2->>L: acquire success
    W2->>R: write fence=43 OK
    W1->>R: write fence=42
    alt no fencing
        R-->>W1: corrupt state
    else with fencing
        R-->>W1: REJECT stale fence
    end
```

## Safety and Liveness

| Property | Mechanism |
|----------|-----------|
| Safety (mutual exclusion) | Single lock holder per resource (best-effort with Redis) |
| Safety (resource integrity) | Monotonic fencing at resource |
| Liveness | TTL expiry frees lock; retry with backoff |

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `RedisLock` | NX+PX acquire, Lua release |
| `LockRenewer` | Periodic TTL extension |
| `FencingService` | Monotonic counter per resource |
| `GatedResource` | Reject stale fence writes |
| `StaleHolderSim` | Chaos: pause + delayed write |

## Docker Topology

- `redis:7` on 6379
- `quay.io/coreos/etcd:v3.5` on 2379

## Related Documentation

- [Fencing Tokens](/docs/consensus/fencing-tokens)
- [etcd](/docs/consensus/etcd)
