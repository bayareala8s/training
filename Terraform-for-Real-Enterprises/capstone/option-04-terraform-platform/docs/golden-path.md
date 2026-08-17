# Golden Path — Service Teams

## Who this is for

Teams that need a **dev VPC + private app host** without designing networking from scratch.

## Steps

1. Copy `examples/service-team-app` into your service repo (or reference modules by Git tag).
2. Set `owner` and unique `name_prefix` / CIDR (ask platform for CIDR allocation).
3. Copy CI workflow from `ci-templates/terraform-consumer.yml`.
4. Open PR → CI validates → approved apply to sandbox.
5. Tag cost owner; run `make lab-pause` equivalent after demos.

## Allowed customizations

| OK | Not OK without platform review |
|----|--------------------------------|
| instance_type within t3.* | Public SSH 0.0.0.0/0 |
| Extra tags | Disable flow logs |
| CIDR from allocated range | NAT Gateway in sandbox without cost approval |

## Support

File issues with: plan output, `owner` tag, environment name.
