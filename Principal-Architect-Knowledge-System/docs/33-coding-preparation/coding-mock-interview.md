---
id: coding-mock-interview
title: Coding Mock Interview
sidebar_position: 5
slug: /coding-preparation/coding-mock-interview
domain: coding-preparation
difficulty: advanced
status: complete
last_reviewed: 2026-08-02
tags: [coding, mock-interview, interview]
---

# Coding Mock Interview

A **45-minute coding mock** calibrated for Principal-level loops. Use with a peer interviewer or self-record. Score with the rubric below — same dimensions as [Mock Interview Rubric](/docs/mock-interviews/mock-interview-rubric) but weighted for code.

## Mock 1: Distributed Rate Limiter (45 min)

**Prompt (interviewer reads):**

> Design and implement a rate limiter for an API gateway. Each `client_id` may make at most **100 requests per 60 seconds**. Return whether a request is allowed. Start with a single-process solution; if time permits, discuss distribution across multiple gateway instances.

**Candidate should clarify:**

- Sliding window vs token bucket vs fixed window
- Per-client vs per-API-key vs per-IP
- Behavior when limit exceeded (429, queue, degrade)
- Thread safety

**Strong answer includes:**

- Token bucket or sliding window with O(1) per request
- Map of `client_id` → bucket state
- Discussion of Redis `INCR` + expiry for multi-instance
- Mention of hot-key sharding for celebrity clients

**Follow-ups:**

1. How do you test this without flakiness on clock boundaries?
2. What metrics would you emit?
3. How does this interact with [Airbnb Rate Limiting](/docs/real-world-scenarios/airbnb-distributed-rate-limiting)?

---

## Mock 2: Idempotent Charge API (45 min)

**Prompt:**

> Implement `POST /v1/charges` with header `Idempotency-Key`. Duplicate keys within 24 hours must return the **same** response body and status without creating a second charge.

**Strong answer includes:**

- State machine: `missing` → `in_progress` → `completed` / `failed`
- Unique constraint on `(tenant_id, idempotency_key)`
- 409 or 202 for in-flight duplicate
- Link to payment provider idempotency

**Follow-ups:**

1. What if the process crashes after charge succeeds but before DB update?
2. How does this relate to [Stripe Payment Idempotency](/docs/real-world-scenarios/stripe-payment-idempotency)?

---

## Mock 3: Design + Code Hybrid — Search Autocomplete (45 min)

**Prompt:**

> Build the **server-side** logic for search autocomplete: given a prefix string, return up to 5 suggestions ranked by historical query frequency. Data updates continuously from search logs.

**Strong answer:**

- Trie or prefix index + min-heap per node for top-K
- Or: external search index (Elasticsearch) for production realism
- Discuss write path (async aggregation) vs read path (low latency)
- Staleness acceptable? How fresh must suggestions be?

---

## Scoring Rubric

| Dimension | 1 (No hire) | 3 (Hire) | 5 (Strong hire) |
|-----------|-------------|----------|-----------------|
| **Clarification** | Codes immediately | Asks scope questions | States assumptions, non-goals, API contract |
| **Approach** | Random structure | Reasonable DS choice | Compares alternatives, states complexity |
| **Implementation** | Does not compile / major bugs | Core path works | Clean, readable, handles key edges |
| **Production sense** | Ignores failures | Mentions tests | Idempotency, metrics, rollout |
| **Communication** | Silent | Periodic updates | Continuous think-aloud, invites feedback |

**Pass bar for principal:** Average ≥ 3.5 with no dimension below 2.

## Interviewer Script

1. **0–2 min:** Intro; confirm language and format (IDE vs whiteboard)
2. **2–7 min:** Candidate clarifies; interviewer answers bounded hints only
3. **7–32 min:** Implementation; probe with follow-ups above
4. **32–40 min:** Edge cases and tests
5. **40–45 min:** Debrief — one strength, one improvement

## Self-Practice (No Peer)

1. Set 45-minute timer
2. Record screen + voice
3. Play back — count minutes of silence (target: &lt; 2 min total)
4. Score yourself with rubric; file gaps in `progress/weak-areas.yaml`

## Full Loop Placement

| Company pattern | Where this mock fits |
|-----------------|---------------------|
| Google (coding confirmed) | Round 2 or 3 of onsite |
| Others (optional coding) | Insurance mock — one session before travel |

## Related

- [Mock Interviews Overview](/docs/mock-interviews/overview)
- [Design-Adjacent Problems](/docs/coding-preparation/design-adjacent-problems)
- [Practice Routine](/docs/coding-preparation/practice-routine)
