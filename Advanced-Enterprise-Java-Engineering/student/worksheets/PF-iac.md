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
| Date | 2026-09-06 |
| Terraform used (`validate` / `plan` / `apply` / files only) | **`validate`** on `labs/BUILD-1201/work/` (`init -backend=false`). No apply. |
| Ansible used (`syntax-check` / run local / files only) | **files only** (`ansible-playbook` not installed). Tree: `labs/BUILD-1203/work/` |
| GitHub Actions used (yes / files only) | **files only** — `labs/BUILD-1204/work/.github/workflows/baypay.yml` |
| Reference commit or branch | Downloads workspace; starter left incomplete |

---

## 2. Terraform root (BUILD-1201)

Region and tags from ACCOUNT.md:

| Field | Your answer |
|---|---|
| `variable "region"` default | **`us-west-2`** (starter had hardcoded `us-east-1`) |
| Provider region expression | `region = var.region` |
| Tags (Course, Module, Lab, Environment, Expiration) | `Course=AEJE`, `Module=12`, `Lab=BUILD-1201`, `Environment=student`, `Expiration=2026-09-06` (`default_tags`) |
| ECR repository name | `baypay/payment-service` (IMMUTABLE + scan-on-push; untagged expire 7d) |
| Outputs you exported | `repository_url`, `repository_arn` |
| Resources you **refused** to add (ALB, NAT, ECS, RDS, EKS) | No `aws_ecs_cluster`, `aws_lb`, `aws_nat_gateway`, `aws_db_instance`, EKS |
| `terraform validate` result | **Success** (`terraform init -backend=false` then validate; no apply) |

In 4–6 sentences, explain why the env skeleton is ECR-plus-tags and not a Fargate stack.

This root is the **registry contract** later labs push into — not Avery’s runtime. Finance finds `Course=AEJE` / `Expiration` on one cheap repo. A Fargate + ALB stack here would re-litigate BUILD-1101 and leave an **idle ALB (~$0.54/day)** on a Module 12 skeleton (COST-1105). ECS stays the student **compute** default; it is not this apply. `validate` does not prove `apply` is cheap — it only checks HCL. Local state is honest for a 75-minute sandbox (no remote backend); you lose lock/sharing and you must not commit `tfstate`. BUILD-1202 will module this; one file that creates ECR is the honest first root.

---

## 3. Reusable modules (BUILD-1202)

Cite AEJE-D-055. Working tree: `labs/BUILD-1202/work/` (starter left hollow).

| Field | Your answer |
|---|---|
| `modules/ecr` inputs / outputs | In: `name`, `region` (default `us-west-2`), `tags`. Out: `repository_url`, `repository_arn`. Resource: IMMUTABLE `aws_ecr_repository`. |
| `modules/ecs_service` `container_port` | Default **8080**; root passes `8080` explicitly |
| `modules/ecs_service` health path | Default **`/actuator/health/liveness`**; root passes it explicitly |
| Image reference (must not be `:latest`) | `…/baypay/payment-service:3.9.2` (`var.container_image`) |
| Cheap resource inside `ecs_service` (if any) | `aws_cloudwatch_log_group` `/ecs/<name>` retention 7d — **not** `aws_lb` / `aws_ecs_service` |

What belongs in a module variable versus a root `local`? One paragraph.

A **module variable** is a contract another root will set: `name`, `container_port`, `health_check_path`, `image`, `region`. A **root `local`** is something only this caller knows (this lab’s extra tag map, how we compose `Course=AEJE`). Passing `container_port = 8080` even though the default is 8080 is the teaching point: reviewers and INCIDENT-1205 see the ACCOUNT.md number at the call site. `:latest` is a broken input — floating tags are how a payment image silently changes. Log group is the cheap stand-in so the module has a real resource without an ALB (~$0.54/day). One `ecs_service` module postpones separate `task_definition` / `alb` modules until we apply compute; the **path** stays a variable so the ALB cannot drift back to `/`. One ECR module instance per environment (not per lab tag) is enough until a second caller appears.

---

## 4. Configuration automation (BUILD-1203)

Cite AEJE-D-058. Working tree: `labs/BUILD-1203/work/` (starter left as mkdir-only).

| Field | Your answer |
|---|---|
| How `BAYPAY_DB_HOST` is set | `group_vars/all.yml` → `baypay_db_host` → both `.j2` files emit `BAYPAY_DB_HOST=` |
| Teaching host value | **`db-east.baypay.example`** |
| How `BAYPAY_DB_URL` is built | `jdbc:postgresql://{{ baypay_db_host }}:{{ baypay_db_port }}/{{ baypay_db_name }}` → `…://db-east.baypay.example:5432/baypay` |
| Liberty `server.env` path you templated | `templates/server.env.j2` → `rendered/server.env` |
| Where the password is **not** | Not in git. `lookup('env', 'BAYPAY_DB_PASSWORD')` (empty default). No `changeme`. |
| Connection plugin (must be local) | `connection: local` / `ansible_connection=local`. `gather_facts: false`. No SSH. |

In 4–6 sentences, explain why Boot and Liberty share one host var.

Avery still hits **8080** on whichever process is live this week — Fargate Boot or the remaining Liberty cell. If those files are hand-copied, `db-east` drifts and one estate talks to yesterday’s host. One `baypay_db_host` renders both `payment-service.env` and Liberty `server.env` (AEJE-D-058). Password stays in the process env or vault at **run**, not in the role (FIX-902 / SECURITY-1103). Templating prevents two slightly different `server.env` files; baking env into the image prevents ConfigMap mistakes by creating a rebuild-per-env. Terraform `templatefile` is enough when the only consumer is HCL; Ansible stays when Liberty jump-host files still exist. `connection: local` keeps blast radius on the laptop — SSH to `dmgr-east` from a $0 lab is the wrong completion.

