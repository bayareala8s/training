# Module 06 — Integration, Application, and Data Architecture

**Week:** 6  
**Duration:** 2-hour live session + AWS lab/assignment  
**Case study:** NorthStar Financial Services (fictional)  
**Student role:** Lead Enterprise Architect  
**Lab:** [Build NorthStar’s Integration Reference Architecture](../../labs/lab-06-integration-platform/student-instructions.md)

---

## Module objective

Select integration and data patterns for NorthStar’s real-time APIs, payment events, partner files, regulatory batches, analytics, and notifications—then deploy a low-cost AWS reference architecture that makes those pattern trade-offs tangible.

---

## Learning objectives

1. Select integration and data patterns based on latency, coupling, volume, reliability, security, cost, and ops complexity (CLO 16).
2. Design application architectures with clear domains, ownership, and shared-platform boundaries (CLO 17).
3. Articulate data product, master data, and metadata ownership models (CLO 18).
4. Defend pattern choices with ADRs and an integration pattern matrix.

Full detail: [`learning-objectives.md`](learning-objectives.md)

---

## Prerequisites

See [`prerequisites.md`](prerequisites.md).

---

## Lessons

| ID | Title | Est. focus |
| -- | ----- | ---------- |
| 6.1 | Integration pattern selection | Concept |
| 6.2 | Application domains and platform boundaries | Concept |
| 6.3 | Data products, master data, and events | Concept |
| 6.4 | Reference architecture leadership and lab | Application / leadership |

---

## Lab

**Build NorthStar’s Integration Reference Architecture**  
Student instructions: [`../../labs/lab-06-integration-platform/student-instructions.md`](../../labs/lab-06-integration-platform/student-instructions.md)

### Deliverables

- Integration pattern matrix for NorthStar scenarios
- Reference architecture diagram (Mermaid)
- Data-flow diagram for payments + partner files
- ≥2 ADRs (e.g., sync API vs events; SFTP/Transfer vs S3 landing)
- Working Terraform exercise evidence + cleanup

---

## Assignment

[`../../assessments/assignments/module-06-assignment.md`](../../assessments/assignments/module-06-assignment.md)

## Quiz

[`../../assessments/quizzes/module-06-quiz.md`](../../assessments/quizzes/module-06-quiz.md)

## Slides

[`../../slides/module-06/slide-outline.md`](../../slides/module-06/slide-outline.md)

---

## Capstone contribution

- Integration reference architecture
- Pattern matrix and ADRs
- Data ownership notes for customer/payment domains

---

## Related templates

- [`student/templates/16-integration-pattern-matrix.md`](../../student/templates/16-integration-pattern-matrix.md)
- [`student/templates/22-data-flow-diagram.md`](../../student/templates/22-data-flow-diagram.md)
- [`student/templates/01-architecture-decision-record.md`](../../student/templates/01-architecture-decision-record.md)
