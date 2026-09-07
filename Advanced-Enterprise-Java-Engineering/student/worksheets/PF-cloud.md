# Portfolio worksheet — Cloud BayPay

**Artifact:** [CAPSTONE-3](../../capstones/03-cloud-baypay/README.md) (Modules 11–12)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-072 (cloud-native target) · AEJE-D-071 (ND source, contrast only)  
**Account notes:** [datasets/baypay-aws/ACCOUNT.md](../../datasets/baypay-aws/ACCOUNT.md)  
**Ops SLO:** [datasets/baypay-ops/OBSERVABILITY.md](../../datasets/baypay-ops/OBSERVABILITY.md) — **99.9%**  
**IaC pointers:** [infrastructure/terraform/baypay-ecs](../../infrastructure/terraform/baypay-ecs/) · [BUILD-1201](../../labs/BUILD-1201/README.md) · [BUILD-1202](../../labs/BUILD-1202/README.md) · [BUILD-1101](../../labs/BUILD-1101/README.md)

Use this sheet as the reviewer-ready Cloud BayPay packet. Fill every section in your own words. Do not paste `solutions/CAPSTONE-3/` or other instructor RCAs. Do not put access keys, `changeme`, or `BAYPAY_DB_PASSWORD` values in this file. `terraform apply` is optional — say whether you applied, and whether you already destroyed.

Tags you will honor: `Course=AEJE`, `Module=Capstone`, `Lab=CAPSTONE-3`, `Environment=student`, `Expiration=<ISO date>`.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | 2026-09-07 |
| Path (`validate` only / `apply` then destroy / files only) | **`validate` only** — no `apply` (ALB would bill) |
| Region (must be `us-west-2`) | **us-west-2** |
| Working tree path (e.g. `/tmp/aeje-capstone-3`) | `student/work/capstone-3/` (BUILD-1202 modules + `local.alb_contract`; ALB HCL pointer `labs/BUILD-1101/work/`) |
| Reference commit or branch | Downloads working tree (not pushed) |
| `Expiration` ISO date | **2026-09-07** (same-day reminder; nothing applied) |

---

## 2. Architecture (AEJE-D-072)

Cite **AEJE-D-072**. Contrast AEJE-D-071 in one sentence (ND is the source estate; do not bounce `dmgr-east`).

AEJE-D-071 is leftover ND (`ihs-east` → `PaymentCluster` / `RefundCluster` → `db-east`). AEJE-D-072 is the cloud-native target. Bouncing `dmgr-east` is not a cloud stabilize.

In 6–8 sentences, describe the target path Avery Chen’s POST takes (TLS edge → ALB or Route → `payment-service` :8080 → secrets → teaching DB). Name owners: Sam (platform / ALB), Jordan (image tag), Riley (health path), Priya (SLO tile).

Avery Chen (`11111111-1111-1111-1111-111111111111`) POSTs `$25.00` to `/api/v1/payments` over TLS. Sam Okada owns the student edge: ALB teaching name `pay-alb-student.baypay.example` (a real apply uses AWS DNS) in **two public subnets** in `us-west-2`. The target group health-checks **`/actuator/health/liveness` on 8080**, matcher **200** — Riley Okonkwo owns that path; `/` 404s and is INCIDENT-1104. A Fargate task (256 CPU / 512 MiB, `desired_count = 1` in a lab) runs `payment-service` from Jordan Voss’s immutable ECR tag `baypay/payment-service:<tag>`, never `:latest`. The execution role injects `BAYPAY_DB_*` from Secrets Manager `baypay/payment/db` (JSON keys) via `valueFrom`; the teaching DB is profile `local` / H2 — no RDS apply. Priya Nair owns the ops tile: **99.9%** successful payment creates (server failures), not 99.99%. Harbor Market does not care whether this process started as a Module 10 Pod or an ECS task. They care that **8080** answers.

