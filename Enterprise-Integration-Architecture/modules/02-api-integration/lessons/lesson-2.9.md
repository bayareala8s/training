# Lesson 2.9 — Rate Limiting

**Module:** 02 — API-Based Integration  
**Duration:** 25–35 minutes  
**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.

---

## Learning outcomes

By the end of this lesson you will be able to:

1. Use rate limits as a fairness and survival control, not as punishment after an outage.
2. Distinguish burst, steady-state, and per-principal throttles.
3. Plan client backoff and partner SLAs together.

---

## Enterprise scenario

A well-meaning partner replayed a day’s worth of payments at 8:00 on Monday. Northbridge’s API scaled until DynamoDB throttled and the mobile app died. Rate limits exist to keep one consumer from becoming a denier of service.

> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, CareMesh Health, Atlas Manufacturing) are instructional fictions.

---

## WHY this exists

Rate limiting protects shared capacity. It is an architecture control: you are allocating a scarce resource (downstream IOPS, fraud engine, human-equivalent process). Burst allows short spikes; steady-state protects the platform. Per-key limits implement fairness among partners. Global limits protect the bank.

---

## WHEN an Enterprise Architect uses it

- Any public or partner API.
- Any dependency with a hard TPS limit.
- When a retry storm is a realistic failure mode.

### When NOT to use it

- Do not set limits so low that legitimate onboarding fails without a quota product.
- Do not rate-limit without telling the client how to back off (429 + Retry-After).

---

## HOW — the pattern (vendor-neutral)

Publish quotas in the contract. Return 429 with a retry hint. Combine with idempotency so retries are safe. Consider token buckets per principal. For internal APIs, still limit—retry storms from your own microservices are common.

### Architecture diagram

```mermaid
flowchart LR
  P[Partners] --> RL[Per-key throttle]
  RL --> G[Global throttle]
  G --> API[API]
  API --> Dep[Weakest dependency]
```

---

## HOW — AWS implementation (after the pattern)

API Gateway usage plans and throttles, WAF rate rules, and service-level limiters. DynamoDB and downstream APIs have their own limits—the gateway limit should be **tighter** than the weakest dependency if you want graceful 429s instead of 500s.

Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.

---

## Anti-patterns

- Unlimited retries on 429.
- One global TPS for all partners regardless of contract.

---

## Tradeoffs

| Dimension | Benefit | Cost / risk |
|-----------|---------|-------------|
| Strict throttle | Protects the platform | Can stall a legitimate recovery replay |
| No throttle | Easy demo | First noisy neighbor wins |

---

## Architecture decision prompt

Partner A is allowed 10 TPS, Partner B 100 TPS. A shared unauthenticated limit would be wrong—why?

Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.

---

## Knowledge check

**Q1.** What should a client do on 429?

*Answer.* Back off, preferably with jitter, honor Retry-After, and retry only idempotent requests.

---

## Architect's note

Quotas are commercial and technical. Architects should sit with the partner manager.

---

## Next

Complete any architecture challenge attached to this lesson in the course player. Record an ADR fragment if the decision would survive a design review.
