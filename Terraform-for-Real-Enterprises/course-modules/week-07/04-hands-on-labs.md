# Week 7 — Hands-On Labs (Detailed)

**Total lab time:** ~5–6 hours · **Repository paths:** [`labs/week-07/`](../../labs/week-07/)

---

## Lab 7.1 — IAM Least Privilege

**Duration:** 2 hours · **Guide:** [labs/week-07/LAB-01-iam.md](../../labs/week-07/LAB-01-iam.md)

### Objectives

- Audit and tighten Terraform runner IAM policy from Week 2
- Document justification for remaining permissions

### Detailed procedure

1. Review `labs/week-02/iam/terraform-runner-policy.json`
2. Replace broad actions (e.g. `ec2:*`) with minimum actions required for course modules (VPC, EC2 describe/create for lab instance, S3 state access, DynamoDB lock)
3. Optional: enable IAM Access Analyzer

```bash
aws accessanalyzer create-analyzer --analyzer-name bal8s-lab --type ACCOUNT
```

4. Add section to security report: **IAM changes** with before/after statement count

### Success criteria

- [ ] Updated policy JSON in repo or `docs/security/`
- [ ] Written justification for any remaining `*` actions

### Common issues

| Symptom | Resolution |
|---------|------------|
| Access Denied on apply | Add specific missing action from CloudTrail |
| Over-scoped still | Pair with platform team example policy |

---

## Lab 7.2 — Tagging Policies

**Duration:** 1–2 hours · **Guide:** [labs/week-07/LAB-02-tagging.md](../../labs/week-07/LAB-02-tagging.md)

### Objectives

- Enforce required tags via variables and validations
- Verify tags in AWS console/CLI

### Required tags (course standard)

```hcl
Course      = "terraform-enterprise"
Project     = "bayareala8s-tf-course"
ManagedBy   = "terraform"
Environment = var.environment
Owner       = var.owner
```

### Procedure

1. Add `owner` variable with validation in environment `variables.tf`
2. Ensure `default_tags` in provider/locals include all keys
3. `make apply ENV=dev` if needed
4. Verify:

```bash
aws ec2 describe-instances --filters "Name=tag:Course,Values=terraform-enterprise" \
  --query 'Reservations[].Instances[].Tags' --output table
```

### Success criteria

- [ ] All lab resources show required tags
- [ ] `terraform plan` does not show tag-only churn after apply

---

## Lab 7.3 — Compliance Checks in CI

**Duration:** 2–3 hours · **Guide:** [labs/week-07/LAB-03-compliance.md](../../labs/week-07/LAB-03-compliance.md)

### Objectives

- Run Checkov locally; configure `.checkov.yml`
- Produce security validation report

### Procedure

```bash
checkov -d modules/ -d labs/shared/ --framework terraform -o cli
checkov -d modules/ -d labs/shared/ --framework terraform -o json > /tmp/checkov.json
```

Edit [`labs/week-07/.checkov.yml`](../../labs/week-07/.checkov.yml) — document any `skip-check` with ticket ID.

Create `docs/security/week-07-validation-report.md`:

- Tool versions (`checkov --version`, `terraform version`)
- Pass/fail counts
- Top 5 findings and remediation or accepted risk
- CI integration note (link Week 4 workflow)

### Success criteria

- [ ] Report committed
- [ ] CI green OR documented exceptions with expiry

---

## Lab submission

Submit:

1. IAM policy diff summary
2. CLI or screenshot proof of tags
3. `docs/security/week-07-validation-report.md`
4. One paragraph mapping a Checkov finding to a SOC2-style control theme
