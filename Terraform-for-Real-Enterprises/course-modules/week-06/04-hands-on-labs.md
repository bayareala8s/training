# Week 6 — Hands-On Labs (Detailed)

**Total lab time:** ~6–7 hours · **Repository paths:** [`labs/week-06/`](../../labs/week-06/)

---

## Lab 6.1 — Simulate Failed Deployment

**Duration:** 2 hours · **Guide:** [labs/week-06/LAB-01-failed-deploy.md](../../labs/week-06/LAB-01-failed-deploy.md)

### Objectives

- Experience a non-zero `terraform apply`
- Document AWS vs state after failure

### Detailed procedure

1. In `labs/shared/environments/dev/main.tf`, temporarily add:

```hcl
resource "aws_instance" "bad" {
  ami           = "ami-invalid"
  instance_type = "t3.micro"
  subnet_id     = module.vpc.public_subnet_ids[0]
}
```

2. Run `make apply ENV=dev` and capture error output
3. Run `terraform state list` — note if `aws_instance.bad` appears or is tainted
4. Remove bad resource block; run `make plan ENV=dev`
5. Write incident notes: what exists in AWS vs state

### Success criteria

- [ ] Notes explain partial apply / taint behavior
- [ ] Dev environment returned to clean plan after fix

### Safety

Use **dev only**. Never inject invalid AMIs in test/prod.

---

## Lab 6.2 — Terraform State Recovery

**Duration:** 2–3 hours · **Guide:** [labs/week-06/LAB-02-state-recovery.md](../../labs/week-06/LAB-02-state-recovery.md)

### Objectives

- Practice `terraform state` inspection and backup
- Explore S3 state object versioning (sandbox)

### Detailed procedure

#### Part A — Inspection

```bash
cd labs/shared/environments/dev
terraform state list
terraform state show 'module.vpc.aws_vpc.this'  # adjust address if needed
```

#### Part B — Backup

```bash
terraform state pull > /tmp/state-backup-$(date +%Y%m%d).json
```

#### Part C — S3 versions (instructor-approved sandbox)

```bash
aws s3api list-object-versions \
  --bucket YOUR-STATE-BUCKET \
  --prefix environments/dev/terraform.tfstate
```

Document restore procedure in runbook—**do not restore prod without approval**.

#### Part D — Untaint (if applicable)

```bash
terraform untaint 'RESOURCE_ADDRESS'  # only after validating resource health
```

### Success criteria

- [ ] State backup file created
- [ ] `docs/runbooks/terraform-recovery.md` updated with state sections

---

## Lab 6.3 — Rollback Automation Workflow

**Duration:** 2 hours · **Guide:** [labs/week-06/LAB-03-rollback.md](../../labs/week-06/LAB-03-rollback.md)

### Objectives

- Document Git-based infrastructure rollback
- Exercise rollback helper script (dry run)

### Detailed procedure

1. **Git revert pattern** (documentation or branch simulation):

```bash
git revert HEAD --no-edit
# CI runs plan → approved apply
```

2. **Rollback script dry run:**

```bash
./scripts/terraform/rollback-plan.sh --env dev --ref HEAD~1
```

3. Complete all sections in `docs/runbooks/terraform-recovery.md`:
   - Failed apply triage
   - State backup/restore
   - Lock break-glass
   - Git revert + CI apply
   - Escalation contacts (placeholders OK)

### Success criteria

- [ ] Runbook complete and internally consistent
- [ ] Evidence of rollback-plan.sh output attached or summarized

---

## Lab submission

Submit:

1. Failed-apply incident notes (Lab 6.1)
2. `docs/runbooks/terraform-recovery.md`
3. Screenshot or CLI output: `list-object-versions` (redacted bucket name OK)
4. Short answer: when is state version restore **dangerous**?