| Field | Your answer |
|---|---|
| Edge (ALB teaching name or AWS DNS) | Teaching `pay-alb-student.baypay.example`; apply would use the AWS-generated DNS |
| Health check path and port | `/actuator/health/liveness` on **8080**, matcher **200** |
| Image (`baypay/payment-service:<tag>`, not `:latest`) | `baypay/payment-service:3.9.2` (module default; pipeline pin is `${{ github.sha }}`) |
| Fargate cpu / memory (if apply-shaped) | **256** / **512**. Not `-Xmx512m`. |
| Subnet shape (public + IGW? NAT?) | Two **public** subnets + **IGW**. `assign_public_ip = true`. **No NAT.** |
| Teaching DB strategy (`local` / H2 — no RDS apply) | Profile `local` / in-memory H2. RDS Multi-AZ is literacy, not this invoice. |

### Service list

| Service | Apply this capstone? (yes / paper only / no) | Why |
|---|---|---|
| ECR `baypay/payment-service` | paper / validate (cheap if applied) | Immutable tags + scan-on-push. Module `modules/ecr`. |
| ECS / Fargate | paper — student **apply default**, not applied | 256/512; `desired_count = 1` in a lab. BUILD-1101 shape. |
| ALB + target group | paper — not applied | Health `/actuator/health/liveness` :8080. Idle ALB bills. |
| Secrets Manager + KMS | paper JSON required | `iam/`; `valueFrom` JSON keys; named CMK. No `changeme`. |
| CloudWatch logs | paper (module creates log group if applied) | Retention 7d in the contract module. Insights **off**. |
| NAT Gateway | **no** | ~$0.045/h + data. Locked shape is public + IGW. |
| EKS / ROSA | **no apply** | Valid **design** home (ARCHITECT-1102). Control plane ~$0.10/h. |
| OpenShift | **no apply** | Valid **design** home (Module 10 Route / SCC). |
| RDS / RDS Multi-AZ | **no** | Use `local` / H2. Multi-AZ is a sentence, not an apply. |

---

## 3. Platform decision (ARCHITECT-1102, restated)

| Criterion | ECS / Fargate | EKS | OpenShift |
|---|---|---|---|
| When BayPay picks it | This quarter / student apply: one Boot service, AWS-native IAM, no CRDs | Estate **already** Kubernetes; CRDs / sidecars you will not rewrite as task defs | Module 10 already production: Routes, SCCs, operators — **stay** |
| Apply in CAPSTONE-3? | student default | paper only | paper only |
| Edge | ALB + TG `:8080` | Ingress / LBC → ALB or NLB | Route `payment-route` (same host as CLUSTER.md Ingress) |
| IAM model | Execution role ≠ task role. `valueFrom` uses execution. | IRSA / Pod Identity | SA + SCC; cloud IAM extra if you call AWS |
| What you refuse in this capstone | Idle ALB overnight; NAT; `:latest`; combined admin role | Applying EKS “to look production” | Applying ROSA for this packet |

**ECS wins this quarter (one paragraph):**

The student / sandbox payment replica is **ECS on Fargate** in `us-west-2`: ECR `baypay/payment-service:<tag>`, task **256/512**, `containerPort` 8080, ALB health-checking `/actuator/health/liveness`, public subnets + IGW, split execution / task roles. One process. Finance pays ALB hours, not an EKS API. That is ACCOUNT.md — not a claim that Kubernetes is wrong.

**EKS wins when (one paragraph — not “more production”):**

EKS wins when BayPay **already** runs Kubernetes (Module 10 YAML, mesh sidecars, CRDs) and the team will not rewrite those as task definitions. You still own add-ons, IRSA, and the control-plane bill (~$2.40/day before nodes). “EKS is more production” is not a reason. A greenfield single-service payment API does not need a kube API this quarter.

**OpenShift wins when (one paragraph — Module 10 remains a home):**

OpenShift wins when `baypay-prod` already serves Harbor Market on **Route `payment-route`**, SCCs, and operators Riley already pages. A sandbox Fargate success does not decommission that home. Stay until a wave plan exists — same honesty as Liberty waves.

**Refusal sentence** (no EKS / ROSA / NAT apply for realism):

I will not apply EKS, ROSA, or a NAT Gateway “for realism” in this capstone; that is a bill (COST-1105), not a comparison, and I will not stand up a second control plane or bounce `dmgr-east` as cloud rollback.

---

