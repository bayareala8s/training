# Terraform Recovery Runbook

**Course:** BayAreaLa8s — Terraform for Real Enterprises  
**Owner:** Platform / DevOps team  
**Last updated:** _fill on completion_

---

## 1. When to use this runbook

- Failed `terraform apply` mid-run
- State file corruption or accidental edit
- Wrong infrastructure version deployed to environment
- Need to rollback after merge to `main`

---

## 2. Severity classification

| Level | Example | Response time |
|-------|---------|-----------------|
| SEV-1 | Prod outage from apply | Immediate rollback |
| SEV-2 | Test env broken | Same business day |
| SEV-3 | Dev sandbox | Next lab session |

---

## 3. Failed apply recovery

1. **Do not** run another apply until cause is understood.
2. Capture logs: `TF_LOG=DEBUG terraform apply 2>&1 | tee apply-failure.log`
3. `terraform state list` — identify partial resources.
4. Fix configuration; run `terraform plan`.
5. If resource exists but not in state: `terraform import ADDR ID`.
6. If resource should not exist: remove from config and `terraform apply`.

---

## 4. State file recovery (S3 backend)

```bash
# List versions
aws s3api list-object-versions \
  --bucket BUCKET \
  --prefix environments/ENV/terraform.tfstate

# Download known-good version
aws s3api get-object \
  --bucket BUCKET \
  --key environments/ENV/terraform.tfstate \
  --version-id VERSION_ID \
  /tmp/terraform.tfstate.restored
```

Coordinate with team before overwriting current state object.

---

## 5. Git rollback procedure

1. Identify good commit: `git log --oneline`
2. `git revert <bad-commit>` or deploy from tagged release
3. Open PR; require CI plan review
4. Approved apply to target environment
5. Verify with `terraform plan` (no unexpected changes)

---

## 6. Rollback script

```bash
./scripts/terraform/rollback-plan.sh --env dev --ref v1.0.0-week5
```

---

## 7. Contacts

| Role | Contact |
|------|---------|
| Instructor | _cohort channel_ |
| AWS support | Enterprise support case if applicable |

---

## 8. Post-incident

- [ ] Drift check scheduled
- [ ] ADR or postmortem filed
- [ ] Module version pin updated if needed
