# Course Build Plan

**Course:** Enterprise Architecture Leadership Masterclass  
**Platform:** BayLearn  
**Owner:** BayAreaLa8s  
**Case study:** NorthStar Financial Services (fictional)  
**Plan version:** 1.1  
**Last updated:** 2026-07-15  
**Overall status:** READY TO TEACH

---

## Guiding Principle

Do **not** generate the entire course in one uncontrolled pass.  
Generate in phases. Validate after each module. Update the manifest. Stop for review at defined checkpoints.

---

## Phase Overview

| Phase | Scope | Checkpoint |
| ----- | ----- | ---------- |
| 1 | Foundation | **Stop for review** |
| 2 | Modules 1–4 | Stop after Module 4 |
| 3 | Modules 5–8 (AWS) | Stop after Module 8 |
| 4 | Modules 9–10 + Capstone | Stop after Capstone |
| 5 | BayLearn seed + marketing | Stop for seed review |
| 6 | Validation | Fix defects |
| 7 | Packaging | Final Done |

---

## Phase 1 — Foundation (Current)

### Objectives

- Inspect repository
- Create directory structure
- Create this build plan
- Create `COURSE_MANIFEST.json`
- List all assets to be generated
- Generate reusable master templates
- Create course-specification foundation documents
- Create NorthStar case study baseline
- **Stop and request review**

### Deliverables

| Asset | Path | Status |
| ----- | ---- | ------ |
| README | `README.md` | Generated |
| Build plan | `COURSE_BUILD_PLAN.md` | Generated |
| Manifest | `COURSE_MANIFEST.json` | Generated |
| Course overview | `course-specification/course-overview.md` | Generated |
| Learning outcomes | `course-specification/learning-outcomes.md` | Generated |
| Delivery model | `course-specification/delivery-model.md` | Generated |
| Assessment model | `course-specification/assessment-model.md` | Generated |
| Instructor standards | `course-specification/instructor-standards.md` | Generated |
| Content standards | `course-specification/content-standards.md` | Generated |
| NorthStar case study | `course-specification/northstar-case-study.md` | Generated |
| Asset inventory | `course-specification/asset-inventory.md` | Generated |
| Master templates | `templates/master/`, `templates/module/`, `templates/lab/`, `templates/assessment/` | Generated |
| Standard rubric | `assessments/rubrics/standard-architecture-rubric.md` | Generated |
| Directory tree | Full repo structure | Generated |

### Exit criteria

- [x] Directory structure matches specification §15
- [x] Manifest lists all planned assets with status
- [x] Templates are reusable across modules
- [ ] Product owner approves Phase 1

### After approval

Proceed to Phase 2 — Module 1 first, then Modules 2–4 sequentially.

---

## Phase 2 — Modules 1–4

### Scope

Business and architecture foundations (no AWS deploy labs yet).

| Module | Title | Lab type |
| ------ | ----- | -------- |
| 01 | The Enterprise Architect’s Role | Architecture operating model |
| 02 | Business Architecture and Capability Mapping | Capability mapping |
| 03 | Current-State Architecture Assessment | Portfolio assessment + CSV dataset |
| 04 | Target-State Architecture and Roadmaps | Target-state roadmap |

### Per-module required assets

For every module, generate:

```text
modules/module-XX-*/
├── README.md                    # Module overview
├── learning-objectives.md
├── prerequisites.md
├── lessons/
│   ├── lesson-XX.1.md
│   ├── lesson-XX.2.md
│   ├── lesson-XX.3.md
│   └── lesson-XX.4.md           # 3–5 lessons
├── diagrams/                    # Mermaid sources
├── workbook-section.md
├── common-mistakes.md
├── debrief-questions.md
├── linkedin-promo.md
└── youtube-description.md

instructor/guides/module-XX/
├── instructor-guide.md
├── speaking-script.md
├── whiteboard-plan.md
├── discussion-questions.md
├── common-misconceptions.md
├── lab-facilitation-guide.md
├── reference-solution.md
├── grading-guide.md
└── slide-notes.md

labs/lab-XX-*/
├── README.md
├── student-instructions.md
├── submission-checklist.md
└── stretch-objectives.md

slides/module-XX/
├── slide-outline.md             # 15–25 slides + speaker notes
└── deck-structure.json

assessments/
├── quizzes/module-XX-quiz.md
├── answer-keys/module-XX-answer-key.md
├── assignments/module-XX-assignment.md
└── rubrics/module-XX-rubric.md  # or inherit standard + module notes

student/templates/               # Module-specific templates as needed
```

### After each module

1. Validate file completeness against checklist
2. Check internal links
3. Update `COURSE_MANIFEST.json`
4. Write `qa/module-XX-qa-report.md`
5. Proceed to next module

### Phase 2 checkpoint

Stop after Module 4 for review before AWS-heavy content.

---

## Phase 3 — Modules 5–8 (AWS Labs)

### Scope

Cloud, integration, security/resilience, and AI — with serverless AWS labs.

| Module | Lab | Key AWS services |
| ------ | --- | ---------------- |
| 05 | Cloud platform foundation | IAM, S3, CloudTrail, CloudWatch, Budgets, DynamoDB, Lambda, API Gateway, SSM |
| 06 | Integration platform | API Gateway, Lambda, EventBridge, SQS, Step Functions, S3, DynamoDB, SNS |
| 07 | Security & resilience | IAM, KMS, S3 versioning, CloudWatch, DR simulation |
| 08 | AI decision assistant | Bedrock, Lambda, Step Functions, DynamoDB, S3, API Gateway, CloudWatch |

