# CAPSTONE-3 — Instructor solution

**Do not share this folder with students before they submit PF-cloud.md and a validate-green tree.**

This is the Staff narrative for Cloud BayPay. Students are **not** required to `terraform apply`. Opening this folder first is a failed Diagnostic method score. There is no extra `.tf` tree here on purpose: the course already ships the contracts in [infrastructure/terraform/baypay-ecs](../../infrastructure/terraform/baypay-ecs/), [solutions/BUILD-1201](../BUILD-1201/), [solutions/BUILD-1202](../BUILD-1202/), [solutions/BUILD-1101](../BUILD-1101/), and [solutions/SECURITY-1103](../SECURITY-1103/). Score the **composition** and the worksheet, not a novel module catalog.

---

## What the capstone is

CAPSTONE-3 is the **delivery** of Modules 11–12. AEJE-D-072 is the target: merchants over TLS → ALB (or a Route, if the home is OpenShift) → `payment-service` on port **8080** → Secrets Manager → a teaching database. AEJE-D-071 is the ND source estate. Students must not stabilize the cloud path by bouncing `dmgr-east`.

**Apply default:** ECS on Fargate in `us-west-2`.  
**Design homes that still win:** EKS (existing Kubernetes / CRDs) and OpenShift (Routes, SCCs, operators) — ARCHITECT-1102.  
**Forbidden apply:** NAT Gateway, EKS/ROSA, RDS, RDS Multi-AZ, always-on EC2, OpenSearch, a second region.

Grade bar: `terraform validate` + [PF-cloud.md](../../student/worksheets/PF-cloud.md). Optional apply neither raises nor lowers Technical accuracy if destroy is honest.

---

## Required contracts

```text
region:     us-west-2
app:        payment-service  Java 21 / Spring Boot 3.5.5
image:      baypay/payment-service:<immutable-tag>   # never :latest
port:       8080
health:     /actuator/health/liveness   matcher 200
secrets:    BAYPAY_DB_* from Secrets Manager valueFrom + named CMK
compute:    ECS on Fargate  cpu 256  memory 512
subnets:    two public + IGW; assign_public_ip = true
slo:        99.9% monthly on POST /api/v1/payments server-success SLI
            (~43 minutes error budget / 30d). 99.99% = Module 14, say so.
tags:       Course=AEJE Module=Capstone Lab=CAPSTONE-3 Environment=student Expiration
iac:        required_providers.aws; variable "region" default us-west-2
            modules/ecr + service contract (port + health path)
validate:   terraform init -backend=false && terraform validate
apply:      optional; destroy same day
scope:      no NAT, no EKS, no RDS Multi-AZ, no access keys, no changeme
```

People (synthetic): Avery Chen (`11111111-1111-1111-1111-111111111111`), Priya Nair (SRE / SLO), Riley Okonkwo (app on-call / health path), Jordan Voss (release / image tag), Sam Okada (platform / ALB + Terraform).

---

## Architecture answer (AEJE-D-072)

Merchants (Avery Chen’s client) enter at an HTTP edge. On the student apply path that edge is an **ALB** in two public subnets in `us-west-2`. The target group probes **`/actuator/health/liveness`** on **8080**. A Fargate task (256/512) runs the image from ECR. The execution role pulls the image, writes logs, reads `arn:aws:secretsmanager:us-west-2:123456789012:secret:baypay/payment/db*`, and decrypts one CMK. The JVM receives `BAYPAY_DB_*` as injected environment. The task role is a separate principal and does **not** need `GetSecretValue` for this app.

Teaching host `pay-alb-student.baypay.example` is a name, not a Route 53 lab. Student apply uses the AWS-generated DNS name. Profile `local` / H2 keeps RDS off the invoice.

If the chosen **production** home is OpenShift, the same process sits behind `payment-route`; if EKS, behind Ingress. The Actuator URL does not change. Saying “EKS is more production” fails Technical accuracy.

### Service list (scored)

| In the apply column | In the design-only column |
|---|---|
| ECR, optional Fargate+ALB, IAM JSON, Secrets/KMS paper, CloudWatch logs | EKS, OpenShift, RDS Multi-AZ, NAT, second region, ACM, Route 53 |

A worksheet that puts EKS or NAT in the apply column as “required for the capstone” fails Production awareness regardless of mermaid quality.

---

