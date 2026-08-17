# Spoke Interface — Shared Services Capstone

Spokes consume hub outputs; they do **not** recreate the hub VPC.

## Hub outputs (contract)

| Output | Use |
|--------|-----|
| `hub_vpc_id` | Peering / TGW attachment target |
| `hub_private_subnet_ids` | Shared services placement |
| `hub_vpc_cidr` | Route tables on spoke |
| `platform_log_group_name` | App log shipping target |
| `tgw_attachment_pattern` | Documented attachment steps |

## Lab mode (this repo)

1. Deploy hub; note `terraform output`.
2. Deploy spoke-dev as a separate VPC (simulates spoke account).
3. Optional stretch: create VPC peering and routes using hub CIDR.

## Production pattern (Transit Gateway)

```text
1. Create TGW in shared-services account
2. Attach hub VPC
3. Attach spoke VPCs (RAM share TGW to workload accounts)
4. Associate / propagate route tables
5. Publish subnet IDs via SSM Parameter Store or Terraform remote state data source
```

### Remote state data source (consumer example)

```hcl
data "terraform_remote_state" "hub" {
  backend = "s3"
  config = {
    bucket = "bayareala8s-terraform-state"
    key    = "capstone/option-02/hub/terraform.tfstate"
    region = "us-west-2"
  }
}

# Example use:
# cidr = data.terraform_remote_state.hub.outputs.hub_vpc_cidr
```

## Non-goals for cohort lab

- Full TGW + RAM (optional stretch; costs more)
- Cross-region hub
