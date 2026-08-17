# Week 4 — CI/CD Pipelines for Terraform

| | |
|---|---|
| **Duration** | 8–10 hours (3h lecture · 5h labs · 1h assignment/review) |
| **Difficulty** | Intermediate–Advanced |
| **Prerequisites** | Weeks 1–3; GitHub account; Week 2 IAM concepts |

## Module summary

Week 4 operationalizes Terraform through **GitOps**: pull-request plans, protected applies, GitHub Actions workflows, **OIDC federation** (no long-lived AWS keys in GitHub), and static analysis gates (`fmt`, `validate`, `tflint`, `checkov`). Students wire the course CI template, configure environment approval gates, and document security findings from automated scans.

## Deliverables

- [ ] `.github/workflows/terraform-ci.yml` running on PR (fmt, validate, plan)
- [ ] OIDC IAM role documented or configured per [`labs/week-04/docs/oidc-setup.md`](../../labs/week-04/docs/oidc-setup.md)
- [ ] GitHub Environment protection for apply (dev/prod pattern)
- [ ] `docs/security/week-04-ci-findings.md` remediation log
- [ ] Assignment: pipeline design document (see `05-assignment.md`)

## Session plan

| Segment | Time | Material |
|---------|------|----------|
| GitOps & pipeline philosophy | 45 min | `02-lecture.md` §1–2 |
| GitHub Actions for Terraform | 60 min | `02-lecture.md` §3 |
| OIDC & credential hygiene | 45 min | `02-lecture.md` §4 |
| Plan/apply gates & environments | 45 min | `02-lecture.md` §5 |
| Validation & policy-as-code | 30 min | `02-lecture.md` §6 |
| Break | 15 min | |
| Lab 4.1 GitHub Actions | 180 min | `04-hands-on-labs.md` |
| Lab 4.2 approval gates | 120 min | `04-hands-on-labs.md` |
| Lab 4.3 validation | 120 min | `04-hands-on-labs.md` |
| Q&A & assignment | 30 min | `05-assignment.md` |


## Diagrams (PNG & SVG)

Download all Week 4 figures: [diagrams/by-week/week-04](../../diagrams/by-week/week-04/README.md) · [Full catalog](../../diagrams/README.md)

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

- **Workflow template:** [`labs/week-04/workflows/terraform-ci.yml`](../../labs/week-04/workflows/terraform-ci.yml)
- **OIDC guide:** [`labs/week-04/docs/oidc-setup.md`](../../labs/week-04/docs/oidc-setup.md)
- **Cross-account IAM:** Week 2 runner role assumed by CI via OIDC
