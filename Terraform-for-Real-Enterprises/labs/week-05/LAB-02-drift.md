# Lab 5.2 — Simulate Infrastructure Drift

**Duration:** 2 hours · **Week 5**

## Objectives

- Introduce manual console change
- Detect drift with `terraform plan`

## Steps

### 1. Apply baseline dev

```bash
make apply ENV=dev
```

### 2. Manual drift

In AWS Console:

- Change a security group rule, OR
- Change an EC2 instance tag not managed by Terraform, OR
- Stop an instance without Terraform

### 3. Detect drift

```bash
make plan ENV=dev
```

Save plan output showing changes.

### 4. Optional: driftctl

```bash
# if installed
driftctl scan --from terraform.tfstate
```

## Deliverable

Start `docs/drift-report-week05.md` with plan output analysis.

## Next

[Lab 5.3 — Remediate](LAB-03-remediate.md)
