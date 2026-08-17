# Lab 3.3 — Publish Internal Module

**Duration:** 1–2 hours · **Week 3**

## Objectives

- Publish module via Git tag or Terraform Registry protocol
- Document upgrade path for consumers

## Steps

### Option A — Git source (common in enterprises)

```hcl
module "vpc" {
  source = "git::https://github.com/YOUR_ORG/tf-modules.git//vpc?ref=v1.0.0"
}
```

### Option B — Local path (this course repo)

```hcl
source = "../../../../modules/vpc"
```

### 1. Create CHANGELOG.md in modules/vpc

Document v1.0.0 features and breaking change policy.

### 2. Semantic versioning policy

Add `modules/vpc/CHANGELOG.md`:

- PATCH: bug fixes
- MINOR: backward-compatible inputs
- MAJOR: removed/changed required inputs

## Deliverable

`modules/vpc/CHANGELOG.md` + Git tag.

## Next

[Week 4 — CI/CD](../week-04/LAB-01-github-actions.md)
