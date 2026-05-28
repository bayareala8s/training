# Lab 3.2 — Compose Networking Modules

**Duration:** 2 hours · **Week 3**

## Objectives

- Wire `modules/vpc` + `modules/compute` in environment stack
- Pass outputs → inputs correctly

## Steps

### 1. Trace data flow

In `labs/shared/environments/dev/main.tf`:

- `module.vpc.private_subnet_ids[0]` → `module.compute.subnet_id`

### 2. Add security group module (stretch)

Create `modules/security-group/` with rules for lab host (egress-only default).

### 3. Validate all environments

```bash
make validate
```

## Deliverable

Validation passes for dev, test, prod configs.

## Next

[Lab 3.3 — Publish module](LAB-03-publish.md)
