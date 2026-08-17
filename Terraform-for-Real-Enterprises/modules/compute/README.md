# Compute Module (Enterprise Lab)

Optional lab EC2 instance in a private subnet with egress-only security group and IMDSv2.

## Usage

```hcl
module "compute" {
  source = "../../../../modules/compute"

  name_prefix   = "${var.project_name}-${var.environment}"
  subnet_id     = module.vpc.private_subnet_ids[0]
  instance_type = var.instance_type
  tags          = local.lab_tags
}
```

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `name_prefix` | Prefix for security group and instance names | yes |
| `subnet_id` | Private subnet ID for the lab instance | yes |
| `instance_type` | EC2 type (default `t3.micro`) | no |
| `tags` | Tags merged onto all resources | yes |

## Outputs

| Name | Description |
|------|-------------|
| `instance_id` | Lab EC2 instance ID |
| `security_group_id` | Lab security group ID |

## Cost control

Instances are tagged `Course=terraform-enterprise` and are stopped by:

```bash
make lab-stop    # stop only
make lab-pause   # stop + destroy NAT Gateway (prod)
```

## Security

- No inbound rules on the lab security group (egress only)
- `http_tokens = required` (IMDSv2)
