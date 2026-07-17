# Lesson 3.1 — Discovery

**Module:** 03 — Current-State Architecture Assessment  
**Duration:** ~20 minutes (live portion)  
**Learning objectives:** MLO-3.1

---

## Opening hook (NorthStar)

NorthStar has “300+ applications with unclear ownership.” A junior analyst proposes a six-month CMDB cleanse before any architecture decisions. Meanwhile ExCo wants risk visibility this quarter. Discovery is a design problem: how much confidence do you need for which decisions, by when, and whose time will you consume to get it?

---

## Learning outcomes for this lesson

By the end of this lesson, students can:

1. Choose a scoped discovery strategy matched to decision urgency.
2. Select evidence sources and confidence levels appropriate to architecture recommendations.

---

## Key concepts

### Decision-driven discovery

Start from the decision: TIME dispositions for high-cost duplicates? Top-10 risk briefing? Roadmap wave 1 candidates? Each needs different depth.

### Discovery modes

| Mode | Speed | Confidence | Typical use |
| ---- | ----- | ---------- | ----------- |
| Artifact harvest | Fast | Low–Med | Inventories, diagrams, contracts, tickets |
| Stakeholder interviews | Medium | Med | Ownership, pain, shadow IT |
| Technical probes | Slower | Med–High | Dependency scans, vulnerability data, cost |
| Deep assessment | Slow | High | Mission-critical transformation design |

### Anti-patterns

- Inventory vanity (collecting forever)
- Single-source trust (one LOB spreadsheet)
- Discovery as delay tactic (“we can’t decide until perfect data”)

---

## Framework / model

**Discovery canvas**

```text
Decision needed → Scope slice → Evidence sources → Confidence target → Timebox → Output artifact
```

NorthStar Module 03 default slice: use the fictional 45-app sample CSV as a **teaching portfolio**, scoped further by capability themes from Module 02 (e.g., Customer Onboarding, Integration, Identity, Payments duplicates).

---

## Enterprise example (NorthStar)

For an ExCo risk briefing in three weeks:

- Scope: Mission Critical + High criticality apps in Customer, Payments, Identity, Integration
- Sources: inventory CSV, known incident themes, Module 02 frictions, CISO qualitative input
- Confidence: Medium acceptable if assumptions listed
- Output: TIME summary + top-10 risks—not a full CMDB

---

## Trade-offs

| Option | Pros | Cons | When it fits |
| ------ | ---- | ---- | ------------ |
| Broad shallow discovery | Coverage | Weak decisions | Early orientation |
| Narrow deep discovery | Actionable | Blind spots | Wave-1 design |
| Iterative discovery waves | Balances both | Needs discipline | NorthStar default |

---

## Common mistakes

- Waiting for perfect ownership data before scoring anything.
- Interviewing only technologists (miss business criticality).
- Treating the CSV Recommended disposition as final truth.

---

## Discussion prompts

1. What discovery confidence is “good enough” for Eliminate vs. Invest recommendations?
2. How do you prevent discovery from becoming a political weapon to delay consolidation?

---

## Diagram (Mermaid)

```mermaid
flowchart LR
  D[Decision] --> S[Scope slice]
  S --> E[Evidence]
  E --> C[Confidence]
  C --> A[Architecture artifact]
  A --> N[Next discovery wave]
```

---

## Transition to next lesson / lab

Lesson 3.2 applies TIME as the portfolio language once a scoped inventory exists.

---

## References for instructors (non-proprietary)

- Application portfolio management concepts (industry-standard)
- Course content standards and NorthStar baseline
