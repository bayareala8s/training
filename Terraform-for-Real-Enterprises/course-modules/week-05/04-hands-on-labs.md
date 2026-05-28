# Week 5 — Hands-On Labs (Detailed)

**Total lab time:** ~5–6 hours · **Repository paths:** [`labs/week-05/`](../../labs/week-05/)

---

## Lab 5.1 — Environment Promotion

**Duration:** 2–3 hours · **Guide:** [labs/week-05/LAB-01-promotion.md](../../labs/week-05/LAB-01-promotion.md)

### Objectives

- Apply the same modules to **test** with environment-specific tfvars and backend key
- Author an environment promotion runbook with approval gates

### Detailed procedure

#### Part A — Configure test backend and variables

```bash
cd labs/shared/environments/test
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
# Ensure key = environments/test/terraform.tfstate
```

Edit `terraform.tfvars` for non-overlapping CIDR (e.g. `10.20.0.0/16`).

#### Part B — Init, plan, apply test

From course root:

```bash
make init ENV=test
make plan ENV=test
make apply ENV=test
```

Archive plan output to `docs/plans/test-promotion-YYYYMMDD.txt` (redact account IDs if sharing publicly).

#### Part C — Promotion runbook

Create `docs/runbooks/environment-promotion.md` with steps:

1. PR approved for module/version change
2. Plan in test; peer review
3. Apply test; smoke test (e.g. VPC exists, tags present)
4. Plan prod; change advisory approval
5. Apply prod in maintenance window

Include a variable comparison table:

| Variable | dev | test | prod |
|----------|-----|------|------|
| vpc_cidr | 10.10.0.0/16 | 10.20.0.0/16 | 10.30.0.0/16 |
| enable_nat_gateway | false | false | true |

### Success criteria

- [ ] Test state object exists in S3 under `environments/test/`
- [ ] `terraform state list` shows expected modules
- [ ] Runbook committed (no secrets)

### Common issues

| Symptom | Resolution |
|---------|------------|
| CIDR overlap with dev | Change test `vpc_cidr` in tfvars |
| Backend key wrong | Verify `backend.hcl` key matches environment |
| Plan wants to destroy dev resources | Wrong directory or backend key |

---

## Lab 5.2 — Simulate Infrastructure Drift

**Duration:** 2 hours · **Guide:** [labs/week-05/LAB-02-drift.md](../../labs/week-05/LAB-02-drift.md)

### Objectives

- Introduce a controlled manual change in AWS
- Detect drift via `terraform plan`

### Detailed procedure

1. Ensure dev is applied: `make apply ENV=dev`
2. In AWS Console, change one of:
   - Security group ingress rule
   - EC2 tag not in Terraform
   - Stop lab instance (if present)
3. Run `make plan ENV=dev` and save full output
4. Start `docs/drift-report-week05.md` with:
   - What you changed
   - Plan excerpt
   - Severity (low/medium/high)

### Optional stretch

```bash
driftctl scan --from terraform.tfstate  # if driftctl installed
```

### Success criteria

- [ ] Plan shows non-empty diff attributable to manual change
- [ ] Drift report started with hypothesis of cause

---

## Lab 5.3 — Remediate Drift

**Duration:** 1–2 hours · **Guide:** [labs/week-05/LAB-03-remediate.md](../../labs/week-05/LAB-03-remediate.md)

### Objectives

- Choose and execute remediation strategy
- Document prevention controls

### Remediation decision table

| Situation | Action |
|-----------|--------|
| Console change should be kept | Update `.tf`, then apply |
| Console change is wrong | `terraform apply` to revert |
| Resource exists, not in state | `terraform import` |
| State stale | Careful refresh/plan |

### Procedure

1. Apply fix: `make apply ENV=dev`
2. Confirm clean plan: `make plan ENV=dev` → no unexpected changes
3. Complete drift report using [docs/templates/drift-report.md](../../docs/templates/drift-report.md) if available
4. Add prevention section: SCP idea, nightly plan job, IAM read-only prod

### Success criteria

- [ ] `docs/drift-report-week05.md` complete
- [ ] Dev plan clean after remediation

---

## Lab submission

Submit:

1. Link or path to `docs/runbooks/environment-promotion.md`
2. Redacted test plan summary (5–10 lines)
3. Completed drift report
4. One paragraph: `moved` block vs `state mv` — when you would use each
