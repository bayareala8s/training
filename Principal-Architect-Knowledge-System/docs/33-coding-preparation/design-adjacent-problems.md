---
id: design-adjacent-problems
title: Design-Adjacent Problems
sidebar_position: 3
slug: /coding-preparation/design-adjacent-problems
domain: coding-preparation
difficulty: intermediate
status: complete
last_reviewed: 2026-08-02
tags: [coding, algorithms, interview, principal-architect]
---

# Design-Adjacent Problems

These are the **highest-yield coding problems** for Principal Architect interviews. Each connects to curriculum chapters and labs. Practice **explaining aloud** while writing pseudo-code — not silently grinding LeetCode.

## Problem Bank

| # | Problem | Why principals see it | Curriculum link | Lab |
|---|---------|----------------------|-----------------|-----|
| 1 | **Rate limiter** | Every API platform | [Distributed Rate Limiter](/docs/system-design/distributed-rate-limiter) | [Lab 011](/docs/system-design/distributed-rate-limiter#25-hands-on-exercise) `:8101` |
| 2 | **Idempotent POST handler** | Payments, workflows | [Idempotency](/docs/distributed-systems-foundations/idempotency) | [Lab 008](/docs/distributed-systems-foundations/idempotency#25-hands-on-exercise) `:8081` |
| 3 | **LRU cache** | CDN, feed, session | [Caching Fundamentals](/docs/caching/caching-fundamentals) | — |
| 4 | **Consistent hashing** | Sharding, Dynamo-style | [Distributed Caching](/docs/caching/distributed-caching) | [Lab 001](/docs/caching/distributed-caching#25-hands-on-exercise) `:8096` |
| 5 | **Autocomplete / top-K** | Search boxes | [Search Autocomplete](/docs/system-design/search-autocomplete) | — |
| 6 | **URL shortener encode/decode** | Base62, collision | [URL Shortener](/docs/system-design/url-shortener) | — |
| 7 | **Producer-consumer queue** | Backpressure, streaming | [Message Delivery Semantics](/docs/messaging-and-streaming/message-delivery-semantics) | [Lab 006](/docs/messaging-and-streaming/kafka-architecture#25-hands-on-exercise) `:8094` |
| 8 | **Merge K sorted streams** | Log aggregation | [Logging Platform](/docs/system-design/logging-platform) | — |
| 9 | **Interval merge / meeting rooms** | Scheduling, capacity | [Workflow Engine](/docs/system-design/workflow-engine) | — |
| 10 | **Serialize / deserialize tree or graph** | API payloads | [REST, gRPC, and GraphQL](/docs/api-and-integration-architecture/rest-grpc-and-graphql) | — |
| 11 | **Thread-safe counter / metrics** | Observability | [Metrics Platform](/docs/system-design/metrics-platform) | — |
| 12 | **Detect cycle in linked structure** | Poison messages, refs | [Sagas](/docs/transactions/sagas) | [Lab 010](/docs/transactions/sagas#25-hands-on-exercise) `:8093` |

## Deep Dive: Rate Limiter (Token Bucket)

**Prompt:** Implement a rate limiter: max 100 requests per minute per `client_id`.

**Clarify:**

- Per-process or distributed? (Assume single-node first, then extend to Redis)
- Burst allowed? (Token bucket vs fixed window)
- What HTTP status on reject? (429 + `Retry-After`)

**Pseudo-code sketch:**

```python
class TokenBucket:
    def __init__(self, rate_per_sec: float, burst: int):
        self.rate = rate_per_sec
        self.capacity = burst
        self.tokens = burst
        self.last_refill = now()

    def allow(self) -> bool:
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

    def _refill(self):
        elapsed = now() - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now()
```

**Principal follow-ups:**

- Race conditions if multiple threads? → lock or atomic compare-and-swap
- Distributed? → Redis `INCR` + TTL or centralized token service
- Hot key on celebrity client? → local shard of limit state

## Deep Dive: Idempotent API Handler

**Prompt:** `POST /charges` with header `Idempotency-Key`. Duplicate keys must return the same response without double-charging.

**Core logic:**

1. Lookup `(tenant_id, idempotency_key)` in store
2. If `completed` → return cached response
3. If `in_progress` → return 409 or poll
4. Else insert `in_progress`, process, store result, mark `completed`

Link: [Stripe Payment Idempotency](/docs/real-world-scenarios/stripe-payment-idempotency) scenario.

## Deep Dive: Consistent Hashing

**Prompt:** Given N servers and string keys, route key to server; add/remove server with minimal remapping.

**Signals:**

- Virtual nodes for balance
- O(log N) lookup with sorted ring
- Know remapping fraction ≈ 1/N on add/remove

Lab: [Consistent hashing](/docs/caching/distributed-caching#25-hands-on-exercise) on `:8096`

## Deep Dive: Autocomplete

**Prompt:** Given prefix, return top 5 suggestions by frequency.

**Approaches:**

| Approach | Tradeoff |
|----------|----------|
| Trie + heap per node | Fast prefix, memory heavy |
| Elasticsearch / prefix index | Production realistic |
| Sorted array + binary search | Simple, poor for updates |

Principal angle: discuss **incremental indexing** and **staleness** — not just trie traversal.

## Complexity Cheat Sheet

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| Rate limiter (single node) | O(1) per request | O(clients) | Ring or map of buckets |
| LRU cache | O(1) get/put | O(capacity) | Hash map + doubly linked list |
| Consistent hash lookup | O(log V) | O(V) virtual nodes | V = virtual nodes |
| Merge K sorted | O(N log K) | O(K) | Min-heap |
| Autocomplete trie | O(L + K log K) | O(total chars) | L = prefix length |

## Practice Format (45 min)

| Phase | Time | Activity |
|-------|------|----------|
| Clarify | 5 min | Requirements, constraints, API shape |
| Approach | 5 min | Data structures, complexity, tradeoffs |
| Implement | 20 min | Core path in pseudo-code or language |
| Test | 5 min | Normal, edge, failure cases |
| Extend | 10 min | Scale, distribution, observability |

## Anti-Patterns in Principal Coding Rounds

| Anti-pattern | Why it fails |
|--------------|--------------|
| Silent coding for 15+ minutes | Panel cannot calibrate; looks like Staff, not Principal |
| Ignoring idempotency on mutations | Shows gap between code and production |
| No mention of tests | Principal owns quality bar |
| Over-optimizing obscure DP | Wrong signal for architecture roles |

## Related

- [Practice Routine](/docs/coding-preparation/practice-routine)
- [Coding Mock Interview](/docs/coding-preparation/coding-mock-interview)
- [System Design Methodology](/docs/system-design/system-design-methodology)