### Additional AWS requirements

- Terraform modules under `infrastructure/terraform/`
- Cost estimates under `infrastructure/cost-estimates/`
- Cleanup scripts
- Security warnings
- Resource tags: `Project=BayLearn`, `Course=EnterpriseArchitectureLeadership`, etc.
- Avoid NAT Gateway, always-on EC2, EKS, OpenSearch, continuous Transfer Family endpoints
- Target Lab 5 cost ≈ <$5 when cleaned up promptly
- `terraform fmt` and `terraform validate` where applicable

### Phase 3 checkpoint

Stop after Module 8 for AWS cost/security review.

---

## Phase 4 — Modules 9–10 and Capstone

### Scope

| Module | Focus |
| ------ | ----- |
| 09 | Governance, ARB simulation, ADRs, executive communication |
| 10 | Capstone narrative, trade-offs, presentation, career plan |
| Capstone | NorthStar Enterprise Transformation Program (24 artifacts) |

### Capstone required artifacts

See specification §7 (24 artifacts including 5 ADRs and 15-slide executive presentation).

### Phase 4 checkpoint

Stop for capstone and grading review.

---

## Phase 5 — BayLearn Integration

### Seed files

```text
baylearn-seed/
├── course.json
├── modules.json
├── lessons.json
├── assignments.json
├── rubrics.json
├── materials.json
├── quizzes.json
└── cohort.json
```

### Additional

- Course landing-page copy
- Certificate configuration
- Cohort schedule
- Email templates

### Phase 5 checkpoint

Validate JSON schemas and portal compatibility.

---

## Phase 6 — Validation

Validate:

- [ ] All 10 modules have required assets
- [ ] All labs have cleanup sections (AWS labs)
- [ ] All assignments have rubrics
- [ ] All quizzes have answer keys
- [ ] All files are linked from module READMEs
- [ ] All JSON validates
- [ ] Terraform formats and validates
- [ ] No broken references
- [ ] No duplicated contradictory content
- [ ] Consistent branding and terminology
- [ ] No placeholder/TODO content remains
- [ ] Student and instructor packages are separable
- [ ] Reference solutions clearly separated from student materials

---

## Phase 7 — Packaging

Create:

| Package | Contents |
| ------- | -------- |
| Student course ZIP | Modules, labs (student), workbook, templates, datasets |
| Instructor course ZIP | Guides, scripts, solutions, grading, slide notes |
| AWS lab ZIP | Terraform, lab guides, cleanup, cost estimates |
| Capstone ZIP | Brief, datasets, templates, rubric |
| BayLearn seed ZIP | All seed JSON |
| Complete course manifest | Final `COURSE_MANIFEST.json` + packaging report |

---

## Generation Order (Recommended)

```text
Phase 1  → Foundation + templates          [CHECKPOINT]
Phase 2a → Module 01                       [QA]
Phase 2b → Module 02                       [QA]
Phase 2c → Module 03 (+ app inventory CSV) [QA]
Phase 2d → Module 04                       [CHECKPOINT]
Phase 3a → Module 05 (+ Terraform)         [QA]
Phase 3b → Module 06 (+ Terraform)         [QA]
Phase 3c → Module 07 (+ Terraform)         [QA]
Phase 3d → Module 08 (+ Bedrock lab)       [CHECKPOINT]
Phase 4a → Module 09                       [QA]
Phase 4b → Module 10                       [QA]
Phase 4c → Capstone package                [CHECKPOINT]
Phase 5  → BayLearn seed + marketing       [CHECKPOINT]
Phase 6  → Full validation                 [FIX]
Phase 7  → Packaging                       [DONE]
```

---

## Quality Gates (Every Module)

| Gate | Rule |
| ---- | ---- |
| Completeness | All files in per-module checklist exist |
| Case study | References NorthStar consistently; labeled fictional |
| Trade-offs | Explicit alternatives and consequences |
| Security | Security/ops/cost considered where relevant |
| Assessment | Quiz + answer key + assignment + rubric |
| Instructor | Full instructor package present |
| Manifest | Status updated to `generated` or `validated` |
| QA report | `qa/module-XX-qa-report.md` written |

---

## Roles During Generation

| Role | Responsibility |
| ---- | -------------- |
| Curriculum designer | Outcomes, lesson flow, assessments |
| Enterprise architect | Technical accuracy, trade-offs, ADRs |
| AWS lab engineer | Terraform, cost, cleanup, security |
| Technical instructor | Scripts, facilitation, misconceptions |
| Course-production specialist | Manifest, packaging, BayLearn seed |

---

## Definition of Done (Course-Level)

The course is complete only when all items in specification §20 are satisfied, including:

- All 10 modules exist with full asset sets
- AWS labs deploy and clean up successfully
- Capstone integrates all modules
- BayLearn seed validates
- No placeholder content remains
- Course can be delivered live without requiring additional content creation

---

## Current Checkpoint

**Status:** Phases 1–7 complete — **READY TO TEACH**.

**Start:** [`INSTRUCTOR_START_HERE.md`](INSTRUCTOR_START_HERE.md) · Packages in `packages/` · Final QA: [`qa/course-final-qa.md`](qa/course-final-qa.md)
