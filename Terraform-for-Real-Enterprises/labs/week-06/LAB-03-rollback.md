# Lab 6.3 — Rollback Automation Workflow

**Duration:** 2 hours · **Week 6**

## Objectives

- Document Git-based rollback for infrastructure
- Use provided rollback helper script

## Steps

### 1. Git revert pattern

```bash
git revert HEAD --no-edit
git push origin main
# CI runs plan → approved apply
```

### 2. Run rollback script (dry run)

```bash
./scripts/terraform/rollback-plan.sh --env dev --ref HEAD~1
```

### 3. Complete runbook

Fill all sections in `docs/runbooks/terraform-recovery.md`.

## Deliverable

Runbook + evidence of successful recovery exercise from Lab 6.1–6.2.

## Next

[Week 7 — Security](../week-07/LAB-01-iam.md)
