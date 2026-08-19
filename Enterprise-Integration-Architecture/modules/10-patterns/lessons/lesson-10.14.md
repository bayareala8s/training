# Lesson 10.14 — Retry

**Module:** 10 — Enterprise Integration Patterns  
**Duration:** 25–35 minutes  
**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.

---

## Learning outcomes

By the end of this lesson you will be able to:

1. Explain the problem Retry solves.
2. Draw a vendor-neutral architecture for the pattern.
3. Choose when not to use it and map a sensible AWS example.

---

## Enterprise scenario

Harbor/Northbridge incident: Transient faults should not fail the business operation.

> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, CareMesh Health, Atlas Manufacturing) are instructional fictions.

---

## WHY this exists

Retry exists because Transient faults should not fail the business operation. The pattern is a known, named response so architects can debate tradeoffs instead of inventing folklore. 

---

## WHEN an Enterprise Architect uses it

- Network blips, 429, 503.

### When NOT to use it

- Poison schema; unbounded retry; retrying non-idempotent posts without keys.

### Integration characteristics to inspect

- Problem presence
- Cost of the pattern
- Ops skill

---

## HOW — the pattern (vendor-neutral)

**Pattern:** Retry. Structure the design so the problem cannot recur silently. Include failure behavior in the diagram. Teach the pattern in reviews by name so teams share vocabulary.

### Architecture diagram

```mermaid
flowchart LR
  P[Problem] --> Pat[Pattern: Retry]
  Pat --> Out[Controlled outcome]
```

---

## HOW — AWS implementation (after the pattern)

**AWS example (after the pattern):** SDK retries + SQS redrive + backoff/jitter (Module 11). Count them.

Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.

---

## Anti-patterns

- Using Retry as decoration without the problem present.
- Renaming the pattern every project.

---

## Tradeoffs

| Dimension | Benefit | Cost / risk |
|-----------|---------|-------------|
| Apply pattern | Known failure modes | Over-engineering if the problem is absent |
| Ignore | Faster demo | Recurring incident class |

---

## Architecture decision prompt

How many total attempts exist if SDK, Lambda, and SQS all retry?

Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.

---

## Knowledge check

**Q1.** In one sentence, what problem does Retry solve?

*Answer.* Transient faults should not fail the business operation.

---

## Architect's note

Every pattern in this module must appear in at least one capstone ADR by name.

---

## Next

Complete any architecture challenge attached to this lesson in the course player. Record an ADR fragment if the decision would survive a design review.
