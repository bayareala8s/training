# Lesson 10.17 — Compensating Transaction

**Module:** 10 — Enterprise Integration Patterns  
**Duration:** 25–35 minutes  
**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.

---

## Learning outcomes

By the end of this lesson you will be able to:

1. Explain the problem Compensating Transaction solves.
2. Draw a vendor-neutral architecture for the pattern.
3. Choose when not to use it and map a sensible AWS example.

---

## Enterprise scenario

Harbor/Northbridge incident: A completed step must be undone when a later step fails.

> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, CareMesh Health, Atlas Manufacturing) are instructional fictions.

---

## WHY this exists

Compensating Transaction exists because A completed step must be undone when a later step fails. The pattern is a known, named response so architects can debate tradeoffs instead of inventing folklore. Compensation is not rollback of a local DB transaction; it is a new business action with its own contract.

---

## WHEN an Enterprise Architect uses it

- Saga undo: refund, release inventory, cancel shipment.

### When NOT to use it

- Compensation that is not idempotent; compensating what never happened; hoping DELETE is enough for money.

### Integration characteristics to inspect

- Problem presence
- Cost of the pattern
- Ops skill

---

## HOW — the pattern (vendor-neutral)

**Pattern:** Compensating Transaction. Structure the design so the problem cannot recur silently. Include failure behavior in the diagram. Teach the pattern in reviews by name so teams share vocabulary.

### Architecture diagram

```mermaid
flowchart LR
  P[Problem] --> Pat[Pattern: Compensating Transaction]
  Pat --> Out[Controlled outcome]
```

---

## HOW — AWS implementation (after the pattern)

**AWS example (after the pattern):** Explicit compensating APIs/commands from Step Functions catch blocks; events like InventoryReleased.

Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.

---

## Anti-patterns

- Using Compensating Transaction as decoration without the problem present.
- Renaming the pattern every project.

---

## Tradeoffs

| Dimension | Benefit | Cost / risk |
|-----------|---------|-------------|
| Apply pattern | Known failure modes | Over-engineering if the problem is absent |
| Ignore | Faster demo | Recurring incident class |

---

## Architecture decision prompt

Is compensation a refund API or a “negative quantity” event—and how do you audit it?

Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.

---

## Knowledge check

**Q1.** In one sentence, what problem does Compensating Transaction solve?

*Answer.* A completed step must be undone when a later step fails.

---

## Architect's note

Every pattern in this module must appear in at least one capstone ADR by name.

---

## Next

Complete any architecture challenge attached to this lesson in the course player. Record an ADR fragment if the decision would survive a design review.
