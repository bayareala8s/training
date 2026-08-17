# Enterprise Architecture Leadership Masterclass

**Tagline:** From Senior Engineer to Enterprise Architecture Leader

**Product owner:** BayAreaLa8s  
**Platform:** BayLearn  
**Format:** Live instructor-led cohort  
**Duration:** 10 weeks  
**Level:** Advanced  
**Recommended tuition:** $2,499 per learner  
**Cohort size:** 8–15 learners (corporate: 10–25)

---

## Purpose

A practical architecture leadership program where students work through a realistic enterprise transformation and produce professional architecture artifacts.

Students learn to connect business strategy to technology direction, evaluate complex trade-offs, design enterprise target states, govern architecture decisions, and communicate effectively with executives and engineering teams.

This is **not** a TOGAF exam-prep course, a basic AWS class, a cloud-service tutorial series, or a generic system-design course.

---

## Case Study

All modules use one fictional enterprise:

**NorthStar Financial Services** — a global financial services and digital payments organization with 8,000 employees, 4 million retail customers, hybrid cloud estates, and a fragmented application portfolio undergoing enterprise transformation.

> NorthStar Financial Services is a **fictional** organization created for instructional purposes. It is not affiliated with any real company.

---

## Curriculum Overview

| Week | Module | Focus |
| ---: | ------ | ----- |
| 1 | The Enterprise Architect’s Role | Operating model, principles, leadership |
| 2 | Business Architecture and Capability Mapping | Strategy, capabilities, value streams |
| 3 | Current-State Architecture Assessment | Portfolio, debt, risk |
| 4 | Target-State Architecture and Roadmaps | Vision, transitions, sequencing |
| 5 | Cloud and Platform Strategy | Landing zones, platforms, FinOps |
| 6 | Integration, Application, and Data Architecture | Patterns, domains, data products |
| 7 | Security, Risk, Compliance, and Resilience | Zero Trust, threat modeling, DR |
| 8 | AI Strategy and Intelligent Enterprise Architecture | Governed AI, RAG, HITL |
| 9 | Architecture Governance and Executive Communication | ARB, ADRs, executive memos |
| 10 | Capstone and Architecture Leadership | Full transformation proposal |

---

## Weekly Commitment

- 2-hour live class
- 1-hour optional office hour
- 3–5 hours of assignment and lab work
- 1 architecture artifact per week

---

## Repository Layout

```text
├── COURSE_BUILD_PLAN.md          # Phased generation and QA plan
├── COURSE_MANIFEST.json          # Asset inventory and generation status
├── course-specification/         # Product, outcomes, delivery, assessment
├── modules/                      # Per-module lessons and materials
├── labs/                         # Student lab instructions
├── instructor/                   # Guides, scripts, solutions, grading
├── student/                      # Workbook, templates, datasets, portfolio
├── slides/                       # Slide outlines and speaker notes
├── infrastructure/               # Terraform, diagrams, cost estimates
├── assessments/                  # Quizzes, assignments, rubrics, keys
├── capstone/                     # Capstone brief, rubric, reference
├── baylearn-seed/                # Portal-compatible JSON seed data
├── templates/                    # Reusable master templates
├── automation/                   # Generation prompts, validation, packaging
└── qa/                           # Module and package QA reports
```

---

## Start here

| Audience | Document |
| -------- | -------- |
| Instructors | [`INSTRUCTOR_START_HERE.md`](INSTRUCTOR_START_HERE.md) |
| Students | [`STUDENT_START_HERE.md`](STUDENT_START_HERE.md) |
| Calendar | [`course-specification/teaching-calendar.md`](course-specification/teaching-calendar.md) |
| **Diagram library** | [`diagrams/README.md`](diagrams/README.md) · [`diagram-library/`](diagram-library/) |

## Build Status

| Phase | Description | Status |
| ----- | ----------- | ------ |
| 1 | Foundation | Complete |
| 2 | Modules 1–4 | Complete |
| 3 | Modules 5–8 (AWS labs + Terraform) | Complete |
| 4 | Modules 9–10 + Capstone | Complete |
| 5 | BayLearn seed | Complete |
| 6 | Validation | Complete |
| 7 | Packaging | Complete — see `packages/` |
| 8 | **Diagram Generation Framework** | Complete — 300+ diagrams in `diagrams/` + shared `diagram-library/` |

See [`COURSE_BUILD_PLAN.md`](COURSE_BUILD_PLAN.md) and [`COURSE_MANIFEST.json`](COURSE_MANIFEST.json).

---

## Completion Requirements

Students must:

- Attend at least 70% of live sessions
- Complete at least 80% of required assignments
- Achieve an overall score of at least 70%
- Submit the final capstone
- Present the capstone to the review panel

---

## Branding

- **Colors:** Dark navy, white, restrained gold accents
- **Tone:** Executive-quality, accessible, trade-off aware
- **Diagrams:** Mermaid and professional slide visuals
- **Format:** 16:9 slides

---

## License and Usage

Course materials are produced for BayLearn delivery by BayAreaLa8s.  
Fictional case-study data must remain clearly labeled.  
Do not imply affiliation with any real employer or financial institution.