## 4. Terraform and modules

Which tree did you validate? (course skeleton / BUILD-1202 modules / BUILD-1101 copy / composition)

**Composition:** `student/work/capstone-3/` — BUILD-1202 modules, retagged `Lab=CAPSTONE-3` / `Module=Capstone`, plus `local.alb_contract` pointing at `labs/BUILD-1101/work/` for the live ALB HCL (also never applied). Course skeleton `infrastructure/terraform/baypay-ecs` is ECR-only; I did not leave modules hollow.

| Field | Your answer |
|---|---|
| `variable "region"` default | **`us-west-2`** |
| `required_providers.aws` present? | Yes (`hashicorp/aws` `>= 5.0`) |
| `modules/ecr` inputs / outputs (or “skeleton only”) | In: `name`, `region`, `tags`. Out: `repository_url`, `repository_arn`. `image_tag_mutability = "IMMUTABLE"`, scan-on-push. |
| Service-contract `container_port` | **8080** (default + root pass) |
| Service-contract health path | **`/actuator/health/liveness`** |
| Image reference (must not be `:latest`) | `…/baypay/payment-service:3.9.2` (`var.container_image`) |
| Tags (`Course`, `Module`, `Lab`, `Environment`, `Expiration`) | `Course=AEJE`, `Module=Capstone`, `Lab=CAPSTONE-3`, `Environment=student`, `Expiration=2026-09-07` |
| Resources you **refused** (NAT, EKS, RDS, second ALB) | No `aws_nat_gateway`, no EKS, no `aws_db_instance`, no second `aws_lb` in this root |
| `terraform init -backend=false && terraform validate` result | **Success** — `The configuration is valid.` (2026-09-07) |

In 4–6 sentences, explain what BUILD-1202 postponed (no live `aws_ecs_service` / ALB in the module) and how BUILD-1101 or ACCOUNT.md still supplies the ALB health contract. Cite `infrastructure/terraform/baypay-ecs` if you used it.

BUILD-1202’s `ecs_service` module is a **contract**: port, health path, image, and a cheap CloudWatch log group. It does **not** create `aws_ecs_service` or `aws_lb`, because those are the BUILD-1101 / COST-1105 invoice. `local.alb_contract` and `labs/BUILD-1101/work/` still name path `/actuator/health/liveness`, port **8080**, matcher **200**, Fargate 256/512, two public subnets, `assign_public_ip = true`. The course skeleton `infrastructure/terraform/baypay-ecs` is provider + tags + one ECR — useful, not a full module story. Pipeline: BUILD-1204 `${{ github.sha }}` (after `needs: test`) becomes the ECS image input; `:latest` is not the deploy tag. `validate` does not prove `apply` is cheap.

---

## 5. IAM, secrets, and KMS

| Field | Your answer |
|---|---|
| Execution role purpose | Agent that **starts** the container: ECR pull, CloudWatch logs, **`GetSecretValue` on one ARN**, **`kms:Decrypt` on one CMK**. Paper: `iam/execution-role.json` (`baypay-cap3-execution`). |
| Task role purpose | What the **JVM becomes**. Separate principal `baypay-cap3-task`. Empty / narrow. **No** `GetSecretValue`, **no** `AdministratorAccess`. |
| Secret ARN shape (`baypay/payment/db` + JSON keys) | `arn:aws:secretsmanager:us-west-2:123456789012:secret:baypay/payment/db` + `:url::` / `:username::` / `:password::` → `BAYPAY_DB_URL` / `USER` / `PASSWORD` |
| Who may `kms:Decrypt` (execution vs task) | **Execution** only (`iam/kms-key-policy.json`). Task role is not on the CMK. |
| What you grepped for (`changeme`, `AdministratorAccess`, `AKIA`) | In `student/work/capstone-3/`: no `changeme`, no `AKIA`. `AdministratorAccess` appears only as a refusal in `iam/task-role.json` comments. |

In 4–6 sentences, explain why a combined `AdministratorAccess` role is not a deploy shortcut, and why the task role does not need `GetSecretValue` when ECS injects `valueFrom`.

