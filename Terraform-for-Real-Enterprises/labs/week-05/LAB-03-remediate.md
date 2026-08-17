# Lab 5.3 — Remediate Drift

**Duration:** 1–2 hours · **Week 5**

## Objectives

- Choose remediation: Terraform apply vs import vs refresh-only
- Prevent recurrence

## Steps

### 1. Remediation strategies

| Situation | Action |
|-----------|--------|
| Console change should be kept | Update `.tf` code, then apply |
| Console change is wrong | `terraform apply` to revert |
| Resource exists but not in state | `terraform import` |
| State stale | `terraform refresh` or plan carefully |

### 2. Apply fix

```bash
make apply ENV=dev
```

### 3. Complete drift report

Template: [docs/templates/drift-report.md](../../docs/templates/drift-report.md)

### 4. Prevention

- Disable console edits in prod (policy)
- CI plan on schedule (nightly drift job — document as stretch goal)

## Deliverable

Completed `docs/drift-report-week05.md`.

## Next

[Week 6 — Recovery](../week-06/LAB-01-failed-deploy.md)
