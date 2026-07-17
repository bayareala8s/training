# Lesson 5.1 — Cloud Strategy and Adoption Posture

**Module:** 05 — Cloud and Platform Strategy  
**Duration:** ~20 minutes (live portion)  
**Learning objectives:** M5-LO1, M5-LO5

---

## Opening hook (NorthStar)

NorthStar’s CIO announces: “We’re going all-in on cloud.” Business units hear permission to open accounts and migrate anything that burns. Within six months, NorthStar has **account sprawl**, inconsistent identity, and no shared logging. Cost rises while delivery barely improves.

Your job as Lead Enterprise Architect: turn “cloud” from a slogan into a **strategy with posture, principles, and placement rules**.

> Fiction notice: NorthStar Financial Services is fictional and used for BayLearn instruction only.

---

## Learning outcomes for this lesson

By the end of this lesson, students can:

1. Distinguish cloud posture options (hybrid, primary provider, multi-cloud) for a financial-services enterprise.
2. Write adoption principles that constrain local optimization without freezing delivery.

---

## Key concepts

### Cloud strategy vs. cloud migration plan

A **strategy** answers: Why cloud? Which workloads? Under what constraints? Who owns shared capabilities?  
A **migration plan** answers: In what order do we move specific systems?

Enterprises that skip strategy get migrations without platforms—and platforms without customers.

### Adoption posture

| Posture | Meaning | NorthStar fit |
| ------- | ------- | ------------- |
| Hybrid by design | Keep regulated or latency-sensitive systems on-prem while cloud hosts digital products | Likely near-term reality |
| Cloud-first | Default to cloud unless exception | Target for new products |
| Multi-cloud active-active | Run same critical workloads on multiple clouds | High cost/complexity; rarely justified early |
| Multi-cloud for concentration risk | Primary provider + exit options / selective secondary | Executive risk conversation |

### Workload placement principles

Place workloads using explicit criteria: data classification, latency, resilience needs, team skills, total cost, and regulatory evidence requirements—not fashion.

---

## Framework / model

```text
Business drivers → Cloud posture → Principles → Placement rules → Platform capabilities → Guardrails/FinOps
```

---

## Enterprise example (NorthStar)

Drivers: 20% cost reduction, faster digital products, standardized cloud adoption, stronger compliance posture.

Recommended teaching posture for this cohort: **cloud-first for new digital products; hybrid coexistence for acquired cores; single primary provider with documented exit criteria**—not active-active multi-cloud in year one.

---

## Trade-offs

| Option | Pros | Cons | When it fits |
| ------ | ---- | ---- | ------------ |
| Cloud-first, single provider | Speed, skill focus, platform leverage | Concentration risk | Most product teams for next 24 months |
| Aggressive multi-cloud | Negotiation leverage, some resilience narrative | Duplicate platforms, thin skills | Rare; selective services only |
| Lift-and-shift everything | Fast “progress” optics | Cost + fragility | Almost never as default |

---

## Common mistakes

- Equating “we have accounts” with “we have a landing zone”
- Declaring multi-cloud without multi-platform funding
- Migrating before identity, logging, and FinOps baselines exist

---

## Discussion prompts

1. Which NorthStar business driver most strongly argues *against* active-active multi-cloud in year one?
2. What evidence would make you approve an exception to cloud-first for a payments core system?

---

## Diagram (Mermaid)

```mermaid
flowchart LR
  D[Business drivers] --> P[Cloud posture]
  P --> PR[Principles]
  PR --> W[Workload placement]
  W --> PL[Platform capabilities]
  PL --> G[Guardrails and FinOps]
```

---

## Transition to next lesson / lab

Next we design the **landing zone and platform capability map**—the shared foundation that makes cloud-first safe.

---

## References for instructors (non-proprietary)

- AWS Well-Architected concepts at overview level (no proprietary claims)
- Course content standards and NorthStar baseline
