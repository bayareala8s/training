# Week 7 — Security, Compliance & Governance

| | |
|---|---|
| **Duration** | 8–9 hours (3h lecture · 4h labs · 1h assignment/review) |
| **Difficulty** | Advanced |
| **Prerequisites** | Weeks 1–6 (operations foundation) |

## Module summary

Week 7 connects Terraform to **enterprise security and compliance**: IAM least privilege for automation roles, mandatory **tagging** for cost and ABAC, static analysis with **Checkov**, and **policy-as-code** patterns (OPA/Sentinel concepts, SCP alignment). Students tighten IAM policies, enforce tag validations, and produce a security validation report for CI.

## Deliverables

- [ ] Hardened Terraform runner IAM policy with justification
- [ ] Required tags enforced in environment variables
- [ ] `docs/security/week-07-validation-report.md` from Checkov/tflint
- [ ] Assignment: governance control matrix (see `05-assignment.md`)

## Session plan

| Segment | Time | Material |
|---------|------|----------|
| IAM for Terraform automation | 60 min | `02-lecture.md` §1–2 |
| Tagging, cost, ABAC | 45 min | `02-lecture.md` §3 |
| Static analysis & policy-as-code | 75 min | `02-lecture.md` §4–5 |
| Break | 15 min | |
| Lab 7.1 IAM | 90 min | `04-hands-on-labs.md` |
| Lab 7.2 tagging | 75 min | `04-hands-on-labs.md` |
| Lab 7.3 compliance CI | 90 min | `04-hands-on-labs.md` |
| Q&A & assignment briefing | 30 min | `05-assignment.md` |


## Diagrams (PNG & SVG)

Download all Week 7 figures: [diagrams/by-week/week-07](../../diagrams/by-week/week-07/README.md) · [Full catalog](../../diagrams/README.md)

## Files

- [01-learning-objectives.md](01-learning-objectives.md)
- [02-lecture.md](02-lecture.md)
- [03-enterprise-scenarios.md](03-enterprise-scenarios.md)
- [04-hands-on-labs.md](04-hands-on-labs.md)
- [05-assignment.md](05-assignment.md)
- [06-instructor-notes.md](06-instructor-notes.md)
- [07-knowledge-check.md](07-knowledge-check.md)
- [glossary.md](glossary.md)
