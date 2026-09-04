# Portfolio worksheet — Terraform, Ansible and CI/CD

**Artifact:** Module 12 / [BUILD-1201](../../labs/BUILD-1201/README.md) · [BUILD-1202](../../labs/BUILD-1202/README.md) · [BUILD-1203](../../labs/BUILD-1203/README.md) · [BUILD-1204](../../labs/BUILD-1204/README.md) · [INCIDENT-1205](../../labs/INCIDENT-1205/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-055 (modules) · AEJE-D-056 (pipeline) · AEJE-D-057 (rollback) · AEJE-D-058 (Ansible)  
**Account notes:** [datasets/baypay-aws/ACCOUNT.md](../../datasets/baypay-aws/ACCOUNT.md)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste instructor solution text. Do not put access keys or `BAYPAY_DB_PASSWORD` values in this file. `terraform apply` and live GitHub Actions are optional — say whether you used them.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | |
| Terraform used (`validate` / `plan` / `apply` / files only) | |
| Ansible used (`syntax-check` / run local / files only) | |
| GitHub Actions used (yes / files only) | |
| Reference commit or branch | |

---

## 2. Terraform root (BUILD-1201)

Region and tags from ACCOUNT.md:

| Field | Your answer |
|---|---|
| `variable "region"` default | |
| Provider region expression | |
| Tags (Course, Module, Lab, Environment, Expiration) | |
| ECR repository name | |
| Outputs you exported | |
| Resources you **refused** to add (ALB, NAT, ECS, RDS, EKS) | |
| `terraform validate` result | |

In 4–6 sentences, explain why the env skeleton is ECR-plus-tags and not a Fargate stack.

---

## 3. Reusable modules (BUILD-1202)

Cite AEJE-D-055.

| Field | Your answer |
|---|---|
| `modules/ecr` inputs / outputs | |
| `modules/ecs_service` `container_port` | |
| `modules/ecs_service` health path | |
| Image reference (must not be `:latest`) | |
| Cheap resource inside `ecs_service` (if any) | |

What belongs in a module variable versus a root `local`? One paragraph.

---

## 4. Configuration automation (BUILD-1203)

Cite AEJE-D-058.

| Field | Your answer |
|---|---|
| How `BAYPAY_DB_HOST` is set | |
| Teaching host value | |
| How `BAYPAY_DB_URL` is built | |
| Liberty `server.env` path you templated | |
| Where the password is **not** | |
| Connection plugin (must be local) | |

In 4–6 sentences, explain why Boot and Liberty share one host var.

---

## 5. CI/CD (BUILD-1204)

Cite AEJE-D-056.

| Field | Your answer |
|---|---|
| Test job: Java version | |
| Test command | |
| How publish depends on test | |
| Image tag | |
| Why `:latest` is not the deploy tag | |
| How credentials appear (secret **names** only) | |

---

## 6. Failed deploy (INCIDENT-1205)

Cite AEJE-D-057. Use **your** worksheet words. Do not paste `solutions/INCIDENT-1205/`.

| Field | Your answer |
|---|---|
| Gate 1 quote (pipeline) | |
| Gate 2 quote (deployments / health) | |
| Gate 3 quote (task definition) | |
| Stabilize (last healthy revision / image) | |
| Remediate (smoke port, tags) | |
| What you did **not** bounce | |

---

## 7. Least-privilege and cost

| Field | Your answer |
|---|---|
| IAM you would grant for 1201 apply (ECR only) | |
| IAM you would grant for 1205 rollback (describe + update-service) | |
| What you would refuse (`AdministratorAccess`, access keys in git) | |
| Optional apply cost you estimated, or `$0` validate-only | |
| Cleanup you actually performed | |

---

## 8. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, Jordan Voss, and Riley Okonkwo, in one sitting, how the Terraform root, the two modules, the Ansible env render, and the Java 21 pipeline keep Avery Chen’s POST on port 8080 — and what you do first when a green pipeline still fails ALB health.

---

## Honesty

- [ ] I did not open `solutions/BUILD-120N/` or `solutions/INCIDENT-1205/` before attempting the work
- [ ] I requested INC-AWS-1205 evidence in the documented gate order
- [ ] Every AWS claim has a source (ACCOUNT.md, my `.tf`, or a pack file)
- [ ] I did not paste an instructor RCA
- [ ] I did not put an access key or a live password in this file
- [ ] I did not apply ALB, NAT, EKS, or RDS for these labs
- [ ] If I applied ECR, I destroyed it in `us-west-2`
