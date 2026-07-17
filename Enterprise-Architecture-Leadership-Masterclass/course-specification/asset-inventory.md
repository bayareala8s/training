# Complete Asset Inventory

This inventory lists all assets planned for the course. Status reflects Phase 1 completion.

**Legend:** `generated` | `planned` | `validated` | `packaged`

---

## A. Foundation (Phase 1)

| Asset | Path | Status |
| ----- | ---- | ------ |
| README | `README.md` | generated |
| Build plan | `COURSE_BUILD_PLAN.md` | generated |
| Manifest | `COURSE_MANIFEST.json` | generated |
| Course overview | `course-specification/course-overview.md` | generated |
| Learning outcomes | `course-specification/learning-outcomes.md` | generated |
| Delivery model | `course-specification/delivery-model.md` | generated |
| Assessment model | `course-specification/assessment-model.md` | generated |
| Instructor standards | `course-specification/instructor-standards.md` | generated |
| Content standards | `course-specification/content-standards.md` | generated |
| NorthStar case study | `course-specification/northstar-case-study.md` | generated |
| Asset inventory | `course-specification/asset-inventory.md` | generated |
| Standard rubric | `assessments/rubrics/standard-architecture-rubric.md` | generated |

---

## B. Per-module assets (×10 modules)

For each module `01`–`10`, generate:

### Module content

| Asset | Typical path |
| ----- | ------------ |
| Module README / overview | `modules/module-XX-*/README.md` |
| Learning objectives | `modules/module-XX-*/learning-objectives.md` |
| Prerequisites | `modules/module-XX-*/prerequisites.md` |
| Lessons (3–5) | `modules/module-XX-*/lessons/lesson-XX.*.md` |
| Mermaid diagrams | `modules/module-XX-*/diagrams/` |
| Workbook section | `modules/module-XX-*/workbook-section.md` |
| Common mistakes | `modules/module-XX-*/common-mistakes.md` |
| Debrief questions | `modules/module-XX-*/debrief-questions.md` |
| LinkedIn promo | `modules/module-XX-*/linkedin-promo.md` |
| YouTube/Loom description | `modules/module-XX-*/youtube-description.md` |

### Instructor package

| Asset | Typical path |
| ----- | ------------ |
| Instructor guide | `instructor/guides/module-XX/instructor-guide.md` |
| Speaking script | `instructor/scripts/module-XX/speaking-script.md` |
| Whiteboard plan | `instructor/guides/module-XX/whiteboard-plan.md` |
| Discussion questions | `instructor/guides/module-XX/discussion-questions.md` |
| Common misconceptions | `instructor/guides/module-XX/common-misconceptions.md` |
| Lab facilitation guide | `instructor/guides/module-XX/lab-facilitation-guide.md` |
| Reference solution | `instructor/reference-solutions/module-XX/` |
| Grading guide | `instructor/grading/module-XX-grading-guide.md` |
| Slide notes | `instructor/guides/module-XX/slide-notes.md` |

### Lab

| Asset | Typical path |
| ----- | ------------ |
| Lab README | `labs/lab-XX-*/README.md` |
| Student instructions | `labs/lab-XX-*/student-instructions.md` |
| Submission checklist | `labs/lab-XX-*/submission-checklist.md` |
| Stretch objectives | `labs/lab-XX-*/stretch-objectives.md` |

### Slides

| Asset | Typical path |
| ----- | ------------ |
| Slide outline + speaker notes | `slides/module-XX/slide-outline.md` |
| Deck structure metadata | `slides/module-XX/deck-structure.json` |

### Assessments

| Asset | Typical path |
| ----- | ------------ |
| Quiz | `assessments/quizzes/module-XX-quiz.md` |
| Answer key | `assessments/answer-keys/module-XX-answer-key.md` |
| Assignment | `assessments/assignments/module-XX-assignment.md` |
| Rubric notes | `assessments/rubrics/module-XX-rubric.md` |
| QA report | `qa/module-XX-qa-report.md` |

**Module statuses:** all `planned` until Phase 2+

---

## C. AWS / infrastructure (Modules 5–8)

| Asset | Path pattern | Status |
| ----- | ------------ | ------ |
| Terraform modules | `infrastructure/terraform/modules/` | planned |
| Environments | `infrastructure/terraform/environments/` | planned |
| Cleanup scripts | `infrastructure/terraform/scripts/` | planned |
| Cost estimates | `infrastructure/cost-estimates/lab-0X.md` | planned |
| Diagrams | `infrastructure/diagrams/` | planned |

---

## D. Student templates (28 planned; Phase 1 ships starter set)

