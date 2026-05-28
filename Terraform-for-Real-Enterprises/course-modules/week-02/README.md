# Week 2 — AWS Multi-Account Architecture

| | |
|---|---|
| **Duration** | 8–9 hours (3h lecture · 4–5h labs · 1h assignment/review) |
| **Difficulty** | Intermediate |
| **Prerequisites** | Week 1 (remote state, provider, tagging); basic IAM |

## Module summary

Week 2 connects Terraform to **enterprise AWS account structure**: Organizations, organizational units (OUs), service control policies (SCPs), landing zones, shared services accounts, and **cross-account IAM** for automation. Students design a multi-account model, implement least-privilege runner roles, and run Terraform plans using assumed-role credentials—the same pattern CI will use in Week 4.

## Deliverables

- [ ] Multi-account architecture diagram and account matrix (`docs/architecture/week-02-accounts.md`)
- [ ] Cross-account IAM role (`bal8s-terraform-runner`) with trust and scoped policy
- [ ] Documented cross-account `terraform plan` workflow
- [ ] Assignment: landing zone design brief (see `05-assignment.md`)

## Session plan

| Segment | Time | Material |
|---------|------|----------|
| Why multi-account & blast radius | 45 min | `02-lecture.md` §1–2 |
| Organizations, OUs, SCPs | 60 min | `02-lecture.md` §3–4 |
| Landing zones & shared services | 45 min | `02-lecture.md` §5 |
| Cross-account IAM for Terraform | 60 min | `02-lecture.md` §6 |
| Break | 15 min | |
| Lab 2.1 architecture design | 90 min | `04-hands-on-labs.md` |
| Lab 2.2–2.3 IAM & apply | 150 min | `04-hands-on-labs.md` |
| Q&A & assignment briefing | 30 min | `05-assignment.md` |

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

- **Organization:** BayAreaLa8s — *Terraform for Real Enterprises*
- **Repository:** `bayareala8s/training/Terraform-for-Real-Enterprises`
- **Tagging:** `Course=terraform-enterprise` (required for [`scripts/aws/`](../../scripts/aws/) start/stop)
- **State:** Week 1 bootstrap bucket; this week maps **which account** owns state vs workloads
