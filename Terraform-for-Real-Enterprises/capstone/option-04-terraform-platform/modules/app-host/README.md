# App Host (platform wrapper)

Private EC2 host for labs/services on a network-baseline subnet.

## Usage

```hcl
module "app" {
  source = "../../modules/app-host"

  name_prefix = "payments-dev"
  subnet_id   = module.network.private_subnet_ids[0]
  owner       = "payments-team"
}
```