| # | Template | Status |
| - | -------- | ------ |
| 1 | Architecture principles | generated (starter) |
| 2 | Stakeholder matrix | generated |
| 3 | Capability map | generated |
| 4 | Capability heatmap | planned (extend in M2) |
| 5 | Value-stream map | planned (M2) |
| 6 | Application inventory | planned (M3) |
| 7 | TIME assessment | generated |
| 8 | Technical-debt register | generated |
| 9 | Current-state architecture | planned (M3) |
| 10 | Target-state architecture | planned (M4) |
| 11 | Transition-state plan | planned (M4) |
| 12 | Architecture roadmap | generated |
| 13 | Cloud strategy | generated |
| 14 | Platform capability map | planned (M5) |
| 15 | Build-versus-buy assessment | generated |
| 16 | Integration-pattern matrix | generated |
| 17 | Data-flow diagram | planned (M6) |
| 18 | Threat model | generated |
| 19 | RTO/RPO worksheet | generated |
| 20 | Risk-control matrix | generated |
| 21 | AI use-case scorecard | generated |
| 22 | AI governance checklist | generated |
| 23 | Architecture review checklist | generated |
| 24 | ADR template | generated |
| 25 | Executive decision memo | generated |
| 26 | Executive presentation template | planned (M9/M10) |
| 27 | Architecture portfolio checklist | generated |
| 28 | Personal leadership plan | generated |

Additional generated in Phase 1: RACI matrix (`05-raci-matrix.md`)

---

## E. Capstone

| Asset | Path | Status |
| ----- | ---- | ------ |
| Scenario | `capstone/scenario/` | planned |
| Student brief | `capstone/student-brief/` | planned |
| Datasets | `capstone/datasets/` | planned |
| Reference architecture | `capstone/reference-architecture/` | planned |
| Rubric | `capstone/rubric/` | planned |
| Presentation template | `capstone/presentation-template/` | planned |

Required student artifacts: 24 (see specification §7)

---

## F. BayLearn seed

| File | Status |
| ---- | ------ |
| `baylearn-seed/course.json` | planned |
| `baylearn-seed/modules.json` | planned |
| `baylearn-seed/lessons.json` | planned |
| `baylearn-seed/assignments.json` | planned |
| `baylearn-seed/rubrics.json` | planned |
| `baylearn-seed/materials.json` | planned |
| `baylearn-seed/quizzes.json` | planned |
| `baylearn-seed/cohort.json` | planned |

---

## G. Workbook and portfolio

| Asset | Path | Status |
| ----- | ---- | ------ |
| Combined workbook | `student/workbook/` | planned (assembled across modules) |
| Readings index | `student/readings/` | planned |
| Portfolio guide | `student/portfolio/` | planned |
| Application inventory CSV | `student/datasets/` | planned (M3) |

---

## H. Automation and packaging

| Asset | Path | Status |
| ----- | ---- | ------ |
| Generation prompts | `automation/generation-prompts/` | planned |
| Validation scripts | `automation/validation/` | planned |
| Packaging scripts | `automation/packaging/` | planned |
| Student ZIP | packages | planned |
| Instructor ZIP | packages | planned |
| AWS lab ZIP | packages | planned |
| Capstone ZIP | packages | planned |
| BayLearn seed ZIP | packages | planned |

---

## I. Master generation templates (Phase 1)

| Template | Path | Status |
| -------- | ---- | ------ |
| Module README | `templates/module/MODULE_README.template.md` | generated |
| Lesson | `templates/module/LESSON.template.md` | generated |
| Instructor guide | `templates/module/INSTRUCTOR_GUIDE.template.md` | generated |
| Speaking script | `templates/module/SPEAKING_SCRIPT.template.md` | generated |
| Slide outline | `templates/module/SLIDE_OUTLINE.template.md` | generated |
| Lab (general) | `templates/lab/LAB.template.md` | generated |
| AWS lab | `templates/lab/AWS_LAB.template.md` | generated |
| Quiz | `templates/assessment/QUIZ.template.md` | generated |
| Assignment | `templates/assessment/ASSIGNMENT.template.md` | generated |
| QA report | `templates/master/QA_REPORT.template.md` | generated |

---

## Estimated totals (at Done)

| Category | Count |
| -------- | ----: |
| Modules | 10 |
| Lessons | 35–45 |
| Labs | 10 |
| Quizzes | 10 |
| Assignments | 10 |
| Downloadable templates | 25+ |
| Capstone artifacts (student) | 24 |
| BayLearn seed files | 8 |

---

## Next generation batch

After Phase 1 approval: **Module 01 — The Enterprise Architect’s Role** (full asset checklist).
