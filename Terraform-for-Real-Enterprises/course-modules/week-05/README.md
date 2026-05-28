# Week 5 — Environment Promotion, Drift & Safe Refactoring

| | |
|---|---|
| **Duration** | 8–9 hours (3h lecture · 4h labs · 1h assignment/review) |
| **Difficulty** | Intermediate–Advanced |
| **Prerequisites** | Weeks 1–4 (state, multi-account, modules, CI/CD) |

## Module summary

Week 5 teaches how enterprises move infrastructure changes through **dev → test → prod** without surprise, how to **detect and remediate drift** when reality diverges from code, and how to **refactor Terraform safely** (moves, imports, state surgery) without outages. Students promote the shared environment stacks, simulate console drift, and document operational runbooks.

## Deliverables

- [ ] Test environment deployed via promotion checklist
- [ ] Drift report with remediation decision documented
- [ ] Environment promotion runbook (`docs/runbooks/environment-promotion.md`)
- [ ] Assignment: promotion & drift governance design (see `05-assignment.md`)

## Session plan

| Segment | Time | Material |
|---------|------|----------|
| Promotion models & pipelines | 60 min | `02-lecture.md` §1–3 |
| Drift detection & remediation | 75 min | `02-lecture.md` §4–5 |
| Safe refactoring & state moves | 60 min | `02-lecture.md` §6–7 |
| Break | 15 min | |
| Lab 5.1 promotion | 120 min | `04-hands-on-labs.md` |
| Lab 5.2–5.3 drift | 120 min | `04-hands-on-labs.md` |
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
