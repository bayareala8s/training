# Capstone Option 3 — Multi-Region DR Infrastructure

**Track:** Active-passive disaster recovery  
**Status:** Reference implementation (ready to apply)

## Business problem

Critical workloads need a **documented failover path** to a second region with matching network foundations and a clear state/config strategy.

## Design

| Role | Region | Stack | CIDR | State key |
|------|--------|-------|------|-----------|
| Primary | `us-west-2` | `terraform/environments/primary` | 10.60.0.0/16 | `capstone/option-03/primary/...` |
| Secondary (DR) | `us-east-1` | `terraform/environments/secondary` | 10.70.0.0/16 | `capstone/option-03/secondary/...` |

Pattern: **active-passive** — separate state per region (clear blast radius). Failover is runbook-driven (tabletop acceptable for cohort).

## Deliverables

| Requirement | Location |
|-------------|----------|
| Primary + secondary regions | `primary/` + `secondary/` stacks |
| State / failover strategy | [docs/failover-strategy.md](docs/failover-strategy.md) |
| Failover / failback runbook | [docs/runbooks/failover.md](docs/runbooks/failover.md) |
| Security / cost | `docs/` |
| CI | `.github/workflows/terraform-ci.yml` |

## Quick start

```bash
# Primary (us-west-2)
cd capstone/option-03-multi-region-dr/terraform/environments/primary
cp backend.hcl.example backend.hcl && cp terraform.tfvars.example terraform.tfvars
terraform init -backend-config=backend.hcl
terraform apply -var-file=terraform.tfvars

# Secondary DR (us-east-1)
cd ../secondary
cp backend.hcl.example backend.hcl && cp terraform.tfvars.example terraform.tfvars
terraform init -backend-config=backend.hcl
terraform apply -var-file=terraform.tfvars
```

## Cost control

Two regions ≈ 2× compute/NAT. Prefer:

```bash
enable_lab_compute = false   # in tfvars for demos
make lab-pause               # stops tagged EC2 in configured region (run per region)
```

For secondary region pause:

```bash
AWS_REGION=us-east-1 make lab-stop
```
