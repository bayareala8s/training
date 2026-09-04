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
| Date | |
| Path (`validate` only / `apply` then destroy / files only) | |
| Region (must be `us-west-2`) | |
| Working tree path (e.g. `/tmp/aeje-capstone-3`) | |
| Reference commit or branch | |
| `Expiration` ISO date | |

---

## 2. Architecture (AEJE-D-072)

Cite **AEJE-D-072**. Contrast AEJE-D-071 in one sentence (ND is the source estate; do not bounce `dmgr-east`).

In 6–8 sentences, describe the target path Avery Chen’s POST takes (TLS edge → ALB or Route → `payment-service` :8080 → secrets → teaching DB). Name owners: Sam (platform / ALB), Jordan (image tag), Riley (health path), Priya (SLO tile).

| Field | Your answer |
|---|---|
| Edge (ALB teaching name or AWS DNS) | |
| Health check path and port | |
| Image (`baypay/payment-service:<tag>`, not `:latest`) | |
| Fargate cpu / memory (if apply-shaped) | |
| Subnet shape (public + IGW? NAT?) | |
| Teaching DB strategy (`local` / H2 — no RDS apply) | |

### Service list

| Service | Apply this capstone? (yes / paper only / no) | Why |
|---|---|---|
| ECR `baypay/payment-service` | | |
| ECS / Fargate | | |
| ALB + target group | | |
| Secrets Manager + KMS | | |
| CloudWatch logs | | |
| NAT Gateway | **no** | |
| EKS / ROSA | **no apply** | |
| OpenShift | **no apply** | |
| RDS / RDS Multi-AZ | **no** | |

---

## 3. Platform decision (ARCHITECT-1102, restated)

| Criterion | ECS / Fargate | EKS | OpenShift |
|---|---|---|---|
| When BayPay picks it | | | |
| Apply in CAPSTONE-3? | student default | paper only | paper only |
| Edge | | | |
| IAM model | | | |
| What you refuse in this capstone | | | |

**ECS wins this quarter (one paragraph):**

**EKS wins when (one paragraph — not “more production”):**

**OpenShift wins when (one paragraph — Module 10 remains a home):**

**Refusal sentence** (no EKS / ROSA / NAT apply for realism):

---

## 4. Terraform and modules

Which tree did you validate? (course skeleton / BUILD-1202 modules / BUILD-1101 copy / composition)

| Field | Your answer |
|---|---|
| `variable "region"` default | |
| `required_providers.aws` present? | |
| `modules/ecr` inputs / outputs (or “skeleton only”) | |
| Service-contract `container_port` | |
| Service-contract health path | |
| Image reference (must not be `:latest`) | |
| Tags (`Course`, `Module`, `Lab`, `Environment`, `Expiration`) | |
| Resources you **refused** (NAT, EKS, RDS, second ALB) | |
| `terraform init -backend=false && terraform validate` result | |

In 4–6 sentences, explain what BUILD-1202 postponed (no live `aws_ecs_service` / ALB in the module) and how BUILD-1101 or ACCOUNT.md still supplies the ALB health contract. Cite `infrastructure/terraform/baypay-ecs` if you used it.

---

## 5. IAM, secrets, and KMS

| Field | Your answer |
|---|---|
| Execution role purpose | |
| Task role purpose | |
| Secret ARN shape (`baypay/payment/db` + JSON keys) | |
| Who may `kms:Decrypt` (execution vs task) | |
| What you grepped for (`changeme`, `AdministratorAccess`, `AKIA`) | |

In 4–6 sentences, explain why a combined `AdministratorAccess` role is not a deploy shortcut, and why the task role does not need `GetSecretValue` when ECS injects `valueFrom`.

---

## 6. Monitoring and SLO (99.9%)

Cite OBSERVABILITY.md. Do **not** silently upgrade to 99.99%. If you mention 99.99%, say it is Module 14 / ARCHITECT-1401.

| Field | Your answer |
|---|---|
| SLI (your words) | |
| SLO target (must be **99.9%**) | |
| Window | |
| Error-budget size (~43 minutes / 30d if you use the teaching number) | |
| Latency teaching target (P99) | |
| What you would **page** on versus ticket | |
| Labels you refused (`customerId`, `accountId`, `Idempotency-Key`, PAN) | |

In 4–6 sentences, explain why 4xx stay off default burn and why editing the tile to 99.99% would be the wrong “improvement” on this packet.

---

## 7. Scaling and resilience

| Field | Your answer |
|---|---|
| Student `desired_count` | |
| Production scale **signal** (not CPU-only) | |
| Max replica cap (and why) | |
| Scale-down posture | |
| Unhealthy target: stabilize vs remediate | |
| Rollback artifact (last healthy task def / immutable tag) | |
| What you will **not** bounce (`dmgr-east`, RDS, leftover cell) | |

One paragraph: RUNNING vs target-group healthy (INCIDENT-1104). One paragraph: green pipeline vs healthy deploy (INCIDENT-1205).

---

## 8. Cost briefing (before any apply)

Use COST-1105 teaching rates unless you cite a public page (`us-west-2`, date, URL). Show the multiply.

| Window | ALB | Fargate 256/512 | NAT (refused) | EKS CP (refused) |
|---|---|---|---|---|
| 1.5 hours | | | | |
| 24 hours | | | | |
| 7 days | | | | |

Same-day session range you would brief before `apply` (or **$0** validate-only):

Overnight idle ALB (one sentence):

What still bills after `desired_count = 0`:

---

## 9. Cleanup / destroy

- [ ] I did not apply, **or** I destroyed the same day
- [ ] ALB, listener, target group
- [ ] ECS service, cluster, task definition
- [ ] ECR repository **and images**
- [ ] CloudWatch log group
- [ ] Secrets / KMS deletion window (if created)
- [ ] Confirmed no NAT, no EKS, no RDS in `us-west-2`
- [ ] `Expiration` was a reminder — I still ran destroy (or had nothing to destroy)

Notes (account alias, stack dir, date destroyed):

---

## 10. Interview snippet (Staff, 8–10 sentences)

Explain to Sam Okada, Priya Nair, Riley Okonkwo, and Jordan Voss, in one sitting: why Fargate is the student default; when EKS or OpenShift still wins; how `BAYPAY_DB_*` is injected; why Avery Chen’s POST must not depend on an idle ALB or a health check on `/`; why the SLO stays 99.9%; and what you destroy before you leave.

---

## Honesty

- [ ] I did not open `solutions/CAPSTONE-3/` before attempting this sheet
- [ ] Every AWS claim has a source (ACCOUNT.md, my `.tf`, OBSERVABILITY.md, or a cited prior lab)
- [ ] I did not paste an instructor solution
- [ ] I did not put an access key or a live password in this file
- [ ] I did not apply NAT, EKS, or RDS Multi-AZ
- [ ] SLO on this page is **99.9%** (99.99% only if I named the Module 14 upgrade)
- [ ] If I applied, I destroyed in `us-west-2` the same day