One role as both `executionRoleArn` and `taskRoleArn` plus `AdministratorAccess` is cheaper on day one and an account compromise on day two: anything the JVM can be tricked into inherits `iam:*`. Avery’s POST already carries account ids — that process must not be the account. ECS injects `secrets.valueFrom` **as the execution role** before the process starts; Spring only sees env. Copying `GetSecretValue` onto the task role widens the JVM for no benefit. The console/sandbox user is a **third** identity — do not copy that admin policy onto the task. Never commit access keys.

---

## 6. Monitoring and SLO (99.9%)

Cite OBSERVABILITY.md. Do **not** silently upgrade to 99.99%. If you mention 99.99%, say it is Module 14 / ARCHITECT-1401.

| Field | Your answer |
|---|---|
| SLI (your words) | Successful `POST /api/v1/payments` / (successful + **server** failures). Server failure = 5xx, timeout, or a dependency that becomes 5xx. 4xx stay off default burn except 429 if treated as capacity. |
| SLO target (must be **99.9%**) | **99.9%** |
| Window | 30 days rolling |
| Error-budget size (~43 minutes / 30d if you use the teaching number) | **~43 minutes** / 30 days |
| Latency teaching target (P99) | P99 **< 400 ms** on a COMPLETED create (teaching) |
| What you would **page** on versus ticket | **Page** SLO burn (fast + slow) and saturation that predicts burn (Hikari pending, servlet threads). **Ticket** scrape / dashboard errors. Do not page “CPU > 80%.” |
| Labels you refused (`customerId`, `accountId`, `Idempotency-Key`, PAN) | All four. Low-cardinality only: `uri`, `method`, `outcome`, `status`. |

In 4–6 sentences, explain why 4xx stay off default burn and why editing the tile to 99.99% would be the wrong “improvement” on this packet.

A frozen-account `422` and a missing `Idempotency-Key` `400` are the API working. Burning budget on those hides a real 5xx. 99.99% is ~52 minutes/year — that is ARCHITECT-1401 / Module 14 architecture (multi-AZ, DR), not this ops tile. Silently editing Grafana to 99.99% does not buy the design; it just makes Priya page on noise. This packet keeps **99.9%**.

---

## 7. Scaling and resilience

| Field | Your answer |
|---|---|
| Student `desired_count` | **1** |
| Production scale **signal** (not CPU-only) | In-flight POSTs or ALB request count on `/api/v1/payments` — closer to the SLI than CPU |
| Max replica cap (and why) | A **max** so a Harbor Market burst cannot stampede the teaching DB / H2 story. CPU tracking is literacy, not the payment SLO. |
| Scale-down posture | Slow. Do not flap tasks under a brief quiet window. |
| Unhealthy target: stabilize vs remediate | Stabilize: fix TG path / replace the task. Remediate: Terraform + CI fail on path `/`. Process `RUNNING` ≠ target healthy. |
| Rollback artifact (last healthy task def / immutable tag) | Last **healthy** task definition / immutable tag (INCIDENT-1205). Not `:latest`. |
| What you will **not** bounce (`dmgr-east`, RDS, leftover cell) | `dmgr-east`, leftover `PaymentCluster`, RDS that was never applied. |

One paragraph: RUNNING vs target-group healthy (INCIDENT-1104). One paragraph: green pipeline vs healthy deploy (INCIDENT-1205).

**1104:** ECS can show `RUNNING` while merchants see 502/503 because the target group still probes `/` and Spring 404s. That is not a reason to open 8080 to the world, add NAT, attach `AdministratorAccess`, or bounce `dmgr-east`. Fix the path. Matcher stays `200`.

**1205:** A green test job that publishes `:latest` (or a bad immutable tag) can roll a task that fails liveness. Rollback is the last healthy tag / task def, not “redeploy latest.” `needs: test` is a prerequisite for publish; it is not a substitute for the ALB contract.

---

## 8. Cost briefing (before any apply)

Use COST-1105 teaching rates unless you cite a public page (`us-west-2`, date, URL). Show the multiply.

Teaching rates: ALB **$0.0225/h** (LCU ≈ 0). Fargate 256/512: `0.25 × $0.04048 + 0.5 × $0.004445` ≈ **$0.01234/h**. NAT **$0.045/h**. EKS CP **$0.10/h**.

