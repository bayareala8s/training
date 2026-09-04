# ARCHITECT-1102 — Instructor solution

**Do not share this file with students before they submit the decision table.**

The compact pick in the student lab is a *post-attempt* numbering check. It is not the scored narrative. A worksheet that only says “use ECS because this is the AWS module” must not outscore a page with win/lose conditions and a Module 10 mapping.

ECS on Fargate is the **student apply default**. Kubernetes and OpenShift from Module 10 remain **valid homes**. Do not apply EKS or ROSA. Do not recommend traditional WebSphere ND on EKS worker nodes.

## Decision table (acceptable content)

| Criterion | ECS / Fargate | EKS | OpenShift (self-managed or ROSA) |
|---|---|---|---|
| When BayPay picks it | One Spring Boot service, AWS-native IAM, no custom controllers. Student apply default (BUILD-1101). | Estate is already Kubernetes: CRDs, operators, sidecars, shared platform YAML. | Estate is already OpenShift: Routes, SCCs, Operators, `payment-route` in `baypay-prod`. |
| Control plane you operate | None (AWS runs ECS). You own task defs and services. | AWS runs the API server. You still own add-ons, node/Fargate profiles, Ingress controller. | You or ROSA run the platform. You own Projects, Routes, SCCs. |
| Edge | ALB + target group, health on `/actuator/health/liveness` | Ingress or AWS Load Balancer Controller → same Actuator URL | Route (`payment-route`) → same Actuator URL |
| IAM | Task role ≠ execution role (SECURITY-1103) | IRSA / Pod Identity — you design the binding | Service account + cloud credential operator (or kube secrets) |
| Deploy artifact | Task definition + ECS service | Deployment + Service | Deployment + Route |
| Health owner | Target group path in Terraform | kubelet probe in the Deployment | Same as Kubernetes; Route does not replace readiness |
| 90-minute lab cost | ALB + tiny Fargate (optional apply) | **Refuse.** Control plane ~$0.10/hr plus nodes | **Refuse.** ROSA/cluster fee is not a lab |
| How it loses | Custom controllers; multi-cluster kube API; team only speaks Deployments | No platform team; “create EKS for realism”; you only have one JAR | You only need one AWS service this quarter and nobody operates OCP |

## When ECS wins (acceptable paragraph)

BayPay’s *next* sandbox and the course default: `payment-service` is one JVM, port 8080, Actuator liveness, image in ECR. BUILD-1101 already names the objects (cluster, task def, service, ALB, target group). Task role versus execution role is native. There is no EKS control-plane bill. Avery Chen’s POST does not get faster because the API server is Kubernetes.

## When EKS wins (acceptable paragraph)

EKS wins when Module 10’s **API** is already the product: CRDs, admission, a mesh or operator you will not rewrite as a task definition, or a platform team that ships Deployments to every service. “More production” is not a reason. You still owe IRSA, an Ingress/ALB controller, node patching or Fargate profiles, and the ~$0.10/hour control plane. You do not apply EKS to learn that sentence.

## When OpenShift wins (acceptable paragraph)

OpenShift wins when `baypay-prod` already serves Harbor Market on `payment-route`, SCCs match the Module 9 UID contract, and operators are how the platform team installs. Moving to ECS to “be on AWS” throws away that operating model for one sandbox ALB. Module 10 is a home, not a hallway.

## Mapping inset

| Module 10 | ECS / ALB | Notes |
|---|---|---|
| Deployment | Task definition + ECS service | Replicas ≈ `desired_count` |
| Service (ClusterIP) | Target group (`ip` targets, port 8080) | Not a selector-vs-label lab |
| Ingress / Route | ALB listener → target group | Teaching host `pay-alb-student.baypay.example` |
| Secret `baypay-db` | Secrets Manager + execution role (SECURITY-1103) | Never task-def plaintext |
| `readinessProbe` / `livenessProbe` | Target group health + optional ECS health check | Same URLs from BUILD-305 |
| Namespace `baypay-prod` | Cluster + service names / tags | Not a kube Namespace |

Health path in every column: `/actuator/health/liveness` (and readiness when the object is a kube probe). Never `/`.

## Refusal

Do not apply EKS, ROSA, NAT Gateway, or multi-AZ RDS in a 90-minute lab. Do not invent a second control plane as a rollback environment (same failure mode as a second ND cell in ARCHITECT-604). Do not run traditional `payment.ear` on EKS worker nodes as modernization.

## Diagram

AEJE-D-049: one process, three control planes, one merchant path. ECS is the apply default; EKS and OpenShift are choices with cost and ops load.

## Scoring notes

Full marks require three honest columns, a non-slogan ECS default, an EKS win that is not “more production,” an OpenShift win that keeps Module 10, a mapping inset, and a refusal to apply EKS/ROSA. “Always EKS” or “OpenShift is legacy” caps Technical accuracy and Production awareness.
