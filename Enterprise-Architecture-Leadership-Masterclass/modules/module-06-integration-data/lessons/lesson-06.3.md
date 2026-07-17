# Lesson 6.3 — Data Products, Master Data, and Events

**Module:** 06  
**Duration:** ~20 minutes  
**Learning objectives:** M6-LO3

---

## Opening hook (NorthStar)

Three systems disagree on customer legal name. Analytics builds yet another copy from partner files. Payments emit events with a different account identifier format. Master data is not a committee—it is an **owned data product** with contracts.

---

## Learning outcomes

1. Define data product ownership for accounts and payments.
2. Distinguish master data, transactional events, and analytics/regulatory datasets.

---

## Key concepts

| Concept | Meaning |
| ------- | ------- |
| Data product | Owned dataset/API with consumers, SLA, quality metrics |
| Master data | Shared reference entities (e.g., Account) with golden sources |
| Transactional events | Facts about what happened |
| Analytical/regulatory batches | Curated outputs for reporting windows |

### Event design heuristics

- Past-tense names (`AccountCreated`, `PaymentSubmitted`)
- Stable identifiers
- Explicit versioning strategy
- Consumers tolerate eventual consistency where chosen

---

## Framework

```text
Source of truth → contracts → distribution pattern → consumer quality feedback
```

---

## Enterprise example

- **Account master:** Accounts domain via API + `AccountCreated` events  
- **Payment facts:** Payments domain events to bus/queue  
- **Partner file raw landing:** Partner domain; curated analytics batch owned with Data/Risk partners  

---

## Trade-offs

| Option | Pros | Cons | When it fits |
| ------ | ---- | ---- | ------------ |
| Single golden Account API | Clarity | Hotspot | Core customer journeys |
| Copy account fields into every event | Convenience | Drift | Anti-pattern if unbounded |
| File as master | Partner simplicity | Latency/quality issues | Rare; usually landing only |

---

## Common mistakes

- “Everyone can publish any JSON”
- Analytics becoming accidental master
- No PII handling rules on events/files

---

## Discussion prompts

1. Is the partner file ever allowed to update account master directly?
2. What quality metric proves the account data product is healthy?
