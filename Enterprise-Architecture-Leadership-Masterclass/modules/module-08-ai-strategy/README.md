# Module 08 — AI Strategy and Intelligent Enterprise Architecture

**Week:** 8  
**Duration:** 2-hour live session + lab/assignment  
**Case study:** NorthStar Financial Services (fictional)  
**Student role:** Lead Enterprise Architect  
**Slug:** `module-08-ai-strategy`

> **Fiction notice:** NorthStar Financial Services is a fictional organization created for BayLearn instructional use. It is not affiliated with any real company.

---

## Module objective

Design a governed enterprise AI capability for NorthStar—selecting use cases with explicit criteria, architecting an incident decision assistant with structured outputs, validation, human-in-the-loop (HITL), safe logging, and cost/token tracking—and evaluate quality with a labeled dataset.

---

## Learning objectives

Students will be able to:

1. Score AI use cases for value, feasibility, data readiness, risk, and operability.
2. Design a governed AI architecture (Bedrock or mock fallback) with structured JSON outputs and validation.
3. Implement HITL routing, safe logging, and token/cost tracking for operational decisions.
4. Build a small evaluation dataset and define a quality measure for assistant outputs.

Full detail: [`learning-objectives.md`](learning-objectives.md)

---

## Prerequisites

See [`prerequisites.md`](prerequisites.md). Module 07 security/resilience mindset is assumed. AWS account may need **Bedrock model access**—lab includes a **mock/fallback mode** if Bedrock is not enabled.

---

## Lessons

| ID | Title | Est. focus |
| -- | ----- | ---------- |
| 8.1 | Enterprise AI Strategy and Use-Case Selection | Concept |
| 8.2 | Governed AI Architecture Patterns | Concept |
| 8.3 | HITL, Evaluation, and Operating Model | Concept |
| 8.4 | Cost, Risk, and Architecture Leadership for AI | Application / leadership |

---

## Lab

**Build NorthStar’s Governed AI Decision Assistant**  
Student instructions: [`../../../labs/lab-08-ai-decision-assistant/student-instructions.md`](../../../labs/lab-08-ai-decision-assistant/student-instructions.md)

### Deliverables

- AI use-case scorecard for the incident assistant
- Architecture diagram + structured prompt / JSON schema notes
- Working invoke path (Bedrock **or** mock mode) with validation + HITL routing evidence
- Evaluation dataset results + quality measure write-up + cost/token notes

---

## Assignment

[`../../../assessments/assignments/module-08-assignment.md`](../../../assessments/assignments/module-08-assignment.md)

## Quiz

[`../../../assessments/quizzes/module-08-quiz.md`](../../../assessments/quizzes/module-08-quiz.md)

## Slides

[`../../../slides/module-08/slide-outline.md`](../../../slides/module-08/slide-outline.md)

---

## Instructor package

Instructor-only materials live under `instructor/`. Do not distribute reference solutions or answer keys to students.

| Asset | Path |
| ----- | ---- |
| Instructor guide | [`../../instructor/guides/module-08/instructor-guide.md`](../../instructor/guides/module-08/instructor-guide.md) |
| Speaking script | [`../../instructor/scripts/module-08/speaking-script.md`](../../instructor/scripts/module-08/speaking-script.md) |
| Reference solution | [`../../instructor/reference-solutions/module-08/`](../../instructor/reference-solutions/module-08/) |
| Grading guide | [`../../instructor/grading/module-08-grading-guide.md`](../../instructor/grading/module-08-grading-guide.md) |

---

## Capstone contribution

This module’s artifacts feed the capstone as:

- AI use-case scorecard and governance checklist
- Governed AI reference architecture for incident decisions
- Evaluation approach and HITL policy notes

---

## Related templates

- [`../../student/templates/12-ai-use-case-scorecard.md`](../../student/templates/12-ai-use-case-scorecard.md)
- [`../../student/templates/19-ai-governance-checklist.md`](../../student/templates/19-ai-governance-checklist.md)
- [`../../student/templates/01-architecture-decision-record.md`](../../student/templates/01-architecture-decision-record.md)

---

## AWS / infrastructure

| Asset | Path |
| ----- | ---- |
| Terraform module | `infrastructure/terraform/modules/ai-decision-assistant/` |
| Lab environment | `infrastructure/terraform/environments/lab08/` |
| Cleanup script | `infrastructure/terraform/scripts/cleanup-lab08.sh` |
| Cost estimate | `infrastructure/cost-estimates/lab-08.md` |
| Evaluation dataset | `labs/lab-08-ai-decision-assistant/datasets/incident-eval-set.csv` |

**Bedrock note:** If model access is not enabled in your account, set `use_mock_bedrock = true` (default-safe). The lab still teaches architecture, validation, HITL, and evaluation.

**Cost warning:** Bedrock token usage and API Gateway/Lambda are usually small at lab scale—still set a budget alert and run cleanup after class.
