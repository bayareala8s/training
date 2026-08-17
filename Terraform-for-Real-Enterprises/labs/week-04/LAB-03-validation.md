# Lab 4.3 — Infrastructure Validation

**Duration:** 2 hours · **Week 4**

## Objectives

- Run `tflint` and `checkov` in CI or locally
- Fix or document findings

## Steps

### 1. Local validation

```bash
cd modules/vpc
tflint --init && tflint
checkov -d . --framework terraform
```

### 2. Add CI step

See [workflows/terraform-ci.yml](workflows/terraform-ci.yml) `security` job.

### 3. Remediation log

Create `docs/security/week-04-ci-findings.md` with:

| Check | Severity | Action |
|-------|----------|--------|
| ... | ... | fixed / accepted risk |

## Deliverable

Findings document + passing (or justified) CI.

## Next

[Week 5 — Drift](../week-05/LAB-01-promotion.md)