## Platform pick (ARCHITECT-1102, restated)

| Home | BayPay this quarter | Apply in this capstone? |
|---|---|---|
| ECS/Fargate | One Spring Boot service, AWS-native IAM, no custom controllers | **Yes — student default** |
| EKS | Estate already Kubernetes; CRDs / sidecars you will not rewrite as task defs | No — paper only |
| OpenShift | Module 10 Routes / SCCs / operators already the production home | No — paper only |

Refusal sentence graders should see: *We will not apply EKS, ROSA, or a NAT Gateway for realism in a 4–8 hour capstone.*

Mapping inset: Deployment ≈ task + service; Service / Route ≈ ALB target group; Secret `baypay-db` ≈ Secrets Manager `baypay/payment/db`; probe path stays `/actuator/health/liveness` in every home.

---

## IaC answer

Students may compose any of:

1. **Course skeleton** `infrastructure/terraform/baypay-ecs` — provider pin, `us-west-2`, ACCOUNT.md tags, one immutable ECR. Validate-green. Does **not** create ALB/Fargate; the worksheet must still write the ALB health contract.
2. **BUILD-1202 modules** (`solutions/BUILD-1202/`) — `modules/ecr` + `modules/ecs_service` with `container_port` default 8080 and `health_check_path` default `/actuator/health/liveness`. The service module’s cheap resource is a log group, not a live `aws_ecs_service`. That postponement is intentional.
3. **BUILD-1101 apply shape** (`solutions/BUILD-1101/`) — VPC, two public subnets, ALB, Fargate service. Health path and `containerPort` must be present. Retag `Module=Capstone`, `Lab=CAPSTONE-3`.

A passing packet **names the gap**: skeleton/modules prove the registry and the port/health interface; BUILD-1101 is the file that would create the ALB. Inlining ECR in the root and leaving `modules/` empty is a weak module story (same as BUILD-1202). Adding NAT/ALB to the 1202 module lab “to finish the name” fails Cost.

`terraform validate` does not prove `apply` is cheap. Students who treat a green validate as a license to skip the idle-ALB briefing fail Production awareness.

Image input must not be `:latest`. BUILD-1204’s `${{ github.sha }}` (or another immutable tag) is the honest pin. Publish `needs: test`.

---

## Secrets and KMS answer

Same as SECURITY-1103:

- Two roles, both trust `ecs-tasks.amazonaws.com`.
- Execution: ECR auth + pull on `baypay/payment-service`, logs on the payment log group, `GetSecretValue` on one secret, `kms:Decrypt` on one CMK. No `Action: "*"`.
- Task: no `AdministratorAccess`, no copied `GetSecretValue` unless the student writes why the JVM calls the API (this app does not).
- Task definition: `secrets` with `valueFrom` ARNs including JSON keys (`:url::`, `:username::`, `:password::`). No plaintext `BAYPAY_DB_PASSWORD`.
- KMS key policy: account root administers; execution role decrypts; no `Principal: "*"`.

A combined admin role “so the first deploy would work” is a day-two account compromise. Score it as a Security fail even if Terraform validates.

---

## Monitoring and SLO answer

Locked in OBSERVABILITY.md. **Do not silently upgrade to 99.99%.**

| Field | Answer |
|---|---|
| SLI | Successful `POST /api/v1/payments` / (successful + server failures). Server failure = 5xx, timeout, or dependency failure that becomes 5xx. Ordinary 4xx stay off default burn (429 may be capacity if the cohort says so). |
| SLO | **99.9%** monthly availability on that SLI |
| Error budget | ~43 minutes / 30-day month |
| Latency | P99 **< 400 ms** on the teaching happy path |
| Page | Fast and slow SLO burn; saturation that predicts burn (Hikari pending, thread pool maxed) |
| Do not page | CPU > 80%; log line contains ERROR |

99.99% is ARCHITECT-1401 / Module 14 — a different failure-domain conversation (not “edit the Grafana tile”). A packet that only says 99.99% without naming the upgrade fails Technical accuracy.

Labels refused on Micrometer: `customerId`, `accountId`, `Idempotency-Key`, raw `paymentId`, PAN. Avery’s identifiers belong in logs/traces, not on cardinality.

Paper dashboards are enough. Live Grafana / AMP / CloudWatch Container Insights are not required and Insights is another SKU.

---

## Scaling and resilience answer

