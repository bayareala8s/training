# Capstone Option 4 — Internal Terraform Platform

**Track:** Module library + golden path for internal teams  
**Status:** Reference implementation (ready to use)

## Business problem

Application teams need a **blessed path** to provision network + compute without forking raw VPC code. Platform engineering versions modules and ships a reusable CI template.

## Deliverables

| Requirement | Location |
|-------------|----------|
| Module library (≥2 modules) | `modules/network-baseline`, `modules/app-host` (wrappers around course modules) |
| Versioning | [modules/CHANGELOG.md](modules/CHANGELOG.md) + tag guidance |
| Golden path docs | [docs/golden-path.md](docs/golden-path.md) |
| Reusable CI template | [ci-templates/terraform-consumer.yml](ci-templates/terraform-consumer.yml) |
| Example consumer | `examples/service-team-app/` |
| Security / cost | `docs/` |

## Module map

```text
modules/
├── network-baseline/   # opinionated VPC (NAT instance default)
└── app-host/           # private EC2 lab host on network-baseline outputs
```

Wrappers pin interfaces for service teams; underlying implementation reuses course `modules/vpc` and `modules/compute`.

## Quick start (as a service team)

```bash
cd capstone/option-04-terraform-platform/examples/service-team-app
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
terraform init -backend-config=backend.hcl
terraform apply -var-file=terraform.tfvars
```

## Platform team versioning

```bash
git tag -a platform-modules/v1.0.0 -m "Initial platform module release"
# Consumers: source = "...?ref=platform-modules/v1.0.0"
```
