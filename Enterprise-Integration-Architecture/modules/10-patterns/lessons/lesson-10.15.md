# Lesson 10.15 — Dead Letter Queue

**Module:** 10 — Enterprise Integration Patterns  
**Duration:** 25–35 minutes  
**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.

---

## Learning outcomes

By the end of this lesson you will be able to:

1. Explain the problem Dead Letter Queue solves.
2. Draw a vendor-neutral architecture for the pattern.
3. Choose when not to use it and map a sensible AWS example.

---

## Enterprise scenario

Harbor/Northbridge incident: Poison or exhausted messages must not block or vanish.

> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, CareMesh Health, Atlas Manufacturing) are instructional fictions.

---

## WHY this exists

Dead Letter Queue exists because Poison or exhausted messages must not block or vanish. The pattern is a known, named response so architects can debate tradeoffs instead of inventing folklore. 

---

## WHEN an Enterprise Architect uses it

- After max attempts; operator inspect and replay.

### When NOT to use it

- DLQ as trash; no alarms; purge to green.

### Integration characteristics to inspect

- Problem presence
- Cost of the pattern
- Ops skill

---

## HOW — the pattern (vendor-neutral)

**Pattern:** Dead Letter Queue. Structure the design so the problem cannot recur silently. Include failure behavior in the diagram. Teach the pattern in reviews by name so teams share vocabulary.

### Architecture diagram

```mermaid
flowchart LR
  P[Problem] --> Pat[Pattern: Dead Letter Queue]
  Pat --> Out[Controlled outcome]
```

---

## HOW — AWS implementation (after the pattern)

**AWS example (after the pattern):** SQS redrive; Lambda destinations; EventBridge DLQ.

Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.

---

## Anti-patterns

- Using Dead Letter Queue as decoration without the problem present.
- Renaming the pattern every project.

---

## Tradeoffs

| Dimension | Benefit | Cost / risk |
|-----------|---------|-------------|
| Apply pattern | Known failure modes | Over-engineering if the problem is absent |
| Ignore | Faster demo | Recurring incident class |

---

## Architecture decision prompt

What are inspect, fix, replay, and who is paged?

Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.

---

## Knowledge check

**Q1.** In one sentence, what problem does Dead Letter Queue solve?

*Answer.* Poison or exhausted messages must not block or vanish.

---

## Architect's note

Every pattern in this module must appear in at least one capstone ADR by name.

---

## Next

Complete any architecture challenge attached to this lesson in the course player. Record an ADR fragment if the decision would survive a design review.
