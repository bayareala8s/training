# Portfolio worksheet — AWS architecture

**Artifact:** Module 11 / [BUILD-1101](../../labs/BUILD-1101/README.md) · [ARCHITECT-1102](../../labs/ARCHITECT-1102/README.md) · [SECURITY-1103](../../labs/SECURITY-1103/README.md) · [INCIDENT-1104](../../labs/INCIDENT-1104/README.md) · [COST-1105](../../labs/COST-1105/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-048 (deploy), AEJE-D-049 (platform choice), AEJE-D-050 (IAM), AEJE-D-051 (incident), AEJE-D-052 (cost)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste secrets or access keys; all BayPay data is synthetic. `terraform apply` is optional — say whether you applied.

The Module 11 portfolio artifact is this page: **AWS architecture decision (ECS vs EKS vs OpenShift)** plus the deploy, IAM, and cost insets. Detailed arithmetic lives on [PF-aws-cost.md](PF-aws-cost.md).

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | 2026-09-06 |
| Path (`validate` only / `apply` then destroy / files only) | **`validate` only** — no `apply` (ALB would bill) |
| Region (must be `us-west-2`) | **us-west-2** |
| Reference commit or branch | Downloads workspace; `labs/BUILD-1101/work/` (starter left incomplete) |

---

## 2. Deploy (BUILD-1101)

Teaching names from [ACCOUNT.md](../../datasets/baypay-aws/ACCOUNT.md):

| Field | Your answer |
|---|---|
| Image (`…/baypay/payment-service:<tag>`, not `:latest`) | ECR `baypay/payment-service:<tag>` (immutable). Teaching default URI uses `:3.9.2`, never `:latest`. |
| `containerPort` | **8080** |
| Health check path and matcher | **`/actuator/health/liveness`** on port **8080**, HTTP, matcher **200**. Not `/`, not `/health`. |
| Fargate cpu / memory | **256** / **512** (`desired_count = 1`). Not `-Xmx512m`. |
| Subnet shape (public + IGW? NAT?) | Two **public** subnets + **IGW**. `assign_public_ip = true`. **No NAT.** |
| Tags (`Course`, `Module`, `Lab`, `Environment`, `Expiration`) | `Course=AEJE`, `Module=11`, `Lab=BUILD-1101`, `Environment=student`, `Expiration=2026-09-06` |

In 4–6 sentences, explain what AEJE-D-048 is showing and why the starter was incomplete.

AEJE-D-048 is the **student apply** shape: merchants hit an ALB in `us-west-2` public subnets; the target group health-checks **`/actuator/health/liveness`** on **8080**; one Fargate task (256 CPU / 512 MiB) runs `payment-service` from ECR `baypay/payment-service:<tag>`. There is no NAT, no EKS, no RDS — profile `local` (H2). The starter already built VPC, IGW, ALB, cluster, and two IAM roles, but left `health_check` off the target group (provider default **`/`**, which Spring **404s**) and omitted `containerPort` in `portMappings`. A task can be `RUNNING` while the ALB marks targets unhealthy (INCIDENT-1104). Jordan’s “creates an ALB” file is not a payment front door until those two ACCOUNT.md lines exist. `pay-alb-student.baypay.example` is a teaching name — not a reason to open Route 53.

---

## 3. Platform decision (ARCHITECT-1102)

AEJE-D-049: same `payment-service` (Java 21, **8080**, `/actuator/health/liveness`) behind three control planes. No fourth default (App Runner, Lambda, “ECS on EC2 always-on”). No ND-on-EKS. No second control plane as a rollback cell (same smell as ARCHITECT-604’s second ND cell).

| Criterion | ECS / Fargate | EKS | OpenShift |
|---|---|---|---|
| When BayPay picks it | **This quarter / student apply:** one Spring Boot service, AWS-native IAM, no custom controllers | Estate **already** Kubernetes; you need the API, CRDs, sidecars you will not rewrite as task defs | Module 10 is already production: Routes, SCCs, operators — **stay** |
| Control plane you operate | AWS operates ECS; you own task def + service + cluster name | You operate **add-ons + YAML** on a billed EKS API (~$0.10/h before nodes) | You (or ROSA) operate the OCP API; workers still need patches |
| Deploy artifact | Task definition + `aws_ecs_service` (BUILD-1101) | Deployment + Service (Module 10 YAML) | Same Deployment; Route/SCC/operators on top |
| Edge | **ALB** + target group `:8080` | Ingress / AWS Load Balancer Controller → ALB or NLB | **Route** `payment-route` (same host as Ingress in CLUSTER.md) |
| Health probe owner | **ALB** target group (`/actuator/health/liveness`, matcher 200) | **kubelet** readiness/liveness (same URL); Ingress is not the probe | kubelet + Route admission; same Actuator URL |
| IAM model | **Execution role** (pull + logs) ≠ **task role** (app AWS calls). Task role “for free” — no IRSA | **IRSA** (or Pod Identity): you design the SA ↔ role trust | Service account + SCC; cloud IAM is extra if you call AWS |
| Who patches nodes | **No nodes** (Fargate) | Managed node groups / Fargate profiles — you still own kube/add-on upgrades | OpenShift workers + operators — platform team load |
| Lock-in | AWS task JSON / Terraform | Kubernetes API is portable; **EKS add-ons and IRSA are not** | Operators/SCCs/Routes are OCP-shaped |
| Unit cost refused in 90 min | Idle **ALB** overnight; NAT; desired_count left at 1 | **EKS control plane** (~$2.40/day) + nodes “to compare” | **ROSA cluster fee** to “look production” |

**ECS wins this quarter (one paragraph):**

BayPay’s next *student / AWS sandbox* payment replica is **ECS on Fargate** in `us-west-2`: ECR `baypay/payment-service:<tag>`, task **256/512**, `containerPort` 8080, ALB `pay-alb-student` health-checking `/actuator/health/liveness`, public subnets + IGW, execution role + empty task role (BUILD-1101). One process, no CRDs, no custom controllers. Finance pays ALB hours, not an EKS API. This is the ACCOUNT.md default — not a claim that Kubernetes is wrong.

**EKS wins when (one paragraph — not “more production”):**

EKS wins when BayPay **already** runs Kubernetes (or must keep Module 10 YAML, mesh sidecars, or CRDs) and the team will not rewrite those as task definitions. You still own add-ons, IRSA, and the control-plane bill. “EKS is more production” is not a reason. A greenfield single-service payment API does not need a kube API this quarter.

**OpenShift wins when (one paragraph — Module 10 remains a home):**

OpenShift wins when `baypay-prod` already serves Harbor Market on **Route `payment-route`**, SCCs, and operators Riley’s on-call already knows. BUILD-1101 succeeding in a sandbox does not decommission that home. Module 10 is not legacy to escape this week. Stay until a migration has a wave plan (same honesty as Liberty waves) — not a slogan.

**Refusal sentence** (no EKS/ROSA/NAT apply for realism):

I will not apply EKS, ROSA, or a NAT Gateway “for realism” in a 90-minute lab; that is a bill (COST-1105), not a comparison, and I will not stand up a second control plane as rollback or run traditional WebSphere ND on EKS workers as modernization.

---

## 4. Mapping inset

Health path is **`/actuator/health/liveness`** in every home. Secrets stay out of git.

| Module 10 object | AWS object | Health / secret contract |
|---|---|---|
| Deployment (`replicas`, pod template) | ECS **task definition** + **service** (`desired_count`) | Same image/port; ALB (not kubelet) owns the student-apply probe |
| Service (`ClusterIP` 8080, selector) | ALB **target group** `:8080` + listener | Empty TG ≈ empty Endpoints (1006/1104 class) |
| Ingress / Route (`payments.apps.baypay.example`) | **ALB** DNS (teaching `pay-alb-student.baypay.example`) | TLS is INC-1005 on kube; ACM/listener later — not Route 53 this week |
| Secret `baypay-db` | Secrets Manager (SECURITY-1103) + task `valueFrom` | `BAYPAY_DB_*` names; never task-def JSON in git |

---

## 5. IAM, secrets, KMS (SECURITY-1103)

Files: `labs/SECURITY-1103/work/` (starter left broken). AEJE-D-050.

| Field | Your answer |
|---|---|
| Execution role purpose | Agent that **starts** the container: ECR pull `baypay/payment-service`, CloudWatch logs, **`GetSecretValue` on one ARN**, **`kms:Decrypt` on one CMK**. Role `baypay-1103-execution`. |
| Task role purpose | What the **JVM becomes** after start. Separate principal `baypay-1103-task`. Empty — this app does not call AWS APIs. **No** `GetSecretValue`, **no** admin. |
| Secret ARN shape (`baypay/payment/db` + JSON keys) | `arn:aws:secretsmanager:us-west-2:123456789012:secret:baypay/payment/db` + `:url::` / `:username::` / `:password::` → `BAYPAY_DB_URL` / `USER` / `PASSWORD` |
| What you grepped for (`changeme`, `AdministratorAccess`, `AKIA`) | In `work/`: **none**. Starter still has `AdministratorAccess` + `changeme` (left on purpose). |

In 4–6 sentences, explain why a combined `AdministratorAccess` role is not a deploy shortcut, and why the task role does not need `GetSecretValue` when ECS injects `valueFrom`.

Sam’s one role (`baypay-payment-combined`) as both `executionRoleArn` and `taskRoleArn` plus `AdministratorAccess` is cheaper on day one and an **account compromise** on day two: anything the JVM can be tricked into (SSRF, RCE) inherits `iam:*`. Avery’s POST already carries account ids — that process must not be the account. ECS injects `secrets.valueFrom` **as the execution role** before the process starts; Spring only sees env. Copying `GetSecretValue` onto the task role widens the JVM for no benefit. A CMK we named (`kms-key-policy.json`: root administers, execution decrypts, no `Principal: "*"`) is worth it when Priya needs a named decrypt grant and an audit trail; the AWS-managed Secrets Manager key is quieter and you never named who can decrypt. One secret / three JSON keys = one IAM `Resource` (`baypay/payment/db*`) versus three secrets / three grants. If the password is still in the task JSON, Secrets Manager is theater — same lesson as FIX-902.

---

## 6. Incident inset (INCIDENT-1104 — optional keep)

Kept as the AWS incident write-up. Pack: `incidents/aws/INC-AWS-1104/`. AEJE-D-051.

| Field | Your answer |
|---|---|
| Symptom (merchant HTTP + task status) | Harbor Market / Avery `c1104c44-…-111104` **502/503** on `pay-alb-student.baypay.example`. Task **RUNNING**. TG unhealthy: health **`/`** → **404**, matcher 200. |
| What you ruled out (and which gate) | SG / timeout (gate 1: HTTP 404, not `Target.Timeout`). Crashed JVM (gate 2: RUNNING, 8080). Spring 503 / TLS (gate 3: ALB 503, HTTP :80). RDS / `dmgr-east` (not in this estate). |
| Stabilize vs remediate | **Now:** TG path `/actuator/health/liveness`. **Next:** Terraform + CI fail on path `/`. Never matcher 404, never 8080/`0.0.0.0/0`. |

Do not paste `solutions/INCIDENT-1104/`. Quote pack evidence only.

---

## 7. Cost summary (COST-1105)

Fill [PF-aws-cost.md](PF-aws-cost.md) in full. Copy the headline numbers here:

Teaching rates (COST-1105 / `us-west-2`). LCU ≈ 0. Fargate `0.25×0.04048 + 0.5×0.004445 = $0.01234/h`.

| Window | ALB | Fargate 256/512 | NAT (refused) |
|---|---|---|---|
| 1.5 hours | $0.03375 | $0.0185 | $0.0675 + data |
| 24 hours | **$0.54** | $0.30 | **$1.08** + data |
| 7 days | $3.78 | $2.07 | $7.56 + data |

EKS refused: **$2.40/day**. ECR 2 GB / 7 d: **$0.047**. Same-day apply brief: **$0.15–$2**. We did **not** apply.

Destroy list (ALB, ECS, ECR — your words):

Same day: ALB + listener + target group; ECS service + cluster + task definition; ECR repo **and images**; CloudWatch log group. Confirm no NAT / EKS / RDS. `desired_count = 0` does not stop the ALB. `Expiration` is a reminder, not destroy.

---

## 8. Public-subnet trade-off

`assign_public_ip = true` on a **public** subnet + IGW is how the task pulls ECR and writes CloudWatch **without a NAT Gateway**. You gave up private-subnet isolation: the ENI has a public address (egress still 443; ALB SG is the only 8080 ingress). A NAT (~$0.045/hour plus data) often **costs more than the ALB** and is the COST-1105 landmine — “Fargate in private subnets is how production looks” is not this lab. Production can add private + NAT (or VPC endpoints) later; a 90-minute student apply must not. Security groups + no admin task role are the isolation you still owe.

---

## 9. Interview snippet (Staff, 6–8 sentences)

Student default is **ECS on Fargate** (AEJE-D-049): one Spring Boot service, ALB + **split** execution/task roles (AEJE-D-050). EKS wins only if the estate **already** needs the Kubernetes API / CRDs / sidecars — not because it is “more production.” OpenShift wins when Route `payment-route` / SCCs / operators are already Harbor Market’s home. Avery’s POST depends on **8080 + `/actuator/health/liveness`**, not the control-plane brand. Execution role pulls, logs, `GetSecretValue` on `baypay/payment/db`, and `kms:Decrypt` on one CMK; the JVM gets `BAYPAY_DB_*` via `valueFrom` (`:url::` / `:username::` / `:password::`). Task role stays empty — not `AdministratorAccess`, not a second `GetSecretValue`. Combined admin is day-two account compromise. Do not apply EKS/ROSA/NAT for realism. An idle ALB still bills — destroy the same day.
