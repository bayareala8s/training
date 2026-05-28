# Lab 7.3 — Compliance Checks in CI

**Duration:** 2–3 hours · **Week 7**

## Objectives

- Run Checkov/tflint in CI
- Produce security validation report

## Steps

### 1. Run Checkov locally

```bash
checkov -d modules/ -d labs/shared/ --framework terraform -o cli
checkov -d modules/ -d labs/shared/ --framework terraform -o json > /tmp/checkov.json
```

### 2. Configure [.checkov.yml](.checkov.yml)

```yaml
quiet: false
compact: true
framework:
  - terraform
skip-check:
  # Document accepted risks with ticket/id
  # - CKV_AWS_130
```

### 3. Security report

Create `docs/security/week-07-validation-report.md`:

- Tool versions
- Pass/fail counts
- Remediated vs accepted findings

## Deliverable

Security validation report + CI green or documented exceptions.

## Next

[Week 8 Capstone](../week-08/LAB-capstone.md)
