# Lab 002: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | `VectorClock.increment(i)` on local/send/receive rules | Must |
| FR-2 | `VectorClock.merge(other)` per receive rule | Must |
| FR-3 | `compare(a,b)` returns BEFORE/AFTER/CONCURRENT/EQUAL | Must |
| FR-4 | `Process` simulates send/receive with clock attachment | Must |
| FR-5 | `VersionVector` tracks per-replica counters for KV keys | Must |
| FR-6 | `CausalMailbox` delivers respecting happens-before | Must |
| FR-7 | `ConflictResolver` supports LWW and multi-value | Should |
| FR-8 | CLI trace replay from JSON scenario file | Could |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Comparison correctness | Matches textbook domination rules |
| NFR-2 | Deterministic simulation | Same trace → same delivery order |
| NFR-3 | Test coverage | ≥ 85% on `src/` |
| NFR-4 | API clarity | Enum for `Relation`, typed vectors |

## Acceptance Criteria

### AC-1: Classic causality

Given trace: P0 local → P0 send → P1 receive → P1 local, `compare(V_receive, V_send) == AFTER`.

### AC-2: Concurrency detection

Given independent branches on P0 and P1 with no message exchange, final clocks are `CONCURRENT`.

### AC-3: Causal delivery

If messages arrive [m2, m1] but m1 → m2, delivery order is [m1, m2].

### AC-4: Sibling writes

Two concurrent puts to same key return two values under multi-value resolver.

## Out of Scope

- Dynamic membership / epoch vectors
- Hybrid logical clocks
- Network transport
- Persistent storage

## Related Documentation

- [Vector Clocks](/docs/time-ordering-and-coordination/vector-clocks)
- [Eventual Consistency](/docs/consistency/eventual-consistency)
