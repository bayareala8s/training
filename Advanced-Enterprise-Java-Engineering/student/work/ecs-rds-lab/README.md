# Optional lab: ECS Fargate + RDS Postgres (start / stop)

This is **not** the required AEJE student apply. Capstone-3 and BUILD-1101 stay
Fargate-only: no NAT, no EKS, no RDS on the graded path.

This folder is a same-day demo you can turn **on** and **all the way off**.
`./stop.sh` runs `terraform destroy`. That is the only way the meter stops.

| Action | Still bills? |
| --- | --- |
| `desired_count = 0` | Yes — ALB, RDS, public IPv4, Secrets Manager |
| Stop the RDS instance in the console | Yes — allocated storage and the ALB |
| `Expiration` tag | No — tags do not delete anything |
| `./stop.sh` (`terraform destroy`) | No — stack is gone |

Region is **us-west-2**. Single-AZ `db.t3.micro`. No NAT Gateway. No Multi-AZ.
No EKS. Heap is `MaxRAMPercentage=75` on the JRE image — never
`-Xmx` equal to the 512 MiB task limit.

## What you get

- Public ALB `:80` → Fargate task `:8080` health `/actuator/health/liveness`
- One `payment-service` task, `256` CPU / `512` MiB, `assign_public_ip = true`
- Private RDS PostgreSQL 16, 20 GB, not internet-reachable
- JDBC URL / user / password from Secrets Manager (`valueFrom` JSON keys)
- Spring profile **`ecs`** (not `prod`) so Avery still seeds
- Immutable ECR tag — never `:latest`

Laptop URL stays `http://localhost:8080/api/v1/payments`. After start, use the
ALB DNS the script prints.

## Cost briefing (order of magnitude, us-west-2)

Leave this up only while you are showing it. A two-hour demo is a few dollars.
A forgotten week is mostly the **ALB** (~$16/month) plus **RDS** (instance +
20 GB) plus **public IPv4**.

| Piece | Why it costs |
| --- | --- |
| ALB | ~$0.0225/hour from the moment Phase 1 apply finishes |
| Fargate 256/512 | ~$0.01–0.015/hour while `desired_count = 1` |
| RDS `db.t3.micro` + 20 GB | Largest compute/storage line; storage remains if you only “stop” the DB |
| Public IPv4 (ALB + task ENI) | Hourly after AWS’s IPv4 charge |
| Secrets Manager | One secret; `recovery_window_in_days = 0` so destroy can delete it |
| NAT / EKS / Multi-AZ | Not created. Do not add them for this demo. |

## Prerequisites

- AWS credentials that can create VPC, ECS, ECR, RDS, IAM, ALB, Secrets Manager
- `aws`, `terraform` (>= 1.5), `docker` (build `linux/amd64` even on Apple silicon)
- This course tree, Java 21 on the host (`./mvnw -DskipTests package`), and Docker

## Cycle

```bash
cd student/work/ecs-rds-lab
./start.sh          # Phase 1 RDS+ALB, image push, Phase 2 service (~15–20 min)
# demo against the printed ALB DNS
./stop.sh           # type DESTROY, or ./stop.sh -y
```

`start.sh` writes `generated.auto.tfvars` (gitignored) so destroy sees the same
image URI. Do not commit `*.tfstate`.

Avery customer id: `11111111-1111-1111-1111-111111111111`.
Active account: `22222222-2222-2222-2222-222222222221`.
`Idempotency-Key` is required on POST.

## If the target stays unhealthy

1. CloudWatch log group `/ecs/baypay-ecsrd/payment-service`
2. Confirm the task used profile `ecs` and received `BAYPAY_DB_*`
3. Confirm you pushed `linux/amd64` (an arm64 image will not start on X86_64 Fargate)
4. Still run `./stop.sh` if you are done — a broken stack bills the same as a working one
