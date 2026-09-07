# BUILD-1202 — starter vs AEJE-D-055 / ACCOUNT.md (before edit)

| Gap | Starter |
|---|---|
| `modules/ecr` `aws_ecr_repository` | `main.tf` comment only |
| `modules/ecr` URL/ARN outputs | Empty |
| `modules/ecs_service` `container_port` default 8080 | **Missing** (only `name`) |
| `modules/ecs_service` `health_check_path` | **Missing** |
| `modules/ecs_service` `image`, `tags` | **Missing** |
| Log group `/ecs/<name>` | **Missing** |
| Contract outputs + `service_contract` map | **Missing** |
| Root passes port / health / image (not `:latest`) | Calls `ecs_service` with **name + region only** |
| Root outputs | Empty |
| Root/module `required_providers` + `region` us-west-2 | Present — keep |
| No ALB / `aws_ecs_service` | Correct — keep |

Fixes in `work/` only. Starter left hollow.
