# Week 8 — Hands-On Labs (Capstone)

**Total build time:** 10–12 hours · **Guides:** [`labs/week-08/LAB-capstone.md`](../../labs/week-08/LAB-capstone.md) · [`../../capstone/README.md`](../../capstone/README.md)

---

## Capstone lab overview

Week 8 has no traditional three-lab sequence. Students execute **one capstone track** integrating weeks 1–7. This document expands the lab guide with milestones, verification, and submission checklist.

---

## Step 0 — Select track (Day 1)

| Option | Read first |
|--------|------------|
| 1 Landing Zone | [`../../capstone/README.md`](../../capstone/README.md) Option 1 |
| 2 Shared Services | Option 2 |
| 3 Multi-Region DR | Option 3 |
| 4 Internal Platform | Option 4 |

Record choice in `capstone/README.md` (your fork or `capstone/your-name/`).

---

## Step 1 — Architecture (Days 1–2)

### Deliverables

- Logical diagram (accounts, CI, state, services)
- Network or platform diagram if applicable
- README problem statement (2–3 paragraphs)

### Verification

- [ ] Peer or instructor sign-off on scope (optional cohort step)
- [ ] State keys and accounts documented before coding

---

## Step 2 — Core Terraform (Days 3–4)

### Required integration checklist

- [ ] Remote state (S3 + DynamoDB) — Week 1
- [ ] Account/env boundaries documented — Week 2
- [ ] ≥2 reusable modules or course module extensions — Week 3
- [ ] dev + test or prod path — Week 5
- [ ] No secrets in Git; OIDC or role — Weeks 4 & 7

### Suggested layout

```text
capstone/
├── README.md
├── architecture/
│   └── diagram.png
├── terraform/
│   └── environments/...
├── .github/workflows/
└── docs/
    ├── security-review.md
    └── cost-analysis.md
```

### Commands (example)

```bash
cd capstone/terraform/environments/dev
terraform init -backend-config=backend.hcl
terraform plan
```

---

## Step 3 — CI/CD & governance (Day 5)

- [ ] GitHub Actions (or equivalent): fmt, validate, plan on PR
- [ ] Apply gated (manual approval or environment protection)
- [ ] Checkov or tflint in pipeline — Week 7

Reference: [`labs/week-04/workflows/terraform-ci.yml`](../../labs/week-04/workflows/terraform-ci.yml)

---

## Step 4 — Security & cost (Day 6)

| Document | Minimum content |
|----------|-----------------|
| `docs/security-review.md` | IAM, encryption, public exposure, secrets |
| `docs/cost-analysis.md` | Monthly estimate or tagged resource table |

Reuse Week 7 validation report format where applicable.

---

## Step 5 — Operations & cleanup (Day 6–7)

- [ ] Document `make lab-stop` or cost controls
- [ ] Link or excerpt recovery runbook (Week 6)
- [ ] Drift approach documented (Week 5)

---

## Step 6 — Presentation (Day 7)

**Duration:** 15–20 minutes

| Section | Minutes |
|---------|---------|
| Business problem | 2 |
| Architecture | 5 |
| CI/Terraform demo | 5 |
| Security & cost | 3 |
| Lessons learned | 2 |

### Demo options

- Live: PR → plan comment → merge → apply (dev)
- Recorded backup if live fails

---

## Submission checklist

- [ ] GitHub repo URL
- [ ] Slide deck or PDF
- [ ] Optional recorded demo link
- [ ] Self-assessment against [capstone rubric](../../capstone/README.md)
- [ ] Peer review form (if cohort assigns)

---

## Cost cleanup

```bash
make lab-stop
# After course completion:
make destroy ENV=dev
```

Do **not** destroy bootstrap state bucket until all environments are destroyed.

---

## Getting help

| Blocker | Resource |
|---------|----------|
| Scope too large | Instructor office hours; cut one region/account |
| CI auth | [`labs/week-04/docs/oidc-setup.md`](../../labs/week-04/docs/oidc-setup.md) |
| Checkov failures | Week 7 `.checkov.yml` skip with ticket |
| State errors | Week 6 recovery runbook |
