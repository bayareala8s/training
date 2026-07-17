# ARB Simulation Pack — Lab 09

**Classification:** Student-facing facilitation aid  
**Case study:** NorthStar Financial Services (fictional)

---

## 1. Roles (assign one primary role per student; pairs share a role in large cohorts)

| Role | Badge focus | Must challenge |
| ---- | ----------- | -------------- |
| Lead EA | Principles, precedent, disposition quality | Enterprise alignment; decision packaging |
| Security architect | Identity, privilege, audit, data protection | Contractor access; logging; keys |
| Business sponsor | Outcomes, timing, residual risk appetite | Whether date justifies irreversible tax |
| Platform lead | Golden paths, operability, FinOps | Second cloud; custom framework ops |
| Data architect | SoR, coupling, residency, golden record | VectorForge as SoR for KYC |
| Delivery architect | Feasibility, skills, sequencing | Realistic path to date with standards |

Optional observer: CIO (instructor) — asks one killer question at the end.

---

## 2. Pre-work (30–45 minutes before live board)

1. Read [`proposal-pack.md`](proposal-pack.md) end-to-end.  
2. Complete the architecture review checklist (`student/templates/13-architecture-review-checklist.md`).  
3. Write 3 role-specific challenge questions.  
4. Draft a preliminary disposition for each of the four decision requests.

---

## 3. Live agenda (45 minutes)

| Min | Activity | Owner |
| --- | -------- | ----- |
| 0–5 | Conflict check; confirm disposition vocabulary | Lead EA |
| 5–15 | Proposer walkthrough (instructor or volunteer) | Proposer |
| 15–30 | Round-robin challenge (2–3 min per role) | All |
| 30–40 | Options & conditions synthesis | Lead EA |
| 40–45 | Disposition vote + ADR/memo owners | Lead EA |

---

## 4. Challenge cards (starter prompts)

**Security**

- What is the least-privilege alternative to standing cluster-admin?
- Where are secrets stored, rotated, and monitored?
- How will SIEM coverage match enterprise retention?

**Platform**

- What shared services are duplicated on CloudNova in Year-1?
- What is the dual-running ops cost vs. landing-zone acceleration?
- Who supports PayWireFX at 2 a.m.?

**Data**

- What becomes the golden record for merchant identity?
- How do we exit VectorForge if benchmarks were wrong?
- Which analytics/regulatory extracts break?

**Delivery**

- What is the critical path if we stay on the primary cloud?
- Which scope can slip without missing merchant NPS?
- What skills exist in-house for the proposed stack?

**Business sponsor**

- What residual risk is acceptable if we miss by 4 weeks vs. approve lock-in?
- Which committed spend is sunk vs. stoppable?

**Lead EA**

- What precedent do we set for the next BU?
- Are we deciding one thing or four? Split the ADRs.

---

## 5. Disposition scorecard (per decision request)

| Request | Approve | Approve w/ conditions | Defer | Reject | Conditions / evidence needed |
| ------- | ------- | --------------------- | ----- | ------ | ---------------------------- |
| Second cloud | | | | | |
| VectorForge SoR | | | | | |
| PayWireFX framework | | | | | |
| Contractor prod access | | | | | |

---

## 6. Participation rubric cues (10% course weight component)

Graders look for:

- Preparation (checklist + questions ready)
- Role fidelity (not generic debate)
- Constructive challenge (options, not only objections)
- Decision quality (testable conditions, clear disposition)

---

## 7. Output owners (default)

| Artifact | Owner |
| -------- | ----- |
| Executive decision memo | Lead EA (each student submits individually) |
| ADR-A cloud hosting | Lead EA + Platform |
| ADR-B data store | Data + Security |
| Optional ADR-C access | Security + Delivery |
