# Week 8 — Capstone Submission & Self-Assessment

**Weight:** **30% of course grade** (capstone) · **Due:** Per cohort schedule · **Presentation:** 15–20 minutes

This assignment aligns with [`../../capstone/README.md`](../../capstone/README.md). Written components supplement your repository and demo.

---

## Required deliverables

| # | Deliverable | Location |
|---|-------------|----------|
| 1 | Terraform repository | GitHub URL in submission form |
| 2 | Architecture diagrams | `capstone/architecture/` or equivalent |
| 3 | CI/CD pipelines | `.github/workflows/` or documented equivalent |
| 4 | Security review | `docs/security-review.md` |
| 5 | Cost analysis | `docs/cost-analysis.md` |
| 6 | Final presentation | Live or slides + optional recording |
| 7 | Self-assessment | This document, section below |

---

## Capstone option (select one)

- [ ] **Option 1** — Enterprise Landing Zone
- [ ] **Option 2** — Shared Services Platform
- [ ] **Option 3** — Multi-Region DR
- [ ] **Option 4** — Internal Terraform Platform

---

## Integration checklist (submit as completed list)

- [ ] Remote state (S3 + DynamoDB)
- [ ] Reusable modules (course `modules/` or your own, ≥2 for option 4)
- [ ] CI: plan on PR; gated apply
- [ ] Environment promotion path (dev + test or prod)
- [ ] Drift approach documented
- [ ] Recovery/rollback referenced in ops docs
- [ ] IAM least privilege; no secrets in Git
- [ ] Checkov/tflint evidence
- [ ] Cost control (`make lab-stop` or equivalent documented)

---

## Self-assessment rubric

Score yourself **2–4** per criterion (see capstone README). Add 2–3 sentences of evidence per score.

| Criterion | Self-score (2–4) | Evidence (paths, PR links, demo timestamp) |
|-----------|------------------|---------------------------------------------|
| Architecture | | |
| Terraform quality | | |
| CI/CD & ops | | |
| Security | | |
| Docs & demo | | |

**Instructor score** uses the same rubric:

| Criterion | Excellent (4) | Proficient (3) | Needs work (2) |
|-----------|---------------|----------------|----------------|
| **Architecture** | Clear multi-account/env design, justified tradeoffs | Sound design, minor gaps | Unclear boundaries |
| **Terraform quality** | Modular, versioned, documented | Works, some duplication | Monolithic |
| **CI/CD & ops** | Full PR workflow, drift/rollback considered | Plan/apply automated | Manual only |
| **Security** | Least privilege, no secrets in Git, guardrails | Mostly secure | Critical gaps |
| **Docs & demo** | Runbooks, diagrams, confident demo | Adequate README | Incomplete |

---

## Written reflection (500–800 words)

1. **Track justification** — Why this option for your career or org context?
2. **Hardest integration** — Which week’s practice was hardest to wire in, and how you solved it?
3. **Next 90 days** — If you deployed this at work, what would phase 2 include?

---

## Submission format

- Form/link provided by instructor
- Git tag or release: `capstone-submission` recommended
- Slides: PDF in repo or learning management system

## Academic integrity

Capstone code must be your cohort work. Cite third-party modules and AI assistance per course policy.
