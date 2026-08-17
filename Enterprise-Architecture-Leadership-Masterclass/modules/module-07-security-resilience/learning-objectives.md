# Learning Objectives — Module 07

**Module:** Security, Risk, Compliance, and Resilience  
**Course outcomes mapped:** LO 19, 20, 21 (see `course-specification/learning-outcomes.md`)  
**Case study:** NorthStar Financial Services (fictional)

---

## Module-level objectives

By the end of Module 07, students will be able to:

| ID | Objective | Bloom | Primary lesson | Lab evidence |
| -- | -------- | ----- | -------------- | ------------ |
| M07-LO1 | Apply Zero Trust principles and draw trust boundaries for a NorthStar platform slice | Apply | 7.1 | Trust-boundary diagram |
| M07-LO2 | Perform lightweight STRIDE threat modeling and prioritize residual risks | Analyze | 7.2 | Completed threat model |
| M07-LO3 | Define RTO/RPO targets and validate recovery using versioning, encryption, and DR simulation | Evaluate | 7.3 | RTO/RPO worksheet + recovery test |
| M07-LO4 | Map controls to AWS implementations and produce a control-evidence matrix suitable for audit conversation | Create | 7.4 | Control-evidence matrix |

---

## Lesson-level outcomes

### Lesson 7.1 — Zero Trust and Trust Boundaries

- Explain Zero Trust as continuous verification, least privilege, and assume-breach—not “no VPN ever.”
- Identify trust boundaries across identity, network (logical), application, and data planes.
- Recommend least-privilege IAM patterns for lab and production analogues.

### Lesson 7.2 — Threat Modeling with STRIDE

- Scope a threat model to a bounded system (payment-file landing zone / digital platform slice).
- Map STRIDE categories to concrete abuse cases for NorthStar.
- Distinguish preventive, detective, and corrective controls.

### Lesson 7.3 — Resilience, RTO/RPO, and DR

- Define RTO and RPO in business language and link them to tiered workloads.
- Compare recovery options: backups/versioning, multi-AZ, cross-region replication, and runbooks.
- Design a failure/recovery test that produces measurable evidence without expensive always-on DR.

### Lesson 7.4 — Compliance Evidence and Leadership

- Connect architecture controls to evidence artifacts (configs, logs, alarms, tickets).
- Brief executives on residual risk without fear-mongering or false certainty.
- Negotiate exceptions with time-bound compensating controls.

---

## Success criteria (observable)

Students succeed when their lab pack:

1. Names data classifications and owners for at least three asset types.
2. Shows at least one diagrammed trust boundary change with a matching IAM or encryption control.
3. Includes a STRIDE table with ≥6 rows and prioritized top risks.
4. States RTO/RPO with justification and shows recovery-test evidence.
5. Lists ≥5 controls with evidence location (bucket policy, KMS key policy, alarm ARN, etc.).
