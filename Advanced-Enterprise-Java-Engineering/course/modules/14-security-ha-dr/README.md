# Module 14 — Security, High Availability and Disaster Recovery

**Duration:** ~3.5 hours of lessons plus 4 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Defend BayPay and survive failure domains  
**Portfolio artifacts:** Security model from [student/worksheets/PF-security.md](../../../student/worksheets/PF-security.md) and DR strategy from [student/worksheets/PF-dr.md](../../../student/worksheets/PF-dr.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, certificate, IAM statement, KMS alias, and regional failover sketch you see is synthetic. Do not treat this pack as a real employer’s PCI ROC, trust store, or DR runbook.

**Delivery note:** this module is **paper only**. Do **not** apply ACM, Route 53 hosted zones, KMS keys, RDS Multi-AZ, or a second-region stack in a 90-minute lab. `terraform validate` on disk remains useful literacy from Module 12; it is not a license to create those objects. Prefer describe-and-defend. See [datasets/baypay-security/TRUST.md](../../../datasets/baypay-security/TRUST.md).

---

## Business context

Module 13 still pages Riley Okonkwo on a **99.9%** monthly SLO for `POST /api/v1/payments` (~43 minutes of equivalent downtime per 30-day month). That is the **ops** contract in [datasets/baypay-ops/OBSERVABILITY.md](../../../datasets/baypay-ops/OBSERVABILITY.md). This module’s **architecture** goal is **99.99%** for the same authorize path — roughly **52 minutes per year**. Do not silently upgrade a Module 13 dashboard to 99.99%. Do not treat “add `us-east-1`” as a free 99.99% button. Single-region multi-AZ in `us-west-2` can be a 99.99% *design*. Multi-region is a **DR / RTO** conversation (DR-1403).

Harbor Bike Co still charges Avery Chen `$84.00` through `POST /api/v1/payments`. The process is the same Java 21 / Spring Boot 3.5.5 modular monolith in `reference-apps/baypay`. The difference is the **trust and survival** path: merchants reach `https://payments.apps.baypay.example`, TLS terminates at the load balancer (or Ingress) unless a lesson says mTLS, the task listens on `8080`, and `BAYPAY_DB_*` never lives in git. The teaching KMS alias is `alias/baypay-payments`. The ECS **task role is not the execution role**. Nobody attaches `AdministratorAccess` so a lab “just works.”

INC-K8S-1005 (Module 10) was a **cluster Secret** hostname/expiry problem. This module’s certificate work is **edge TLS / ACM / DNS**. Do not collapse the two into “TLS is broken.” HTTP from a jump box to task `:8080` can succeed while merchants fail TLS. That is a **symptom class**, not an RCA. Lessons teach expiry alerts and validation as literacy. They do **not** name INCIDENT-1402’s root cause.

The locked trust / HA / DR contract lives in [TRUST.md](../../../datasets/baypay-security/TRUST.md). Reuse those names. Do not invent a second DNS zone, a second KMS alias, or a live ACM apply.

| Field | Locked value |
|---|---|
| App | `payment-service` (Java 21, Spring Boot 3.5.5) |
| Primary region | `us-west-2` |
| Paper secondary | `us-east-1` (describe only; no student apply) |
| Teaching hostname | `payments.apps.baypay.example` (HTTPS) |
| Student ALB example | `pay-alb-student.baypay.example` |
| Port | `8080` in the task; TLS at the edge unless a lesson says mTLS |
| Health | `/actuator/health/liveness`, `/actuator/health/readiness` |
| Secrets | `BAYPAY_DB_*` from Secrets Manager / K8s Secret / leftover Liberty `server.env` |
| KMS alias | `alias/baypay-payments` |
| IAM | Task role ≠ execution role; no `AdministratorAccess` |
| Compute default | **ECS on Fargate** for AWS talk; Kubernetes / OpenShift remain valid homes (ARCHITECT-1102) |
| Architecture goal | **99.99%** for `POST /api/v1/payments` (~52 minutes/year) |
| Ops SLO (Module 13) | Still **99.9%** unless you explicitly change the contract |

DR starting points (students may argue; they must defend):

| Workload | RPO | RTO | Pattern to defend |
|---|---|---|---|
| Payment authorize / complete | Seconds (idempotent retry + replicated ledger intent) | 60 minutes regional | Pilot light or warm standby in `us-east-1` **on paper** |
| Merchant reporting | 24 hours | 24 hours | Backup restore |
| Leftover `BayPayCell` / `dmgr-east` | Not a DR target | Do not fail over to ND | Decommission path (Module 6) |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen account | `22222222-2222-2222-2222-222222222222` |

On-call names: **Riley Okonkwo** (application), **Priya Nair** (SRE), **Sam Okada** (platform), **Jordan Voss** (release), **Morgan Hale** (WAS / leftover cell). Example payment id for security and DR labs: `c1402b22-0000-4000-8000-111111111402`. Payment happy path is still `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. A healthy Fargate task is not that sentence. Traditional WAS / `PaymentCluster` is the **source estate**, not the HA target. Never recommend ND-in-Docker.

---

## Learning objectives

After this module you can:

- Describe the edge TLS / PKI path for `payments.apps.baypay.example`, including 90-day leaf lifetime, expiry tickets (≤30 days) and pages (≤7 days), and why a healthy task on `:8080` does not prove merchants can handshake.
- Separate the ECS task role from the execution role, inject `BAYPAY_DB_*` from a secret store, and refuse `AdministratorAccess`.
- Encrypt payment rows and backups with `alias/baypay-payments`, keep TLS to the database, and never persist PAN.
- Place DNS, ALB, and health checks so the front door is a named failure domain — not a mystery.
- Design single-region multi-AZ 99.99% *on paper* and name failure domains: task, AZ, ALB/node, region, identity/TLS, data store.
- Defend RTO/RPO starting points and a paper `us-east-1` DR pattern without treating leftover cells as failover.
- Size HA/DR capacity (N+1, unused failover headroom, warm vs cold) without repeating L-13.5’s RPS / Hikari lesson.

---

## Prerequisites

- Modules 1–12, especially L-6.4 (`BAYPAY_DB_*`), L-9.5 (secrets not in layers), L-10.2 / INC-K8S-1005 (cluster Secret TLS is a *different* plane), L-11.4 (ALB / Route 53 literacy), L-11.5 (task role vs execution role), L-12.1 (no secrets in git).
- Module 13 ops contract in [OBSERVABILITY.md](../../../datasets/baypay-ops/OBSERVABILITY.md): 99.9% SLO, P99 < 400 ms teaching latency, no PAN on metric labels. If Module 13 lessons are still in flight, OBSERVABILITY.md plus TRUST.md are enough. L-13.5 (RPS / Hikari / JVM capacity) is the **ops** capacity lesson; L-14.7 is the **HA/DR** capacity lesson — cross-link, do not copy.
- Comfort reading HCL, IAM JSON, and a certificate PEM. A live AWS account is **not** required and must not be used to apply ACM, Route 53, KMS, Multi-AZ RDS, or a second region for these labs.

You do **not** need a licensed Liberty cell, a real ACM certificate, or card-network certification. Paper plus the locked names is enough.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional. Lessons teach **trust, HA method, and DR literacy**. They do not name the root cause of INCIDENT-1402.

| Id | Title | What it unlocks |
|---|---|---|
| [L-14.1](lessons/L-14.1.md) | TLS and PKI | Edge certs, expiry alerts, validation literacy, AEJE-D-063 |
| [L-14.2](lessons/L-14.2.md) | IAM and secrets | Task role ≠ execution role; no `AdministratorAccess` |
| [L-14.3](lessons/L-14.3.md) | Encryption | `alias/baypay-payments`, at-rest / in-transit, no PAN |
| [L-14.4](lessons/L-14.4.md) | Networking, DNS and load balancing | Front door as a failure domain |
| [L-14.5](lessons/L-14.5.md) | HA and failure domains | 99.99% design, AEJE-D-064 |
| [L-14.6](lessons/L-14.6.md) | RTO, RPO and DR | Paper `us-east-1`, AEJE-D-066 |
| [L-14.7](lessons/L-14.7.md) | Capacity planning | N+1 and DR headroom; not a repeat of L-13.5 |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [ARCHITECT-1401](../../../labs/ARCHITECT-1401/README.md) | ARCHITECT | Design BayPay for 99.99 percent | L-14.5 |
| [INCIDENT-1402](../../../labs/INCIDENT-1402/README.md) | INCIDENT | Certificate expiration | L-14.1 |
| [DR-1403](../../../labs/DR-1403/README.md) | ARCHITECT | Regional outage tabletop | L-14.6 |
| [SECURITY-1404](../../../labs/SECURITY-1404/README.md) | SECURITY | Threat model BayPay | L-14.2, L-14.3 |

Time-box ARCHITECT, DR, and SECURITY labs at 60–90 minutes. INCIDENT-1402 at 45–75 minutes. Student incident guide shows **symptoms only**. Work the pack’s gates. Do not open `solutions/INCIDENT-1402/` until the worksheet has hypothesis, evidence, next investigation, stabilize, remediate, and comms.

Treat “merchants fail TLS while tasks stay healthy” as a *symptom class*, not a closed RCA. Quote *this* pack’s evidence. A lucky label that matches the title does **not** max Diagnostic method. Lessons do **not** lecture that pack’s cause.

All four labs are **paper**. Do not apply ACM, Route 53, KMS, Multi-AZ RDS, or a second-region stack.

---

## Assessment and portfolio

1. Complete ARCHITECT-1401, INCIDENT-1402, DR-1403, and SECURITY-1404 with gated evidence on the incident.
2. Take [Q-14](../../quizzes/Q-14.md) when your cohort opens it.
3. Export the security model using [student/worksheets/PF-security.md](../../../student/worksheets/PF-security.md) and the DR strategy using [student/worksheets/PF-dr.md](../../../student/worksheets/PF-dr.md).

Those two worksheets are the Module 14 portfolio artifacts. Module 15 will assume you can name the edge hostname, the KMS alias, the 99.99% vs 99.9% split, and why `dmgr-east` is not a failover target — without reciting an instructor RCA.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/20-security/overview.md`, `docs/18-reliability-and-resilience/overview.md`, and `docs/16-cloud-architecture/multi-region-architecture.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). They deepen trust boundaries, failure domains, and multi-region patterns. This module stands alone without them.

---

## Guardrails

- **Paper only.** No student apply of ACM, Route 53, KMS, RDS Multi-AZ, NAT “for realism,” or a second region.
- Lessons do **not** name INCIDENT-1402’s RCA. Student pack is symptoms; instructor solutions live under `solutions/`.
- Reuse TRUST.md names: `payments.apps.baypay.example`, `alias/baypay-payments`, primary `us-west-2`, paper secondary `us-east-1`.
- Task role ≠ execution role. No `AdministratorAccess`. No private keys, `changeme`, or `BAYPAY_DB_PASSWORD` in git.
- 99.99% is this module’s architecture goal (~52 min/year). 99.9% remains the Module 13 ops SLO.
- Single-region multi-AZ can be a 99.99% *design*. Multi-region is DR, not a free availability upgrade.
- Leftover `BayPayCell` / `dmgr-east` / `PaymentCluster` is **not** a DR or HA target. Do not recommend ND-in-Docker.
- Never set `-Xmx` equal to the cgroup / Fargate memory limit.
- Tokenize or never persist PAN. Idempotency keys and payment ids are not metric labels.
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`.
