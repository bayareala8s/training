# Shared Environment Stacks

Terraform environments for **Terraform for Real Enterprises** labs. Same modules, different `terraform.tfvars` per environment—enterprise promotion pattern.

## Layout

| Environment | CIDR (default) | NAT | Lab EC2 | State key suffix |
|-------------|----------------|-----|---------|------------------|
| **dev** | `10.10.0.0/16` | NAT instance | yes | `environments/dev/terraform.tfstate` |
| **test** | `10.20.0.0/16` | NAT instance | yes | `environments/test/terraform.tfstate` |
| **prod** | `10.30.0.0/16` | NAT Gateway | no (default) | `environments/prod/terraform.tfstate` |

## First-time setup (each environment)

```bash
cd labs/shared/environments/<env>
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
# Edit owner and paths as needed

cd ../../../..   # repo root
make init ENV=<env>
make plan ENV=<env>
make apply ENV=<env>
```

## Promotion workflow (Week 5)

1. Change modules or tfvars in a PR
2. `make plan ENV=test` → peer review → `make apply ENV=test`
3. `make plan ENV=prod` → change window → `make apply ENV=prod`

See [docs/runbooks/environment-promotion.md](../../../docs/runbooks/environment-promotion.md).

## Cost control

```bash
make lab-pause    # stop EC2 + destroy prod NAT Gateway (~zero hourly cost)
make lab-resume   # recreate NAT GW + start EC2
make lab-status   # show billing warnings
```

## Modules used

- [modules/vpc](../../../modules/vpc/README.md)
- [modules/compute](../../../modules/compute/README.md)
