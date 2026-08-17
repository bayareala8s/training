# AWS Cost Control — Start / Stop / Destroy

## Scripts

| Script | What it does | Idle cost |
|--------|----------------|-----------|
| `./scripts/aws-start.sh` | Creates NAT + ALB + ECS, pushes images | **~$1.50–3/day** (Fargate + NAT + ALB) |
| `./scripts/aws-stop.sh` | Stops ECS, destroys NAT + ALB | **~$0–2/month** (ECR + DynamoDB only) |
| `./scripts/aws-destroy.sh` | Deletes everything | **$0** |

## Typical teaching week

```bash
# Monday — start class environment
./scripts/aws-start.sh

# Friday — stop to avoid weekend charges
./scripts/aws-stop.sh
```

## What aws-stop removes (cost drivers)

- NAT Gateway (~$0.045/hr)
- Application Load Balancer (~$0.0225/hr)
- ECS Fargate tasks (vCPU/memory per hour)

## What remains (low cost)

- VPC, subnets (free)
- ECR image storage (cents)
- DynamoDB on-demand with no traffic (cents)
- EventBridge bus (free tier)

## Full teardown

```bash
./scripts/aws-destroy.sh
# type: destroy
```

## Redeploy after code changes (platform running)

```bash
./scripts/aws-deploy.sh
```
