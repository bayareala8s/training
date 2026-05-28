# Lab 4.1 — GitHub Actions Terraform CI

**Duration:** 3 hours · **Week 4**

## Objectives

- Add workflow: fmt, validate, plan on pull request
- Use course workflow template

## Steps

### 1. Copy workflow

```bash
mkdir -p .github/workflows
cp starter-templates/github-actions/terraform-ci.yml .github/workflows/terraform-ci.yml
```

Or use [labs/week-04/workflows/terraform-ci.yml](workflows/terraform-ci.yml).

### 2. Configure for your fork

Edit `WORKING_DIRECTORY` and Terraform version.

### 3. OIDC (recommended)

Follow [labs/week-04/docs/oidc-setup.md](docs/oidc-setup.md) to create `github-terraform` IAM role.

### 4. Open test PR

```bash
git checkout -b week-04-ci
# small change in modules/vpc/README.md
git commit -am "test: trigger CI"
git push -u origin week-04-ci
```

Verify workflow runs on GitHub.

## Deliverable

Link to green CI run on PR.

## Next

[Lab 4.2 — Plan/Apply gates](LAB-02-approval-gates.md)
