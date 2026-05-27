# Self-Serve Enterprise File Transfer on AWS

**BayAreaLa8s · BayLearn Academy** — Commercial training program for architects, platform engineers, and integration leads building governed, self-service file transfer on AWS.

## Program at a glance

| Attribute | Detail |
|-----------|--------|
| **Duration** | 8 weeks (recommended: 6–8 hrs/week) |
| **Format** | Instructor-led (ILT), virtual ILT, or hybrid self-paced with live labs |
| **Level** | Intermediate (AWS fundamentals + basic networking required) |
| **Capstone** | Production-style reference architecture + demo runbook |
| **Certification path** | Portfolio artifact + practical assessment (internal BayLearn credential) |

## Repository layout

| Path | Purpose |
|------|---------|
| [`COURSE.md`](COURSE.md) | **Master curriculum** — overview, outcomes, use cases, full syllabus, assessments, career outcomes, tech stack, BayAreaLa8s positioning |
| [`docs/modules/`](docs/modules/) | **Full instructional content** per week (lectures, diagrams, examples, case studies, knowledge checks) |
| [`docs/syllabus/`](docs/syllabus/) | Week-by-week syllabus index (links to modules + labs) |
| [`docs/labs/`](docs/labs/) | Hands-on lab instructions and deliverables |
| [`docs/quizzes/`](docs/quizzes/) | **72 quiz questions** (weeks 1–6) with answer keys |
| **Lab 9 (stretch)** | [`docs/labs/lab-09-ecs-fargate-large-files.md`](docs/labs/lab-09-ecs-fargate-large-files.md) — ECS Fargate large files |
| [`docs/capstone.md`](docs/capstone.md) | Capstone brief, rubric, submission checklist |
| [`docs/assessment.md`](docs/assessment.md) | Quizzes, practicals, grading weights |
| [`docs/career-outcomes.md`](docs/career-outcomes.md) | Roles, skills matrix, interview prep |
| [`docs/technologies.md`](docs/technologies.md) | AWS services, prerequisites, reference links |
| [`marketing/`](marketing/) | Brochure, enterprise proposal, BayLearn listing, [pricing](marketing/contact-and-pricing.md) |
| [`lms/module-manifest.json`](lms/module-manifest.json) | Module metadata for LMS import |

## Quick start for instructors

1. Read [`COURSE.md`](COURSE.md) for program narrative and learning outcomes.
2. Assign weekly reading from [`docs/syllabus/`](docs/syllabus/) and labs from [`docs/labs/`](docs/labs/).
3. Use [`docs/capstone.md`](docs/capstone.md) for weeks 7–8 project work.
4. Grade with [`docs/assessment.md`](docs/assessment.md) rubrics.
5. Share [`marketing/brochure-one-pager.md`](marketing/brochure-one-pager.md) with sponsors and L&D teams.

## Quick start for learners

1. Confirm prerequisites in [`docs/technologies.md`](docs/technologies.md).
2. Configure AWS CLI credentials and copy `infra/environments/lab/terraform.tfvars.example` → `terraform.tfvars`.
3. **Validate locally:** `./scripts/ci_verify.sh` (unit tests + Terraform)
4. **Full cycle (deploy + test + destroy):** `LAB_LARGE_FILE_MB=5 ./scripts/lab_cycle.sh --yes --destroy`
5. **Start labs:** `./scripts/start_stack.sh --yes` · **Stop (no cost):** `./scripts/stop_stack.sh --yes`
6. Complete labs in order; submit weekly deliverables listed in each lab guide.
7. Build the capstone in weeks 7–8 per [`docs/capstone.md`](docs/capstone.md).

See [`docs/labs/TERRAFORM-LABS.md`](docs/labs/TERRAFORM-LABS.md) and [`infra/README.md`](infra/README.md).

## Alignment with BayAreaLa8s platforms

This curriculum aligns with production patterns used in **BayServe** (self-serve connections, Cognito, API + UI) and **BayRelay** (orchestration, Transfer Family connectors, Step Functions, governance). Labs are vendor-neutral AWS exercises; optional stretch modules reference agentic control-plane patterns.

## Licensing and use

Course materials are intended for **BayLearn academy**, **enterprise training proposals**, and **authorized BayAreaLa8s workshops**. Confirm cohort dates and any custom discount in the [enterprise proposal](marketing/enterprise-training-proposal.md) before client distribution.

## Contact

- **Academy (public enrollment):** [academy@bayareala8s.com](mailto:academy@bayareala8s.com)
- **Enterprise workshops:** [training@bayareala8s.com](mailto:training@bayareala8s.com)
- **Pricing:** [marketing/contact-and-pricing.md](marketing/contact-and-pricing.md)
