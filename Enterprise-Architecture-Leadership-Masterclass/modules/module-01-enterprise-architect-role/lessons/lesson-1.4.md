# Lesson 1.4 — Architecture Leadership Assessment

**Module:** 01 — The Enterprise Architect’s Role  
**Duration:** ~15 minutes (live portion) + reflection in workbook/lab  
**Learning objectives:** M01-LO4

---

## Opening hook (NorthStar)

You have a title: Lead Enterprise Architect. You do **not** have line authority over Retail’s architects, Payments engineering managers, or the Partner Channels product org. The CISO will not “report into architecture.” The CEO cares about cost, growth, and risk visibility—not your framework purity.

If your operating model depends on people obeying you because of your title, it will fail at NorthStar.

> **Fiction notice:** NorthStar Financial Services is fictional.

---

## Learning outcomes for this lesson

By the end of this lesson, students can:

1. Assess sources of influence available to a Lead EA and diagnose organizational readiness for architecture change.
2. Prescribe a credible first-90-day leadership plan that builds coalition and decision discipline without over-centralizing.

---

## Key concepts

### Influence without authority (practical sources)

| Influence source | What it looks like | How to grow it at NorthStar |
| ---------------- | ------------------ | --------------------------- |
| Expertise | Pattern judgment; clear trade-off framing | Publish short decision memos; coach ADRs |
| Network | Trusted relationships across BUs | 1:1s with every BU architect in 30 days |
| Process design | Decision rights people actually use | Make engagement faster than chaos |
| Executive sponsorship | CIO covers you when contested | Weekly risk digest the CIO wants to forward |
| Delivery credibility | Helped a team ship safely faster | Pick one painful golden-path win |
| Evidence | Data on duplicate cost / risk | Partner with FinOps and Risk for facts |

**Anti-pattern:** Leading with governance ceremonies before any credibility deposit.

### Organizational readiness snapshot

Score each 1–4 (1 = hostile / absent, 4 = strong):

| Dimension | Probe question |
| --------- | -------------- |
| Executive sponsorship | Will the CIO defend a material ARB decision? |
| BU architect coalition | Do federated architects see EA as ally or auditor? |
| Delivery pressure honesty | Are timelines negotiable when risk is material? |
| Risk culture | Is late security engagement punished or normalized? |
| Platform maturity | Do golden paths exist or only PowerPoint platforms? |
| Decision hygiene | Are major bets written down (ADR / memo)? |

Low sponsorship + low platform maturity → **do not** launch a heavy ARB. Build principles, decision classes, and one visible win first.

### First 90 days (NorthStar Lead EA)

| Days | Leadership move | Artifact |
| ---- | --------------- | -------- |
| 0–30 | Listen tour: BU architects, CISO delegate, Platform, Data, two engineering managers | Stakeholder map; problem themes |
| 0–30 | Draft mission + hybrid operating model option | Lab pack v0.9 |
| 30–60 | Socialize principles (8–10) and exception path | Principles v1 for CIO review |
| 30–60 | Define ARB *triggers* only (not full ceremony yet) | Engagement model |
| 60–90 | Land one cross-BU decision with recorded trade-offs | ADR + executive one-pager |
| 60–90 | Publish architecture-function risk register | Risks to the operating model itself |

### Personal leadership assessment (student)

Rate yourself 1–4 on:

1. Framing decisions in business outcomes  
2. Holding tension without forcing false certainty  
3. Writing for executives (one page, decision-ready)  
4. Facilitating conflict across peers  
5. Knowing when to consult vs. escalate  
6. Comfort saying “I don’t know—here’s how we’ll learn”

Pick the **lowest two** scores as Module 01 workbook development goals. Capstone later requires a personal leadership plan (`student/templates/15-personal-leadership-plan.md`).

---

## Framework / model

**Credibility before control:**

```text
Listen → Shared problem framing → Lightweight principles
    → One useful decision → Visible risk reporting
    → Expand decision rights / ARB scope
```

Skip ahead to “control” and NorthStar will route around you.

---

## Enterprise example (NorthStar)

**Scenario:** Wealth’s architect announces a new CRM platform decision in a town hall—contracts nearly signed. You were not consulted.

| Response | Likely effect |
| -------- | ------------- |
| Public veto attempt | You lose; branded as blocker |
| Silent acceptance | EA irrelevant |
| Influence play | Private 1:1 with Wealth + CIO: map decision class, quantify integration/identity risk, offer time-boxed path with ARB only if thresholds met, document alternatives |

Leadership is the third path: **change the decision quality**, not just the winner.

---

## Trade-offs

| Leadership posture | Pros | Cons | When it fits |
| ------------------ | ---- | ---- | ------------ |
| Servant facilitator | High trust | May under-govern material risk | Early listening phase |
| Benevolent governor | Clear boundaries | Resistance; bypass | Only with sponsorship + golden paths |
| Coalition builder | Sustainable in federated orgs | Slower initial consistency | **Default for NorthStar Year 1** |
| Hero designer | Short-term quality | Does not scale; succession risk | Emergency only |

---

## Common mistakes

- Confusing activity (meetings, frameworks) with influence (changed decisions).
- Trying to win every disagreement in Week 1.
- Ignoring BU architects’ political capital.
- Publishing an operating model nobody co-authored, then being surprised by rejection.

---

## Discussion prompts

1. What is one architecture decision you influenced without authority in your career—and which influence source did the work?
2. If your NorthStar readiness scores are mostly 2s, what is the *smallest* viable governance increment you would still defend to the CIO?

---

## Diagram (Mermaid)

```mermaid
quadrantChart
    title Influence posture for NorthStar Lead EA
    x-axis Low formal authority --> High formal authority
    y-axis Low credibility --> High credibility
    quadrant-1 Expand decision rights carefully
    quadrant-2 Sustain hybrid model
    quadrant-3 Listen and earn wins
    quadrant-4 Avoid: control without trust
    Lead EA Year1: [0.35, 0.40]
    Target Year2: [0.55, 0.70]
```

---

## Transition to next lesson / lab

You now have the conceptual stack: what EA is, how it operates, which principles constrain decisions, and how leadership makes it real. Lab 01 asks you to produce the operating-model pack for NorthStar.

---

## References for instructors (non-proprietary)

- Facilitation principle: challenge ideas, not people
- Keep fiction notice when discussing “your employer” parallels
- Tie personal scores to workbook; do not grade personality
