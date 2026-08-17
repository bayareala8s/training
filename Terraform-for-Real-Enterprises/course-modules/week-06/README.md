# Week 6 — Rollback, State Recovery & Disaster Recovery

| | |
|---|---|
| **Duration** | 8–10 hours (3h lecture · 5h labs · 1h assignment/review) |
| **Difficulty** | Advanced |
| **Prerequisites** | Weeks 1–5 (promotion, drift, CI/CD) |

## Module summary

Week 6 prepares students for **when Terraform fails**: partial applies, corrupted or divergent state, and organizational need for **rollback** and **disaster recovery**. Students experience failed applies, practice state inspection and S3 version recovery, and document Git-based rollback workflows aligned with enterprise change control.

## Deliverables

- [ ] Failed-apply incident notes (Lab 6.1)
- [ ] Updated `docs/runbooks/terraform-recovery.md`
- [ ] Evidence of state backup / version restore exercise (sandbox)
- [ ] Assignment: DR tabletop + recovery playbook (see `05-assignment.md`)

## Session plan

| Segment | Time | Material |
|---------|------|----------|
| Failed applies & partial state | 60 min | `02-lecture.md` §1–2 |
| State recovery & S3 versioning | 75 min | `02-lecture.md` §3–4 |
| Rollback strategies & DR | 75 min | `02-lecture.md` §5–7 |
| Break | 15 min | |
| Lab 6.1 failed deploy | 90 min | `04-hands-on-labs.md` |
| Lab 6.2 state recovery | 120 min | `04-hands-on-labs.md` |
| Lab 6.3 rollback workflow | 90 min | `04-hands-on-labs.md` |
| Q&A & assignment briefing | 30 min | `05-assignment.md` |


## Diagrams (PNG & SVG)

Download all Week 6 figures: [diagrams/by-week/week-06](../../diagrams/by-week/week-06/README.md) · [Full catalog](../../diagrams/README.md)

## Files

- [01-learning-objectives.md](01-learning-objectives.md)
- [02-lecture.md](02-lecture.md)
- [03-enterprise-scenarios.md](03-enterprise-scenarios.md)
- [04-hands-on-labs.md](04-hands-on-labs.md)
- [05-assignment.md](05-assignment.md)
- [06-instructor-notes.md](06-instructor-notes.md)
- [07-knowledge-check.md](07-knowledge-check.md)
- [glossary.md](glossary.md)
