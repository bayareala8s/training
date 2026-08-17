# Lab 4.2 — Plan → Review → Apply

**Duration:** 2 hours · **Week 4**

## Objectives

- Configure GitHub Environment protection for `dev` and `prod`
- Separate plan (PR) from apply (main + approval)

## Steps

### 1. GitHub Environment

Repository → Settings → Environments → New: `dev`, `prod`

- Required reviewers: 1 (instructor or peer)
- Deployment branches: `main` only for prod

### 2. Uncomment apply job

In `.github/workflows/terraform-ci.yml`, enable `apply` job with:

```yaml
environment: dev
```

### 3. Secrets vs OIDC

- **Never** store long-lived `AWS_ACCESS_KEY_ID` in repo secrets for production patterns
- Use OIDC `id-token: write` permission

## Deliverable

Screenshot of approval gate before apply.

## Next

[Lab 4.3 — Static analysis](LAB-03-validation.md)
