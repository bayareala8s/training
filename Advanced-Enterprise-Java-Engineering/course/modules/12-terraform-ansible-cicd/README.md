# Module 12 — Terraform, Ansible and CI/CD

**Duration:** ~3 hours of lessons plus 5 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Automate BayPay environments and releases  
**Portfolio artifact:** Terraform modules and CI/CD design from [student/worksheets/PF-iac.md](../../../student/worksheets/PF-iac.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, image tag, Terraform snippet, and pipeline log you see is synthetic. Do not treat this pack as a real employer’s release system.

**Delivery note:** the grade bar for infrastructure is **`terraform validate`** on disk. `terraform plan` is useful when you have credentials. `terraform apply` is **optional**, costs real money in a student sandbox, and must be destroyed when the lab says so. Prefer paper plus validate if you cannot spend. See [datasets/baypay-aws/ACCOUNT.md](../../../datasets/baypay-aws/ACCOUNT.md).

---

## Business context

Module 11 put `payment-service` on **ECS on Fargate** in `us-west-2`: image in ECR `baypay/payment-service:<tag>`, port `8080`, health on `/actuator/health/liveness` and `/actuator/health/readiness`, secrets from Secrets Manager — never in task-def JSON in git. This module **automates** that estate and the leftover Liberty VMs you have not yet retired.

Harbor Bike Co still charges Avery Chen `$84.00` through `POST /api/v1/payments`. The process is the same Java 21 / Spring Boot 3.5.5 modular monolith in `reference-apps/baypay`. The difference is the release path. Jordan Voss does not copy a JAR onto `Pay2`. Jordan merges a pull request. CI runs `./mvnw test` on **Java 21**. A green main publishes an **immutable** image tag to ECR. Terraform changes desired AWS state. Ansible — if anything — templates `server.xml` and env on a leftover Liberty host. Then you **validate health before you cut** merchants, and you **roll back** if the new revision is not Ready.

The locked pipeline is one sentence:

**Git → CI test → image → Terraform → (Ansible for leftover VM / Liberty config) → validate / rollback.**

| Stage | Owner (synthetic) | What “done” means |
|---|---|---|
| Git | Jordan Voss | Short-lived PR into `main`; no force-push to `main` |
| CI test | pipeline | `./mvnw test` on JDK 21; secrets scan; no publish yet |
| Image | pipeline + ECR | `baypay/payment-service:<immutable-tag>` in `us-west-2`; never `:latest` |
| Terraform | Sam Okada | Modules + remote state in production; **validate** is the student bar |
| Ansible | leftover estate | `server.xml` shape + env on a Liberty VM you still have — not the Fargate task |
| Validate / rollback | Riley / Priya | Actuator + ALB healthy before cut; ECS circuit breaker / prior Terraform revision |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |

On-call names: **Riley Okonkwo** (application), **Priya Nair** (SRE), **Sam Okada** (platform), **Jordan Voss** (release). Payment happy path is still `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. A green pipeline is not that sentence.

Compute default stays **ECS on Fargate**. Do not apply EKS, NAT Gateway, or RDS “for realism.” Public subnets plus IGW are the student VPC trade-off documented in ACCOUNT.md. Traditional `BayPayCell` / `dmgr-east` is the estate you leave; Ansible does not recreate a cell.

---

## Learning objectives

After this module you can:

- Run a trunk-based Git workflow with protected `main`, short-lived PRs, conventional reviews, and no force-push to `main`.
- Gate every merge on `./mvnw test` under **Java 21**, and refuse to publish an image from a red build.
- Push `baypay/payment-service:<tag>` to ECR in `us-west-2` with **immutable tags** and no production `:latest`.
- Explain Terraform state, providers, and modules well enough to `terraform validate` a student stack and say what `apply` would cost.
- Separate **IaC** (Terraform creates AWS) from **config automation** (Ansible templates leftover Liberty `server.xml` / env).
- Validate health before a merchant cut and roll back with ECS circuit breaker and/or a prior Terraform revision — without writing an INCIDENT-1205 RCA in the lesson.

---

## Prerequisites

- Modules 1–10, especially `./mvnw` (GETTING_STARTED), L-6.4 (`BAYPAY_DB_*` / `server.xml`), L-9.3 (no `:latest`), L-10.6 (rollout / undo literacy).
- Module 11 platform contract in [ACCOUNT.md](../../../datasets/baypay-aws/ACCOUNT.md): region `us-west-2`, ECS/Fargate default, ECR `baypay/payment-service:<tag>`, port `8080`, Secrets Manager for `BAYPAY_DB_*`. If Module 11 lessons are still in flight, ACCOUNT.md is enough.
- JDK 21 on `PATH` or `JAVA_HOME`. You do **not** need a global Maven install. The reference app ships `./mvnw`.
- Comfort reading HCL, YAML, and a pull request. A live AWS account is **not** required to pass.

You do **not** need Ansible against a real VM, a licensed Liberty install, or GitHub Actions minutes on a private org. Paper plus `terraform validate` plus local `./mvnw test` is enough.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional. Lessons teach **pipeline and method**. They do not name the root cause of INCIDENT-1205.

| Id | Title | What it unlocks |
|---|---|---|
| [L-12.1](lessons/L-12.1.md) | Git workflow | Trunk / PR, protected `main`, conventional reviews, AEJE-D-054 |
| [L-12.2](lessons/L-12.2.md) | CI build and test | `./mvnw test`, Java 21, no publish on red |
| [L-12.3](lessons/L-12.3.md) | Container publishing | ECR, immutable tags, no `:latest` |
| [L-12.4](lessons/L-12.4.md) | Terraform foundations and modules | State, providers, modules, AEJE-D-055 |
| [L-12.5](lessons/L-12.5.md) | Configuration automation | Ansible for leftover Liberty; IaC vs config, AEJE-D-058 |
| [L-12.6](lessons/L-12.6.md) | Deployment validation and rollback | Health before cut; ECS circuit breaker; Terraform rollback |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [BUILD-1201](../../../labs/BUILD-1201/README.md) | BUILD | Terraform AWS environment | L-12.4 |
| [BUILD-1202](../../../labs/BUILD-1202/README.md) | BUILD | Reusable Terraform modules | L-12.4 |
| [BUILD-1203](../../../labs/BUILD-1203/README.md) | BUILD | Configuration automation | L-12.5 |
| [BUILD-1204](../../../labs/BUILD-1204/README.md) | BUILD | CI/CD pipeline | L-12.1, L-12.2, L-12.3 |
| [INCIDENT-1205](../../../labs/INCIDENT-1205/README.md) | INCIDENT | Failed deployment and rollback | L-12.6 |

Time-box BUILD labs at 60–90 minutes. INCIDENT-1205 at 45–75 minutes. Student incident guide shows **symptoms only**. Work the pack’s gates. Do not open `solutions/INCIDENT-1205/` until the worksheet has hypothesis, evidence, next investigation, stabilize, remediate, and comms.

`terraform validate` is the AWS lab bar. Apply only in a sandbox you may spend in, after a written cost estimate, with tags `Course=AEJE`, `Module`, `Lab`, `Environment=student`, `Expiration`. Delete ALB, services, clusters, and ECR images you created. BUILD-1203 and BUILD-1204 do not require `terraform apply`.

Treat a failed ECS deployment or a red pipeline as a *symptom class*, not a closed RCA. Quote *this* pack’s evidence. A lucky label that matches the title does **not** max Diagnostic method.

---

## Assessment and portfolio

1. Complete BUILD-1201 through BUILD-1204 and INCIDENT-1205 with gated evidence on the incident.
2. Take [Q-12](../../quizzes/Q-12.md) when your cohort opens it.
3. Export Terraform module boundaries and the CI/CD design using [student/worksheets/PF-iac.md](../../../student/worksheets/PF-iac.md).

The worksheet is the Module 12 portfolio artifact. Module 13 will assume you can point at the Git → test → image → Terraform path and explain why a green pipeline is not a merchant-healthy cut.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/17-kubernetes-and-platform-engineering/platform-engineering-and-gitops.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). It deepens desired-state apply and GitOps. This module stands alone without it.

---

## Guardrails

- Secrets never in git: no access keys, no `BAYPAY_DB_PASSWORD` in `.tfvars`, task-def JSON, Ansible vars, or pipeline YAML.
- Region is **`us-west-2`**. Do not apply EKS, NAT Gateway, OpenSearch, or multi-AZ RDS in a 90-minute lab.
- `terraform validate` is enough to pass. Estimate before any `apply`. Destroy when the lab says so. Do not leave an ALB overnight.
- Never deploy `:latest`. Pin immutable tags (and record digests).
- Do not force-push `main`. Revert with a new commit.
- Ansible is for leftover Liberty / VM config. Do not use it to mutate Fargate task definitions as the primary release path.
- Do not bounce `dmgr-east` or recycle `PaymentCluster` to undo an ECS release.
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`.
