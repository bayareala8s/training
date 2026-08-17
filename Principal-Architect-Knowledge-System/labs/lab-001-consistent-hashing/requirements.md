# Lab 001: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | `HashRing.add_node(node_id, vnode_count)` adds vnode positions | Must |
| FR-2 | `HashRing.remove_node(node_id)` removes all vnodes for node | Must |
| FR-3 | `HashRing.get_node(key)` returns owning physical node | Must |
| FR-4 | Lookup wraps around ring when hash exceeds max position | Must |
| FR-5 | Empty ring lookup raises explicit error | Must |
| FR-6 | `redistribution_ratio()` computes key churn on membership change | Must |
| FR-7 | CLI `--demo` prints sample mappings and balance stats | Should |
| FR-8 | CLI `--inject` runs failure scenarios | Should |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Lookup latency | O(log V) — acceptable for lab scale |
| NFR-2 | Hash stability | Same key → same position across process restarts |
| NFR-3 | Determinism | Same operations → same ring state (no randomness) |
| NFR-4 | Test coverage | ≥ 80% on `src/` |
| NFR-5 | Code style | Type hints on public API |

## Acceptance Criteria

### AC-1: Minimal remapping

Given a ring with 5 nodes (128 vnodes each) and 10,000 random keys, when one node is removed, **fewer than 30%** of keys change owner (expected ~20%). Modulo hashing with N changing must remap **> 50%** in the same scenario.

### AC-2: Load balance

With 10 nodes, 128 vnodes, 100,000 keys: coefficient of variation across nodes **< 0.15**.

### AC-3: Idempotent membership

Adding the same `node_id` twice without removal does not duplicate vnodes (second add is no-op or raises clear error).

### AC-4: Correct wraparound

Key hashing to position greater than all vnodes maps to the minimum ring position's owner.

## Out of Scope

- Network protocol for ring gossip
- Data migration execution (only metrics)
- Persistence across restarts
- Byzantine node behavior

## Dependencies

```
pytest>=8.0
pytest-cov>=5.0
sortedcontainers>=2.4   # optional; bisect acceptable
```

## Related Documentation

- [Distributed Caching](/docs/caching/distributed-caching)
- [Quorum Systems](/docs/consistency/quorum-systems)
