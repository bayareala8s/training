# Week 3 — Terraform Modules (Enterprise Design)

| | |
|---|---|
| **Duration** | 8–10 hours (3h lecture · 5–6h labs · 1h assignment/review) |
| **Difficulty** | Intermediate–Advanced |
| **Prerequisites** | Weeks 1–2; comfort with HCL variables, outputs, and `module` blocks |

## Module summary

Week 3 shifts from “Terraform that works” to **Terraform that scales across teams**: module interfaces (inputs/outputs), composition, semantic versioning, publishing via Git tags or private registry, and consumer upgrade policies. Students extend the course VPC module, compose networking + compute stacks, and publish an internal module release with a CHANGELOG.

## Deliverables

- [ ] Enhanced `modules/vpc/` with documented inputs/outputs and README examples
- [ ] Composed environment stack (VPC → compute) validating across dev/test/prod configs
- [ ] Git tag `modules/vpc/v1.0.0` (or equivalent) and `CHANGELOG.md`
- [ ] Assignment: module design review (see `05-assignment.md`)

## Session plan

| Segment | Time | Material |
|---------|------|----------|
| Module anatomy & interfaces | 60 min | `02-lecture.md` §1–2 |
| Composition & data flow | 45 min | `02-lecture.md` §3 |
| Versioning & publishing | 60 min | `02-lecture.md` §4–5 |
| Testing & documentation | 30 min | `02-lecture.md` §6 |
| Break | 15 min | |
| Lab 3.1 VPC module | 180 min | `04-hands-on-labs.md` |
| Lab 3.2 composition | 120 min | `04-hands-on-labs.md` |
| Lab 3.3 publish | 90 min | `04-hands-on-labs.md` |
| Q&A & assignment | 30 min | `05-assignment.md` |


## Diagrams (PNG & SVG)

Download all Week 3 figures: [diagrams/by-week/week-03](../../diagrams/by-week/week-03/README.md) · [Full catalog](../../diagrams/README.md)

## Files

- [01-learning-objectives.md](01-learning-objectives.md)
- [02-lecture.md](02-lecture.md)
- [03-enterprise-scenarios.md](03-enterprise-scenarios.md)
- [04-hands-on-labs.md](04-hands-on-labs.md)
- [05-assignment.md](05-assignment.md)
- [06-instructor-notes.md](06-instructor-notes.md)
- [07-knowledge-check.md](07-knowledge-check.md)
- [glossary.md](glossary.md)

## Course context

- **Repository:** `bayareala8s/training/Terraform-for-Real-Enterprises`
- **Modules path:** [`modules/`](../../modules/) consumed by [`labs/shared/environments/`](../../labs/shared/environments/)
- **Tagging:** `Course=terraform-enterprise`
