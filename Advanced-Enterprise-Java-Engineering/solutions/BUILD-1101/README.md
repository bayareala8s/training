# BUILD-1101 — Instructor solution

**Do not share these files with students before they submit a completed checklist.**

This folder is the answer key for deploying `payment-service` on **ECS/Fargate** behind an ALB in `us-west-2`. Students are **not** required to `terraform apply`. `terraform validate` from this directory must succeed after `terraform init`.

## Files

| File | Role |
|---|---|
| [versions.tf](versions.tf) | AWS provider `>= 5`, region from `var.region` |
| [variables.tf](variables.tf) | `region` default `us-west-2`, tags, image URI |
| [main.tf](main.tf) | VPC (public only), ECR, ALB, ECS/Fargate 0.25 vCPU / 512 MiB |
| [outputs.tf](outputs.tf) | ALB DNS, ECR URL, cluster/service names |

A student tree that matches the contracts (health path, `containerPort = 8080`, no NAT, no EKS, no RDS, tags) passes even if resource names differ.

## What the starter got wrong

- `aws_lb_target_group.pay` had **no** `health_check` block. The provider default path is `/`. Spring Boot on `payment-service` returns **404** on `/` (BUILD-305 / ACCOUNT.md). That is the INCIDENT-1104 symptom if anyone applies the starter.
- `portMappings` omitted `containerPort`. The process port is **8080**.

The starter was valid-looking HCL. It was not the ACCOUNT.md contract.

## Required contracts

```text
region:     us-west-2
subnets:    public only + IGW; assign_public_ip = true
forbidden:  NAT Gateway, EKS, RDS, always-on EC2
cpu/memory: 256 / 512 (0.25 vCPU / 0.5 GB)
port:       containerPort = 8080
health:     path = /actuator/health/liveness  matcher = 200  port = 8080
image:      immutable tag, never :latest
secrets:    no BAYPAY_DB_* plaintext (SECURITY-1103 injects Secrets Manager)
profile:    SPRING_PROFILES_ACTIVE=local (H2) so apply does not need RDS
tags:       Course=AEJE Module=11 Lab=BUILD-1101 Environment=student Expiration=
```

## Checklist (same as the student lab)

- [x] `health_check.path` is `/actuator/health/liveness`, not `/`
- [x] `containerPort = 8080`
- [x] No `aws_nat_gateway`, no EKS, no RDS
- [x] Fargate cpu `256` / memory `512`
- [x] Tags include Course, Module, Lab, Environment, Expiration
- [x] Region default `us-west-2`
- [x] Separate execution role and task role (task role stays empty here)
- [x] No password in the task definition

## Optional apply

Not required. If a student applies, treat it as extra. Destroy **the same day**: ALB, listener, target group, ECS service, cluster, task definition, ECR images (`force_delete` is set), log group, VPC. An idle ALB still bills.

```bash
cd solutions/BUILD-1101
terraform init
terraform validate
# apply is extra credit — estimate cost first
```

## Diagram

AEJE-D-048: merchants → ALB → target group (liveness on 8080) → Fargate task → ECR image. Secrets stay out of this lab’s task JSON.

## Scoring notes

Full marks require the health path, port 8080, public-only VPC, and no NAT/EKS/RDS. Leaving path `/` fails Technical accuracy and is the INCIDENT-1104 defect. Optional `terraform apply` neither raises nor lowers the score. Opening this folder before editing the starter fails Diagnostic method.
