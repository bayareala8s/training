# Module 07 — Security, Risk, Compliance, and Resilience

**Week:** 7  
**Duration:** 2-hour live session + lab/assignment  
**Case study:** NorthStar Financial Services (fictional)  
**Student role:** Lead Enterprise Architect  
**Slug:** `module-07-security-resilience`

> **Fiction notice:** NorthStar Financial Services is a fictional organization created for BayLearn instructional use. It is not affiliated with any real company.

---

## Module objective

Treat security, risk, compliance, and resilience as first-class architecture concerns for NorthStar’s digital platform—design Zero Trust boundaries, perform lightweight STRIDE threat modeling, define measurable RTO/RPO targets, and produce control-evidence artifacts executives and auditors can consume.

---

## Learning objectives

Students will be able to:

1. Apply Zero Trust principles and trust-boundary design to a NorthStar platform slice.
2. Perform lightweight STRIDE threat modeling and map threats to controls and evidence.
3. Define RTO/RPO targets and validate a low-cost recovery approach (versioning, encryption, replication or simulated DR).
4. Produce a control-evidence matrix linking risks, controls, AWS implementations, and audit artifacts.

Full detail: [`learning-objectives.md`](learning-objectives.md)

---

## Prerequisites

See [`prerequisites.md`](prerequisites.md). Modules 05–06 (cloud platform and integration patterns) are assumed complete or reviewed via summary packs. AWS CLI + Terraform required for the lab.

---

## Lessons

| ID | Title | Est. focus |
| -- | ----- | ---------- |
| 7.1 | Zero Trust and Trust Boundaries | Concept |
| 7.2 | Threat Modeling with STRIDE | Concept |
| 7.3 | Resilience, RTO/RPO, and Disaster Recovery | Concept |
| 7.4 | Compliance Evidence and Architecture Leadership | Application / leadership |

---

## Lab

**Secure and Resilient NorthStar’s Digital Platform**  
Student instructions: [`../../../labs/lab-07-security-resilience/student-instructions.md`](../../../labs/lab-07-security-resilience/student-instructions.md)

### Deliverables

- Data classification + trust-boundary diagram for the lab platform slice
- STRIDE threat model with prioritized risks and controls
- RTO/RPO worksheet + failure/recovery test evidence
- Control-evidence matrix mapped to deployed AWS controls

---

## Assignment

[`../../../assessments/assignments/module-07-assignment.md`](../../../assessments/assignments/module-07-assignment.md)

## Quiz

[`../../../assessments/quizzes/module-07-quiz.md`](../../../assessments/quizzes/module-07-quiz.md)

## Slides

[`../../../slides/module-07/slide-outline.md`](../../../slides/module-07/slide-outline.md)

---

## Instructor package

Instructor-only materials live under `instructor/`. Do not distribute reference solutions or answer keys to students.

| Asset | Path |
| ----- | ---- |
| Instructor guide | [`../../instructor/guides/module-07/instructor-guide.md`](../../instructor/guides/module-07/instructor-guide.md) |
| Speaking script | [`../../instructor/scripts/module-07/speaking-script.md`](../../instructor/scripts/module-07/speaking-script.md) |
| Reference solution | [`../../instructor/reference-solutions/module-07/`](../../instructor/reference-solutions/module-07/) |
| Grading guide | [`../../instructor/grading/module-07-grading-guide.md`](../../instructor/grading/module-07-grading-guide.md) |

---

## Capstone contribution

This module’s artifacts feed the capstone as:

- Threat model for a priority platform
- RTO/RPO and resilience targets
- Risk-control / control-evidence matrix

---

## Related templates

- [`../../student/templates/10-threat-model.md`](../../student/templates/10-threat-model.md)
- [`../../student/templates/11-rto-rpo-worksheet.md`](../../student/templates/11-rto-rpo-worksheet.md)
- [`../../student/templates/18-risk-control-matrix.md`](../../student/templates/18-risk-control-matrix.md)
- [`../../student/templates/01-architecture-decision-record.md`](../../student/templates/01-architecture-decision-record.md)

---

## AWS / infrastructure

| Asset | Path |
| ----- | ---- |
| Terraform module | `infrastructure/terraform/modules/security-resilience/` |
| Lab environment | `infrastructure/terraform/environments/lab07/` |
| Cleanup script | `infrastructure/terraform/scripts/cleanup-lab07.sh` |
| Cost estimate | `infrastructure/cost-estimates/lab-07.md` |

**Cost warning:** Keep the lab ephemeral. Target cost is typically under a few USD when cleaned up the same day. Do not leave replication or alarms running overnight without a budget alert.