---

## 5. CI/CD (BUILD-1204)

Cite AEJE-D-056. Working file: `labs/BUILD-1204/work/.github/workflows/baypay.yml` (starter left publish-only / `:latest`).

| Field | Your answer |
|---|---|
| Test job: Java version | **21** (`actions/setup-java` Temurin). Runs on push to `main` **and** every PR. |
| Test command | `./mvnw -B -pl payment-service -am test` in `reference-apps/baypay` (Wrapper, not `mvn`, not `-DskipTests`) |
| How publish depends on test | `needs: test` plus `if: push && ref == main` — PRs test; they do not publish |
| Image tag | `baypay/payment-service:${{ github.sha }}` |
| Why `:latest` is not the deploy tag | SHA is immutable and rollback-addressable. `:latest` moves; INCIDENT-1205 is that pager. |
| How credentials appear (secret **names** only) | `${{ secrets.REGISTRY_USERNAME }}` / `${{ secrets.REGISTRY_PASSWORD }}` — no `AKIA`, no password literal |

`needs` vs parallel: parallel would let a red `./mvnw test` still push. Same jobs on Jenkins/Tekton: Java 21, Wrapper test, SHA tag, secret names — the YAML brand is not the gate. Skipping tests on `main` to ship faster is what Avery pays for with retries. Image build stays in **publish** (isolation); test job stays a JVM. A later smoke GET on 8080 (INCIDENT-1205) is not a substitute for unit tests.

---

## 6. Failed deploy (INCIDENT-1205)

Cite AEJE-D-057. Use **your** worksheet words. Do not paste `solutions/INCIDENT-1205/`.

| Field | Your answer |
|---|---|
| Gate 1 quote (pipeline) | `Job test skipped` … `docker build -t …:3.8.9-debug -t …:latest` … `Skipping image smoke` … `revision=88` … `conclusion=success` |
| Gate 2 quote (deployments / health) | `ROLLBACK … ELB_HEALTH_CHECK_FAILURE`; PRIMARY **`payment-service:80`** / `3.8.0`; TG **8080** `/actuator/health/liveness`; `(port 8080) is unhealthy` |
| Gate 3 quote (task definition) | **88** `SERVER_PORT=9080` / image `3.8.9-debug`; **80** `SERVER_PORT=8080` / `3.8.0`; `containerPort` still 8080 |
| Stabilize (last healthy revision / image) | Leave **`payment-service:80` / 3.8.0** (rollback already completed 22:05Z) |
| Remediate (smoke port, tags) | Pipeline: `./mvnw test` + smoke **GET 8080** `/actuator/health/liveness`; deploy **`${{ github.sha }}`**, never `:latest` |
| What you did **not** bounce | db-east / Postgres / `dmgr-east`. Did not push `:latest`, retarget ALB to 9080, or scale to zero. |

---

## 7. Least-privilege and cost

| Field | Your answer |
|---|---|
| IAM you would grant for 1201 apply (ECR only) | Create/describe/tag on `baypay/payment-service` — not `AdministratorAccess` |
| IAM you would grant for 1205 rollback (describe + update-service) | `ecs:DescribeServices`, `ecs:DescribeTaskDefinition`, `ecs:UpdateService` (pin **80**). Not `iam:CreateAccessKey` |
| What you would refuse (`AdministratorAccess`, access keys in git) | Admin on the task or the on-call user; `AKIA` in workflow; `changeme` in task JSON; laptop `:latest` push |
| Optional apply cost you estimated, or `$0` validate-only | **$0** — validate / files only. No ALB/ECS apply. |
| Cleanup you actually performed | No `us-west-2` stack this module. Starters left incomplete. |

---

## 8. Interview snippet (Staff, 6–8 sentences)

The Terraform root (1201) is ECR + ACCOUNT.md tags in `us-west-2` — not an ALB. Modules (1202 / AEJE-D-055) make **8080** and `/actuator/health/liveness` call-site variables; image is `:3.9.2`, never `:latest`. Ansible (1203 / AEJE-D-058) renders the same `BAYPAY_DB_HOST=db-east.baypay.example` into Boot `.env` and Liberty `server.env`; password is `lookup('env')`, not git. The pipeline (1204 / AEJE-D-056) is Java **21** `./mvnw test` on every PR, then publish **`needs: test`** and tag `${{ github.sha }}`. Credentials are `${{ secrets.REGISTRY_* }}` names only. INC-1205: CI was green (`3.8.9-debug`, no tests/smoke); **88** listened on **9080** while TG stayed **8080**; circuit breaker restored **`payment-service:80` / 3.8.0**. First move is confirm PRIMARY 80 — not push `:latest`, not retarget 9080. Remediate with smoke on **8080**.

---

## Honesty

- [x] I did not open `solutions/BUILD-120N/` or `solutions/INCIDENT-1205/` before attempting the work
- [x] I requested INC-AWS-1205 evidence in the documented gate order
- [x] Every AWS claim has a source (ACCOUNT.md, my `.tf`, or a pack file)
- [x] I did not paste an instructor RCA
- [x] I did not put an access key or a live password in this file
- [x] I did not apply ALB, NAT, EKS, or RDS for these labs
- [x] If I applied ECR, I destroyed it in `us-west-2`
