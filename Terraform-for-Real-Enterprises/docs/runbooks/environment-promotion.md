# Environment Promotion Runbook

## Promotion path

```text
dev (10.10.0.0/16) → test (10.20.0.0/16) → prod (10.30.0.0/16)
```

## Pre-promotion checklist

- [ ] Module version tagged and CHANGELOG updated
- [ ] `terraform plan` clean in source environment
- [ ] Peer review on PR
- [ ] Security scan (Checkov) reviewed
- [ ] Change window agreed for prod

## Steps

1. Merge module changes to `main`
2. `make plan ENV=test` → review → `make apply ENV=test`
3. Smoke test (VPC, connectivity, tags)
4. `make plan ENV=prod` → change advisory → approved apply
5. Post-deploy: `make lab-status` and `terraform plan` (no drift)

## Rollback

See [terraform-recovery.md](terraform-recovery.md).
