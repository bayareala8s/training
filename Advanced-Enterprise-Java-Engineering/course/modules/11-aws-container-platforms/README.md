# Module 11 — AWS Container Platforms

**Duration:** ~4 hours of lessons plus 5 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Run BayPay `payment-service` on ECR + ECS/Fargate in `us-west-2`  
**Portfolio artifact:** AWS platform notes from [student/worksheets/PF-aws-platform.md](../../../student/worksheets/PF-aws-platform.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, hostname, image tag, and AWS identifier you see is synthetic. **Real AWS bills if you apply.** Use a student sandbox you are allowed to spend in.

**Delivery note:** **live apply is optional.** Paper architecture plus `terraform validate` is enough to pass if you cannot spend. If you do apply, **destroy after the lab**. Do not leave an ALB overnight. **EKS is literacy and [ARCHITECT-1102](../../../labs/ARCHITECT-1102/README.md), not the student apply default.** The compute default is **ECS on Fargate**. Do not stand up NAT Gateway, EKS, OpenSearch, or multi-AZ RDS “for realism” in a 90-minute lab.

---

## Business context

Module 9 packaged `payment-service` as an OCI image. Module 10 scheduled that image as Pods in `baypay-prod` behind Ingress or OpenShift Route `payment-route`. This module **relocates the same Java 21 / Spring Boot 3.5.5 process** onto AWS container services. Harbor Bike Co still charges Avery Chen `$84.00` through `POST /api/v1/payments`. The application is still `reference-apps/baypay`. The control plane is now **Amazon ECS**. The image catalog is **Amazon ECR** in **`us-west-2`**.

AWS is **one valid home**, not the only correct home. A BayPay estate that already runs well on Kubernetes or OpenShift (Module 10) does not become wrong because this module uses Fargate. [ARCHITECT-1102](../../../labs/ARCHITECT-1102/README.md) exists so you can say when ECS, EKS, or OpenShift wins — and when you should stay where you are.

The locked AWS notes live in [datasets/baypay-aws/ACCOUNT.md](../../../datasets/baypay-aws/ACCOUNT.md). Reuse those names in every diagram, lab, and interview answer:

| Field | Locked value |
|---|---|
| Region | `us-west-2` |
| App | `payment-service` (Java 21, Spring Boot 3.5.5) |
| Image | ECR `baypay/payment-service:<tag>` — never `:latest` |
| Port | `8080` |
| Health | `/actuator/health/liveness`, `/actuator/health/readiness` |
| Secrets | `BAYPAY_DB_*` from Secrets Manager — never in task-def JSON in git |
| Compute default | **ECS on Fargate** (no EKS, no NAT Gateway, no always-on EC2 unless a lab discloses cost) |
| VPC (student apply) | Public subnets + IGW for Fargate + ALB. Document the security trade-off. |
| Teaching ALB host | `pay-alb-student.baypay.example` (apply uses the AWS-generated DNS name) |
| Tags | `Course=AEJE`, `Module`, `Lab`, `Environment=student`, `Expiration` (ISO date) |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |

On-call names: **Riley Okonkwo** (application), **Priya Nair** (SRE), **Sam Okada** (platform), **Jordan Voss** (release). Payment happy path is still `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. An ALB target `healthy` is not that sentence.

---

## Learning objectives

After this module you can:

- Push and pin `baypay/payment-service:<tag>` in ECR (`us-west-2`) with immutable tags, scan-on-push, and no `:latest` in production.
- Write an ECS task definition and service for Fargate that listens on `8080`, and explain Fargate versus the EC2 launch type without recommending always-on instances for a student lab.
- Say when EKS wins versus ECS — and when Module 10’s Kubernetes or OpenShift remains the better home — without requiring a live EKS cluster.
- Front `payment-service` with an ALB (and know when an NLB or Route 53 name applies). Health checks must match Actuator, not `/` or `/health`.
- Separate the ECS **task role** from the **execution role**, and inject `BAYPAY_DB_*` from Secrets Manager with KMS — never from git.
- Use CloudWatch logs, metrics, and alarms as the AWS signal layer, not as a substitute for traces or correlation ids.
- Talk RDS and S3 literacy without creating RDS on a student apply.
- Scale Fargate tasks, price an idle ALB, tag `Expiration`, and destroy what you created.

---

## Prerequisites

- Modules 1–3: `payment-service`, Actuator probes, `BAYPAY_DB_*`, idempotency and correlation ids.
- Module 9 image contract: `eclipse-temurin:21-jre`, port `8080`, non-root UID, no `:latest`, secrets not in layers.
- Module 10: Deployment / Service / Ingress-or-Route in `baypay-prod`. You will map those objects onto ECS + ALB. You will **not** treat AWS as a replacement that invalidates OpenShift.
- L-7.6 / L-9.6 / L-10.5: do not set `-Xmx` equal to the task memory limit.
- Comfort reading JSON or HCL as desired state. You do **not** need a live AWS account to pass.

An AWS account is **useful, not required**. If you apply, estimate cost first. Prefer paper + `terraform validate` if you cannot spend.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional. Lessons teach **services and method**. They do not name the root cause of INCIDENT-1104.

| Id | Title | What it unlocks |
|---|---|---|
| [L-11.1](lessons/L-11.1.md) | Amazon ECR | Immutable tags, scan-on-push, no `:latest` |
| [L-11.2](lessons/L-11.2.md) | ECS and Fargate | Task definition, service, port `8080`, Fargate vs EC2 |
| [L-11.3](lessons/L-11.3.md) | Amazon EKS | When EKS wins; do not require a cluster |
| [L-11.4](lessons/L-11.4.md) | ALB, NLB, Route 53 | AEJE-D-053; health checks match Actuator |
| [L-11.5](lessons/L-11.5.md) | IAM, Secrets Manager, KMS | Task role vs execution role; `BAYPAY_DB_*` |
| [L-11.6](lessons/L-11.6.md) | CloudWatch | Logs, metrics, alarms — not traces |
| [L-11.7](lessons/L-11.7.md) | RDS and S3 | Literacy; student apply does not create RDS |
| [L-11.8](lessons/L-11.8.md) | Autoscaling and cost | Fargate scale, ALB idle cost, `Expiration` tags |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [BUILD-1101](../../../labs/BUILD-1101/README.md) | BUILD | Deploy BayPay on ECS/Fargate | L-11.1, L-11.2 |
| [ARCHITECT-1102](../../../labs/ARCHITECT-1102/README.md) | ARCHITECT | ECS vs EKS vs OpenShift | L-11.3 |
| [SECURITY-1103](../../../labs/SECURITY-1103/README.md) | SECURITY | IAM, secrets and KMS | L-11.5 |
| [INCIDENT-1104](../../../labs/INCIDENT-1104/README.md) | INCIDENT | Unhealthy ALB target | L-11.4, L-11.6 |
| [COST-1105](../../../labs/COST-1105/README.md) | COST | Cost optimization | L-11.8 |

Time-box BUILD and COST labs at 60–90 minutes. ARCHITECT-1102 is a paper decision; it does not apply EKS. INCIDENT-1104 shows **symptoms only**. Work the pack’s gates. Do not open `solutions/INCIDENT-1104/` until the worksheet has hypothesis, evidence, next investigation, stabilize, remediate, and comms. This module’s lessons do **not** name that pack’s cause.

If you apply: estimate cost before `terraform apply` or console clicks. ALB is dollars/day; Fargate is cents-to-dollars per hour at tiny CPU. **Delete** ALB, services, clusters, and ECR images you created. Empty ECR still has storage cost.

---

## Assessment and portfolio

1. Complete BUILD-1101, ARCHITECT-1102, SECURITY-1103, INCIDENT-1104, and COST-1105. Paper + `terraform validate` counts as complete for apply labs if you cannot spend.
2. Take [Q-11](../../quizzes/Q-11.md) when your cohort opens it.
3. Export the AWS platform decision and destroy evidence using [student/worksheets/PF-aws-platform.md](../../../student/worksheets/PF-aws-platform.md).

The worksheet is the Module 11 portfolio artifact. Module 12 will assume you can point at ECR + ECS/Fargate in `us-west-2` and defend Fargate as the default, EKS as a choice, and OpenShift as still valid.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/16-cloud-architecture/aws-fundamentals.md` and `docs/26-cost-and-finops/overview.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). They deepen region, shared-responsibility, and unit-cost ideas. This module stands alone without them.

---

## Guardrails

- Region is **`us-west-2`**. Do not invent `us-east-1` as the BayPay teaching default.
- Student apply default is **ECS on Fargate**. EKS is literacy and ARCHITECT-1102. Do not apply EKS, NAT Gateway, OpenSearch, or multi-AZ RDS in a 90-minute lab.
- Live apply is **optional**. Paper + `terraform validate` is enough to pass if you cannot spend. **Destroy after the lab.**
- Do not leave an ALB running overnight. Tag `Course=AEJE`, `Module`, `Lab`, `Environment=student`, `Expiration`.
- Do not commit access keys or put `BAYPAY_DB_*` in task-def JSON in git.
- Do not deploy `:latest`. Do not set `-Xmx` equal to the Fargate memory limit.
- Do not treat ECS as the only correct platform. Module 10 Kubernetes and OpenShift remain valid homes.
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`. Students should not need them to finish the work.
