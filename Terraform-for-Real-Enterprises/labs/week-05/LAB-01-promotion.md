# Lab 5.1 — Environment Promotion

**Duration:** 2–3 hours · **Week 5**

## Objectives

- Apply same modules to dev → test → prod with different tfvars
- Document promotion checklist

## Steps

### 1. Configure test environment

```bash
cd labs/shared/environments/test
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
# key = environments/test/terraform.tfstate
make init ENV=test
make plan ENV=test
make apply ENV=test
```

### 2. Promotion checklist

Create `docs/runbooks/environment-promotion.md`:

1. PR approved for module version bump
2. Plan in test; peer review
3. Apply test; smoke test
4. Plan prod; change advisory
5. Apply prod during window

### 3. Compare variables

| Variable | dev | test | prod |
|----------|-----|------|------|
| vpc_cidr | 10.10.0.0/16 | 10.20.0.0/16 | 10.30.0.0/16 |
| enable_nat_gateway | false | false | true |

## Deliverable

Promotion runbook + successful test apply.

## Next

[Lab 5.2 — Simulate drift](LAB-02-drift.md)
