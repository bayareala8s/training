# BUILD-1202 — Instructor solution

**Do not share these files with students before they submit a validate-green module tree.**

This folder is the answer key for reusable Terraform modules. Students are not required to `terraform apply`. Live ECS/ALB is out of scope.

## Files

| Path | Role |
|---|---|
| [provider.tf](provider.tf) | Root `required_providers.aws`, `variable "region"` default `us-west-2` |
| [main.tf](main.tf) | Calls `modules/ecr` and `modules/ecs_service` with port 8080 and liveness path |
| [modules/ecr/](modules/ecr/) | Immutable ECR repository |
| [modules/ecs_service/](modules/ecs_service/) | Log group plus `container_port` / `health_check_path` contract |

A student tree that matches contracts (two modules, port 8080, liveness path, region pin, validate) passes even if they named the health variable `health_path` or omitted the `:latest` validation block.

## What the starter got wrong

- `modules/ecr` had no repository and no outputs.
- `modules/ecs_service` declared only `name` — no port, no health path, no log group.
- Root `main.tf` did not pass port, health, or an immutable image.

The starter could look like a module tree. It did not encode ACCOUNT.md.

## Required contracts

```text
root + modules: required_providers { aws }; variable "region" default us-west-2
ecr:            aws_ecr_repository; outputs URL + ARN; prefer IMMUTABLE
ecs_service:    container_port default 8080
                health_check_path default /actuator/health/liveness
                cheap resource: aws_cloudwatch_log_group /ecs/<name>
image:          not :latest
scope:          no ALB, no aws_ecs_service, no NAT, no keys
validate:       terraform init -backend=false && terraform validate
```

## Diagram

AEJE-D-055: root in `us-west-2` calls ECR and `ecs_service`. The service module publishes port 8080 and the liveness path. It does not create an ALB.

## Scoring notes

Full marks require both modules, the port/health variables, region pin, and validate. Inlining ECR in the root and leaving `modules/ecs_service` empty fails Technical accuracy. Adding an ALB fails Cost. Opening this folder first fails Diagnostic method.