| Window | ALB | Fargate 256/512 | NAT (refused) | EKS CP (refused) |
|---|---|---|---|---|
| 1.5 hours | `0.0225 × 1.5 =` **$0.03375** | `0.01234 × 1.5 ≈` **$0.0185** | `0.045 × 1.5 =` **$0.0675** + data | `0.10 × 1.5 =` **$0.15** |
| 24 hours | `0.0225 × 24 =` **$0.54** | `0.01234 × 24 ≈` **$0.30** | `0.045 × 24 =` **$1.08** + data | `0.10 × 24 =` **$2.40** |
| 7 days | **$3.78** | **$2.07** | **$7.56** + data | **$16.80** |

Same-day session range you would brief before `apply` (or **$0** validate-only):

**$0** this sitting (validate only). If someone applied the BUILD-1101 shape: about **$0.15–$2.00** for 1–4 hours then destroy. Do not add NAT/EKS.

Overnight idle ALB (one sentence):

The ALB is **~$0.54/day even when Harbor Market sends zero traffic** — that line, not the $0.012/h task, is the weekend page from Finance.

What still bills after `desired_count = 0`:

The **ALB** (and listener/TG), empty **ECR** storage, leftover **log groups**, **Secrets Manager** (~$0.40/secret/month) and a **CMK** (~$1/key/month) if you created them. `Expiration` tags do not delete resources.

---

## 9. Cleanup / destroy

- [x] I did not apply, **or** I destroyed the same day
- [x] ALB, listener, target group
- [x] ECS service, cluster, task definition
- [x] ECR repository **and images**
- [x] CloudWatch log group
- [x] Secrets / KMS deletion window (if created)
- [x] Confirmed no NAT, no EKS, no RDS in `us-west-2`
- [x] `Expiration` was a reminder — I still ran destroy (or had nothing to destroy)

Notes (account alias, stack dir, date destroyed):

Validate-only on 2026-09-07. Tree: `student/work/capstone-3/`. Nothing created in `us-west-2`. If a leftover BUILD-1101 ALB from another sitting existed, that would already be a bill — this capstone did not apply.

---

## 10. Interview snippet (Staff, 8–10 sentences)

Explain to Sam Okada, Priya Nair, Riley Okonkwo, and Jordan Voss, in one sitting: why Fargate is the student default; when EKS or OpenShift still wins; how `BAYPAY_DB_*` is injected; why Avery Chen’s POST must not depend on an idle ALB or a health check on `/`; why the SLO stays 99.9%; and what you destroy before you leave.

Fargate is the student default because Harbor Market needs one Boot process on **8080** this quarter, not a second control plane. EKS still wins if we already live on the Kubernetes API and CRDs; OpenShift still wins if Route `payment-route` and SCCs are already production — neither is “more production,” and neither is an apply on this packet. `BAYPAY_DB_*` comes from Secrets Manager `baypay/payment/db` via execution-role `valueFrom`; the task role stays empty and is not on the CMK. Avery’s POST dies if the ALB probes `/` (404) or if we leave the ALB up after class — `RUNNING` is a weak sentence when the target is unhealthy. Jordan ships an immutable tag (`${{ github.sha }}`), not `:latest`; rollback is the last healthy task def. Priya’s tile stays **99.9%** (~43 min / 30d); 99.99% is Module 14 architecture, not a dashboard edit. We did not apply NAT, EKS, or RDS. We destroy the ALB the same day — or we never create it, which is what this sitting did.

---

## Honesty

- [x] I did not open `solutions/CAPSTONE-3/` before attempting this sheet
- [x] Every AWS claim has a source (ACCOUNT.md, my `.tf`, OBSERVABILITY.md, or a cited prior lab)
- [x] I did not paste an instructor solution
- [x] I did not put an access key or a live password in this file
- [x] I did not apply NAT, EKS, or RDS Multi-AZ
- [x] SLO on this page is **99.9%** (99.99% only if I named the Module 14 upgrade)
- [x] If I applied, I destroyed in `us-west-2` the same day
