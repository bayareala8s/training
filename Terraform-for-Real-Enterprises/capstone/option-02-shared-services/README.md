# Capstone Option 2 — Shared Services Platform

**Track:** Centralized networking + monitoring  
**Status:** Reference implementation (ready to apply)

## Business problem

Workload teams need a **hub** for shared networking and logging, with a clear interface so spokes consume subnets / attachment patterns without reinventing VPC design.

## Deliverables map

| Requirement | Location |
|-------------|----------|
| Hub VPC | `terraform/environments/hub/` |
| Centralized logging / flow logs | Hub VPC module + `aws_cloudwatch_log_group.platform` |
| Consumable outputs for spokes | Hub `outputs.tf` + [docs/spoke-interface.md](docs/spoke-interface.md) |
| Spoke example | `terraform/environments/spoke-dev/` |
| CI | `.github/workflows/terraform-ci.yml` |
| Security / cost | `docs/` |

## Architecture

```text
Hub VPC 10.50.0.0/16
  ├── public / private subnets
  ├── NAT instance (lab)
  ├── VPC flow logs → CloudWatch
  └── platform log group

Spoke Dev 10.51.0.0/16
  └── documents TGW / peering attachment pattern (lab: separate VPC + interface docs)
```

## Quick start

```bash
cd capstone/option-02-shared-services/terraform/environments/hub
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
terraform init -backend-config=backend.hcl
terraform apply -var-file=terraform.tfvars

cd ../spoke-dev
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
terraform init -backend-config=backend.hcl
terraform apply -var-file=terraform.tfvars
```

## Cost control

```bash
make lab-pause   # from course root
```
