# Lab 003: Architecture

## System Context

A minimal **Replicated State Machine** where client commands (`Put`, `Get`) flow through Raft log replication. Each node runs identical deterministic `KVStore` logic applied in log order.

```mermaid
flowchart TB
    Client[Client CLI] --> L[Leader]
    L -->|AppendEntries| F1[Follower 1]
    L -->|AppendEntries| F2[Follower 2]
    L --> SM_L[KV State Machine]
    F1 --> SM_F1[KV State Machine]
    F2 --> SM_F2[KV State Machine]
```

## Node Internals

```mermaid
flowchart LR
    subgraph RaftNode
        RPC[RPC Layer]
        CORE[Raft Core]
        LOG[(Persistent Log)]
        SM[State Machine]
    end
    RPC --> CORE
    CORE --> LOG
    CORE --> SM
```

| Module | File | Responsibility |
|--------|------|----------------|
| `raft.go` | Core FSM | Terms, votes, replication |
| `rpc.go` | HTTP/gRPC | RequestVote, AppendEntries |
| `log.go` | Entry store | Indexed (term, command) log |
| `kv.go` | Application | Deterministic command apply |
| `main.go` | Entrypoint | CLI, server bootstrap |

## RPC Definitions

### RequestVote

```
RequestVoteArgs:  term, candidateId, lastLogIndex, lastLogTerm
RequestVoteReply: term, voteGranted
```

### AppendEntries

```
AppendEntriesArgs:  term, leaderId, prevLogIndex, prevLogTerm, entries[], leaderCommit
AppendEntriesReply: term, success, matchIndex
```

## Safety Properties

| Property | Mechanism |
|----------|-----------|
| **Election safety** | At most one leader per term |
| **Leader append-only** | Leader never overwrites/deletes own entries |
| **Log matching** | Same index+term → identical prefix |
| **Leader completeness** | Committed entries appear in future leader logs |
| **State machine safety** | Same commands → same state on all nodes |

## Liveness Properties

| Property | Requirement |
|----------|-------------|
| **Leader election** | Eventually a leader if majority reachable |
| **Replication** | Committed entries eventually applied everywhere |

**Partial synchrony:** Election timeouts must exceed network delay for liveness — not guaranteed under arbitrary delays (FLP context).

## Docker Cluster

```mermaid
flowchart TB
    subgraph Docker Network
        N1[raft-node-1 :9001]
        N2[raft-node-2 :9002]
        N3[raft-node-3 :9003]
    end
    N1 <--> N2
    N2 <--> N3
    N1 <--> N3
```

Each container mounts `./data/node-{id}` for log persistence across restarts.

## Failure Boundaries

```mermaid
flowchart TB
    subgraph Majority["Majority Partition (can commit)"]
        A[Node 1 Leader]
        B[Node 2]
    end
    subgraph Minority["Minority Partition (cannot commit)"]
        C[Node 3 isolated]
    end
```

Minority leader (if any) cannot commit new entries from prior terms; clients see unavailability or stale reads depending on implementation.

## Related Documentation

- [Raft](/docs/consensus/raft)
- [Membership Changes](/docs/consensus/membership-changes)
- [Linearizability](/docs/consistency/linearizability)
