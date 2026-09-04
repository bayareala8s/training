# BayPay AWS lab notes — Modules 11–12

**Fictional company. Real AWS bills if you apply.** Use a **student sandbox** account you are allowed to spend in. Destroy when the lab says so.

Students may read this file. Instructor incident RCAs live only under `solutions/`.

## Defaults

| Field | Value |
|---|---|
| Region | `us-west-2` |
| App | `payment-service` (Java 21, Spring Boot 3.5.5) |
| Image | `registry` / ECR `baypay/payment-service:<tag>` |
| Port | `8080` |
| Health | `/actuator/health/liveness`, `/actuator/health/readiness` |
| Secrets | `BAYPAY_DB_*` from Secrets Manager — never in task-def JSON in git |
| Compute default | **ECS on Fargate** (no EKS, no NAT Gateway, no always-on EC2 unless a lab discloses cost) |
| VPC | Public subnets only for student Fargate + ALB (internet egress via IGW). Document the security trade-off. |
| Tags | `Course=AEJE`, `Module`, `Lab`, `Environment=student`, `Expiration` (ISO date) |

## Cost rules

- Estimate and warn **before** `terraform apply` / console clicks.
- Prefer paper + `terraform validate` if you cannot spend.
- ALB ~ dollars/day; Fargate ~ cents-to-dollars per hour at tiny CPU; RDS is **out of scope** for student apply (use the local H2/Postgres story or a disclosed estimate).
- **Delete** ALB, services, clusters, and ECR images you created. Empty ECR still has storage cost.

## People and names (synthetic)

Avery Chen customer id `11111111-1111-1111-1111-111111111111`.  
Riley Okonkwo (app on-call), Priya Nair (SRE), Sam Okada (platform), Jordan Voss (release).

ALB example host: `pay-alb-student.baypay.example` (teaching; student apply uses the AWS-generated DNS name).

## What you must not do

- Apply EKS, NAT Gateway, OpenSearch, or multi-AZ RDS “for realism” in a 90-minute lab.
- Commit access keys or `changeme` as a production password.
- Leave an ALB running overnight.
- Treat ECS as “the only correct platform.” ARCHITECT-1102 exists so you can say when EKS or OpenShift wins.

## Optional PAKS

- Module 11: `docs/16-cloud-architecture/aws-fundamentals.md`, `docs/26-cost-and-finops/overview.md`
- Module 12: `docs/17-kubernetes-and-platform-engineering/platform-engineering-and-gitops.md`
