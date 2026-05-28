# VPC Module (Enterprise Lab)

Production-style VPC with public/private subnets, optional NAT Gateway or **NAT instance** (stoppable via `scripts/aws`).

## Usage

```hcl
module "vpc" {
  source = "../../modules/vpc"

  name_prefix        = "bal8s-dev"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-west-2a", "us-west-2b"]
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24"]
  enable_nat_gateway = false
  use_nat_instance   = true
  tags               = local.lab_tags
}
```

## Inputs

See `variables.tf`.

## Outputs

See `outputs.tf`.
