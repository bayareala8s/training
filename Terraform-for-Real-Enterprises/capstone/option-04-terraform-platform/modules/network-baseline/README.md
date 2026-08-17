# Network Baseline (platform wrapper)

Opinionated VPC for internal service teams. Implements course `modules/vpc` with platform defaults.

## Usage

```hcl
module "network" {
  source = "../../modules/network-baseline"

  name_prefix = "payments-dev"
  vpc_cidr    = "10.80.0.0/16"
  owner       = "payments-team"
}
```
