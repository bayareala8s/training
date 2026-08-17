# Week 8 — Capstone Lab Guide

**Duration:** 10–12 hours · **Week 8**

## Choose one track

See [capstone/README.md](../../capstone/README.md) for full rubric and **ready reference implementations**.

| Option | Focus | Reference folder |
|--------|--------|------------------|
| 1 | Enterprise landing zone | [option-01-landing-zone](../../capstone/option-01-landing-zone/) |
| 2 | Shared services platform | [option-02-shared-services](../../capstone/option-02-shared-services/) |
| 3 | Multi-region DR | [option-03-multi-region-dr](../../capstone/option-03-multi-region-dr/) |
| 4 | Internal Terraform platform | [option-04-terraform-platform](../../capstone/option-04-terraform-platform/) |

You may extend a reference implementation or build from scratch. Graded work must include your own security/cost writeups and presentation.

## Required integration

Your capstone must demonstrate:

- [ ] Remote state (S3 + DynamoDB)
- [ ] Reusable modules from `modules/` or your extensions
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] dev + test or prod promotion path
- [ ] Security report (Week 7 template)
- [ ] Cost estimate (AWS Pricing Calculator export or table)
- [ ] `make lab-stop` documented in operations section

## Suggested repository layout

```text
capstone/
├── README.md              # Your project overview
├── architecture/
│   └── diagram.png
├── terraform/
│   └── environments/...
├── .github/workflows/
└── docs/
    ├── security-review.md
    └── cost-analysis.md
```

## Milestones

| Day | Task |
|-----|------|
| 1–2 | Architecture + account design |
| 3–4 | Core Terraform implementation |
| 5 | CI/CD + governance |
| 6 | Security + cost docs |
| 7 | Presentation (15–20 min) |

## Presentation checklist

- Business problem (2 min)
- Architecture (5 min)
- Live demo: PR → plan → apply (5 min)
- Security & cost (3 min)
- Lessons learned (2 min)

## Submission

- GitHub repo link (fork or dedicated capstone repo)
- Slide deck or PDF in `capstone/your-name/`
- Recorded demo link (optional per cohort)

## Cost cleanup

```bash
make lab-stop
make destroy ENV=dev   # when course complete
```

Do **not** destroy bootstrap state bucket until all environments are destroyed.
