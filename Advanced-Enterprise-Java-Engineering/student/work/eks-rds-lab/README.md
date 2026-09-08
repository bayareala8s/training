# Optional lab: EKS + shared RDS (start / stop)

This is **not** the required AEJE student apply. Do not add NAT, EKS, or RDS on
the graded path. This folder is an optional same-day demo.

**Yes — this lab reuses the ECS lab’s RDS.** One VPC, one Postgres, two fronts
(ECS ALB and an EKS NLB). Avery’s rows are the same table.

| Destroy | What goes away |
| --- | --- |
| `./stop.sh` (this folder) | EKS cluster, node, NLB, extra 5432 SG rule |
| `../ecs-rds-lab/stop.sh` | VPC, RDS, ECS, ALB, ECR, secrets |

Always stop **EKS first**. The ECS stop script refuses if this state file still
has resources.

## What you get

- EKS 1.31 in the **existing** `10.20.0.0/16` public subnets
- One `t3.small` managed node, public IP, **no NAT**
- Same OCI image as ECS (`baypay/payment-service-ecs-demo:<tag>`)
- Spring profile **`eks`** (not `prod`) so Avery still seeds
- Kubernetes Secret from the existing Secrets Manager JSON
- `Service` type LoadBalancer (NLB :80 → pod :8080, liveness path)
- Heap from the image: `MaxRAMPercentage=75` — never `-Xmx` = 512 MiB

## Cost briefing

The EKS **control plane is ~$0.10/hour** from the moment the cluster is ACTIVE.
That is larger than the Fargate task. One `t3.small` and the NLB add more. RDS
is already billed by the ECS lab — this overlay does not create a second
database.

Same-day destroy. `Expiration` tags do not delete anything.

## Prerequisites

- A finished `../ecs-rds-lab` apply (VPC + RDS + pushed image)
- `aws`, `terraform` (>= 1.5), `kubectl`
- IAM that can create EKS, a node group, and a security-group rule on the RDS SG

## Cycle

```bash
cd student/work/ecs-rds-lab && ./start.sh    # if RDS is not already up
cd ../eks-rds-lab
./start.sh
# demo Swagger on the printed NLB DNS
./stop.sh
cd ../ecs-rds-lab && ./stop.sh               # only after EKS is gone
```

Laptop URL stays `http://localhost:8080`. ECS ALB and this NLB can both be live
against the same `customerId`.
