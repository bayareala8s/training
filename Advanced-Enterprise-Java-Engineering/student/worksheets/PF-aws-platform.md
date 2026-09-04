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
| Date | |
| Path (`validate` only / `apply` then destroy / files only) | |
| Region (must be `us-west-2`) | |
| Reference commit or branch | |

---

## 2. Deploy (BUILD-1101)

Teaching names from [ACCOUNT.md](../../datasets/baypay-aws/ACCOUNT.md):

| Field | Your answer |
|---|---|
| Image (`…/baypay/payment-service:<tag>`, not `:latest`) | |
| `containerPort` | |
| Health check path and matcher | |
| Fargate cpu / memory | |
| Subnet shape (public + IGW? NAT?) | |
| Tags (`Course`, `Module`, `Lab`, `Environment`, `Expiration`) | |

In 4–6 sentences, explain what AEJE-D-048 is showing and why the starter was incomplete.

---

## 3. Platform decision (ARCHITECT-1102)

| Criterion | ECS / Fargate | EKS | OpenShift |
|---|---|---|---|
| When BayPay picks it | | | |
| Control plane you operate | | | |
| Edge (ALB / Ingress / Route) | | | |
| IAM model | | | |
| What you refuse in a 90-minute lab | | | |

**ECS wins this quarter (one paragraph):**

**EKS wins when (one paragraph — not “more production”):**

**OpenShift wins when (one paragraph — Module 10 remains a home):**

**Refusal sentence** (no EKS/ROSA/NAT apply for realism):

---

## 4. Mapping inset

| Module 10 object | AWS object | Health / secret contract |
|---|---|---|
| Deployment | | |
| Service | | |
| Ingress / Route | | |
| Secret `baypay-db` | | |

---

## 5. IAM, secrets, KMS (SECURITY-1103)

| Field | Your answer |
|---|---|
| Execution role purpose | |
| Task role purpose | |
| Secret ARN shape (`baypay/payment/db` + JSON keys) | |
| What you grepped for (`changeme`, `AdministratorAccess`, `AKIA`) | |

In 4–6 sentences, explain why a combined `AdministratorAccess` role is not a deploy shortcut, and why the task role does not need `GetSecretValue` when ECS injects `valueFrom`.

---

## 6. Incident inset (INCIDENT-1104 — optional keep)

If you keep this as your AWS incident write-up:

| Field | Your answer |
|---|---|
| Symptom (merchant HTTP + task status) | |
| What you ruled out (and which gate) | |
| Stabilize vs remediate | |

Do not paste `solutions/INCIDENT-1104/`. Quote pack evidence only.

---

## 7. Cost summary (COST-1105)

Fill [PF-aws-cost.md](PF-aws-cost.md) in full. Copy the headline numbers here:

| Window | ALB | Fargate 256/512 | NAT (refused) |
|---|---|---|---|
| 1.5 hours | | | |
| 24 hours | | | |
| 7 days | | | |

Destroy list (ALB, ECS, ECR — your words):

---

## 8. Public-subnet trade-off

One paragraph: what `assign_public_ip = true` on a public subnet replaces, what isolation you gave up, and why NAT is the wrong 90-minute answer.

---

## 9. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, and Riley Okonkwo, in one sitting, why Fargate is the student default, when EKS or OpenShift still wins, how `BAYPAY_DB_*` is injected, and why Avery Chen’s POST must not depend on an idle ALB or a health check on `/`.
