# BUILD-1101 — starter vs ACCOUNT.md (before edit)

Read starter, then ACCOUNT.md. Gaps before any HCL change:

| ACCOUNT.md contract | Starter |
|---|---|
| Health `/actuator/health/liveness` matcher 200 on 8080 | `aws_lb_target_group.pay` has **no** `health_check` → provider default **`/`** (Spring 404 → INCIDENT-1104) |
| Process / `containerPort` **8080** | `portMappings` has protocol only; **no `containerPort`** |
| Region `us-west-2` | Present (`variable.region`) |
| ECR `baypay/payment-service` immutable | Present |
| Fargate 256 / 512, desired 1, public + IGW, no NAT/EKS/RDS | Present (keep) |
| Tags Course/Module/Lab/Environment/Expiration | Present |
| No password in task env; profile `local` | Present (`SPRING_PROFILES_ACTIVE=local`) |
| Execution role ≠ task role; no AdministratorAccess | Present |

Jordan left an ALB that can mark targets unhealthy while the task is `RUNNING`. That is the incomplete file, not a reason to add NAT.

Fixes in this `work/` tree only. `labs/BUILD-1101/starter/` left for classmates.