**Student apply:** `desired_count = 1`, 256/512, Container Insights off. That is a lab, not Harbor Market peak.

**Paper production:** scale on something closer to the SLO (in-flight POSTs, ALB request count, or error-rate adjacent signals) with a **max replica cap** derived from pool size so tasks cannot DDoS the teaching database. CPU target tracking is literacy and a useful ceiling; it is the wrong *sole* signal when the JVM is wait-bound on Hikari. Scale-down is slow. Do not HPA on heap. Do not set `-Xmx` equal to the Fargate memory limit.

**Resilience this week:** two public AZs for the ALB; unhealthy target → replace the task; rollback = last **healthy** task definition / immutable tag (INCIDENT-1205). Do not bounce Postgres. Do not bounce `dmgr-east`. Do not push `:latest` from a laptop. RDS Multi-AZ is a valid **design** sentence for a later HA conversation; applying it here is a lab failure.

RUNNING is a container-process fact. Healthy is a target-group fact. INCIDENT-1104: path `/` → Actuator 404 → unhealthy → merchant 502/503. Fix the path; bake it into Terraform; do not widen the SG.

---

## Cost answer (teaching USD, `us-west-2`)

| Resource | Hour | 24 h | 7 d |
|---|---|---|---|
| ALB (LCU ≈ 0) | $0.0225 | ≈ $0.54 | ≈ $3.78 |
| Fargate 256/512 | ≈ $0.01234 | ≈ $0.30 | ≈ $2.07 |
| NAT (refused) | $0.045 + data | ≈ $1.08 | ≈ $7.56 |
| EKS CP (refused) | $0.10 | ≈ $2.40 | ≈ $16.80 |

Same-day apply session: **$0.15–$2.00**. Overnight idle ALB: **~$0.54** with zero traffic. Forgotten week: **~$5–$15**. ECR still bills after the service is gone. `desired_count = 0` does not stop the ALB. `Expiration` tags do not destroy. Destroy ALB, ECS, ECR (and any secret/CMK) the **same day**.

Paper + `$0` validate is a complete pass. Apply = dollars/day ALB + Fargate.

---

## Failure scenario (scored narrative)

Priya pages: Harbor Market 502/503 on `pay-alb-student`. Jordan says CI was green. Sam’s `ecs describe-tasks` shows RUNNING. Riley finds the target group probing `/` or a tag that fails liveness. Stabilize: point health at `/actuator/health/liveness` and/or roll back to the last healthy revision. Remediate: bake path + immutable tag into modules and the pipeline. Do not invent RDS down, do not open 8080 to `0.0.0.0/0`, do not attach admin, do not add NAT, do not fail over to BayPayCell.

A second failure: Finance finds an ALB that ran Thursday–Monday. That is a process failure, not an SLO miss. Destroy checklist is part of the architecture.

---

## What the student files should look like

| Deliverable | Pass intent |
|---|---|
| PF-cloud.md | Filled in the student’s words; AEJE-D-072; service list; platform table; validate result; 99.9% SLO; cost multiply; destroy list |
| Working `.tf` | Provider pin, `us-west-2`, tags, ECR and/or modules with port+health; no keys; no NAT/EKS/RDS |
| IAM/task JSON (paper) | Two roles; `valueFrom`; no `changeme` |
| Optional apply | Same-day `terraform destroy`; leftovers confirmed gone in `us-west-2` |

Resource names may differ. Health variable may be `health_path` or `health_check_path`. A student who only validates `baypay-ecs` must still write the ALB health contract on the worksheet.

---

## Scoring notes

- `apply` absence must **not** fail the capstone.
- Health path `/` or missing `containerPort` caps Technical accuracy.
- Silent 99.99% SLO caps Technical accuracy unless the student names the Module 14 upgrade.
- “Always EKS” or “OpenShift is legacy” caps Technical accuracy.
- Opening this folder first caps Diagnostic method.
- Applying NAT, EKS, or RDS Multi-AZ caps Production awareness (and Efficiency) regardless of mermaid quality.
- `AdministratorAccess` or plaintext passwords cap Security.
- Empty PF-cloud.md caps Communication.
- Leaving an ALB up overnight caps Production awareness even if the architecture sentences were excellent.

Full marks require the composition: D-072 + validate + least privilege + 99.9% + idle-ALB briefing + destroy same day (or a clear `$0` validate path).
