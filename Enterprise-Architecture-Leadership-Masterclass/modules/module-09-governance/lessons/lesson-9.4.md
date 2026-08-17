# Lesson 9.4 — Executive Communication and Decision Memos

**Module:** 09 — Architecture Governance and Executive Communication  
**Duration:** ~20 minutes (live portion)  
**Learning objectives:** M9-LO4

---

## Opening hook (NorthStar)

The CIO has twelve minutes between audit committee prep and a partner escalation. She will not open your architecture diagram pack. She will open a **one- to two-page memo** that states: what you recommend, why it matters in business terms, what it costs/risks, and what decision you need today.

---

## Learning outcomes for this lesson

By the end of this lesson, students can:

1. Structure an executive decision memo with clear ask, options, and residual risk.
2. Translate technical architecture consequences into cost, speed, risk, and customer impact language.

---

## Key concepts

### Memo vs. ADR vs. slides

| Artifact | Audience | Job |
| -------- | -------- | --- |
| ADR | Architects / auditors / future teams | Durable decision trail |
| Decision memo | Executives / sponsors | Decision in business language |
| Slides | Live presentation | Narrative + visual hierarchy |

Never make executives reverse-engineer the ask from a diagram.

### Executive memo spine

1. **Decision requested** (one sentence)
2. **Context** (why now)
3. **Options** (2–3, including status quo)
4. **Recommendation** and why
5. **Impacts** — cost, timeline, risk, customer/partner
6. **Conditions / controls** if approving a variant
7. **Ask** — approve / fund / escalate / stop

### Language swaps

| Avoid | Prefer |
| ----- | ------ |
| “Non-functional requirements” | Reliability, security, auditability targets |
| “Technical debt” alone | Run-cost, change-failure, concentration risk |
| “Best practice cloud” | Shared landing zone reduces account sprawl and audit gaps |
| “Block the team” | Propose a path that meets the date with lower enterprise tax |

---

## Framework / model

```text
Ask → Why now → Options → Recommend → Impacts → Controls → Decision
```

---

## Enterprise example (NorthStar)

**Weak:** “We should reject multi-cloud because it increases complexity.”

**Strong:** “Recommend reject Retail Payments’ second-cloud proposal. Approving creates a parallel operating model (identity, logging, DR, FinOps) estimated at $1.2–1.8M annual run uplift and weakens our audit evidence path. Offer accelerated landing-zone onboarding and a 90-day exception only for legally required sovereignty—not for team preference.”

---

## Trade-offs

| Option | Pros | Cons | When it fits |
| ------ | ---- | ---- | ------------ |
| One-page memo | Forces clarity | May oversimplify | Most ARB outcomes |
| Memo + appendix ADRs | Exec + trail | Slightly more work | Tier 2 decisions |
| Deck-only | Familiar | Ask gets buried | Avoid as sole artifact |

---

## Common mistakes

- Hiding the recommendation in paragraph four
- Offering only one option (“approve my plan”)
- Using fear without a feasible alternative path for the BU

---

## Discussion prompts

1. How do you communicate “no” while preserving sponsor trust?
2. What three numbers would you bring to the CIO for this ARB outcome?

---

## Diagram (Mermaid)

```mermaid
flowchart LR
  A[Technical findings] --> B[Business consequences]
  B --> C[Options in exec language]
  C --> D[Clear ask]
  D --> E[Decision + owners]
```

---

## Transition to next lesson / lab

Lab 09: run the ARB on the divergent proposal pack, then produce the memo and ADRs as if the CIO is waiting.

---

## References for instructors (non-proprietary)

- Executive decision memo template `student/templates/02-executive-decision-memo.md`
- Course communication standards
