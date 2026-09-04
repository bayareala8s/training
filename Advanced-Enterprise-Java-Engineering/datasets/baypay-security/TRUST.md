# BayPay trust and HA notes — Module 14

**Fictional company. Synthetic certificates and threats.** Students may read this file. Instructor incident RCAs live only under `solutions/`.

This is the **locked trust / HA / DR contract**. Lessons and labs reuse these names. Do not invent a second DNS zone, a second KMS key alias, or a live ACM apply requirement.

## Defaults

| Field | Value |
|---|---|
| App | `payment-service` (Java 21, Spring Boot 3.5.5) |
| Primary region | `us-west-2` |
| Teaching hostname | `payments.apps.baypay.example` (HTTPS) |
| Student ALB example | `pay-alb-student.baypay.example` |
| Port | `8080` in the task; TLS terminates at the load balancer (or Ingress) unless a lesson says mTLS |
| Health | `/actuator/health/liveness`, `/actuator/health/readiness` |
| Secrets | `BAYPAY_DB_*` from Secrets Manager / K8s Secret / Liberty `server.env` — never in git |
| KMS alias (teaching) | `alias/baypay-payments` |
| IAM | Task role ≠ execution role; no `AdministratorAccess` |
| Compute default | ECS on Fargate for AWS talk; Kubernetes/OpenShift remain valid homes (ARCHITECT-1102) |

## TLS / PKI (teaching names)

| Object | Teaching value |
|---|---|
| Public name | `payments.apps.baypay.example` |
| Issuer story | Public CA or ACM in `us-west-2` (paper describe; no required `apply`) |
| Validation | DNS CNAME in Route 53 hosted zone `baypay.example` (synthetic) |
| Leaf lifetime | 90 days unless a lab’s evidence says otherwise |
| Alert | Cert expiry **≤ 30 days** is a ticket; **≤ 7 days** is a page |
| Trust store | JVM default + any leftover Liberty / IHS plugin store — treat as a second object |

HTTP from a jump box to task `:8080` can succeed while merchants fail TLS. That is a **symptom class**, not an RCA. Quote this pack’s files.

INC-K8S-1005 (Module 10) was a **cluster Secret** hostname/expiry problem. This module’s certificate lab is **edge TLS / ACM / DNS validation**. Do not collapse the two into “TLS is broken.”

## Encryption

| Data | At rest | In transit |
|---|---|---|
| Payment rows (teaching Postgres) | Storage encryption + app does **not** store PAN | TLS to the database |
| Secrets | KMS-encrypted secret store | TLS |
| Backups | Encrypted; key is not the app password in git | — |

Tokenize or never persist PAN. Idempotency keys and payment ids are not secrets but are **not** metric labels (see OBSERVABILITY.md).

## HA teaching target

| Field | Value |
|---|---|
| Availability **architecture** goal | **99.99%** for `POST /api/v1/payments` (ARCHITECT-1401) |
| Rough budget | ~52 minutes/year |
| Default SLO in Module 13 dashboards | Still **99.9%** unless you explicitly change the contract |
| Failure domains | Task, AZ, ALB/node, region, identity/TLS, data store |
| Student apply | **Do not** create multi-AZ RDS, NAT, or a second region. Paper only. |

Single-region multi-AZ can be a 99.99% *design*. Multi-region is a **DR / RTO** conversation (DR-1403), not a free upgrade.

## DR teaching numbers (starting point — students may argue)

| Workload | RPO | RTO | Pattern to defend |
|---|---|---|---|
| Payment authorize / complete | Seconds (idempotent retry + replicated ledger intent) | 60 minutes regional | Pilot light or warm standby in a second region **on paper** |
| Merchant reporting | 24 hours | 24 hours | Backup restore |
| Leftover `BayPayCell` / `dmgr-east` | Not a DR target | Do not fail over to ND | Decommission path (Module 6) |

Primary region `us-west-2`. Paper secondary `us-east-1`. No student `apply` in the second region.

## Threat-model scope (SECURITY-1404)

In scope: `POST/GET /api/v1/payments`, `POST/GET /api/v1/refunds`, `Idempotency-Key`, frozen account `…222`, IAM/secrets, edge TLS, the modular monolith boundary.

Out of scope: real card-network certification, a real employer’s PCI ROC, attacking a live account.

## People and demo identities (synthetic)

Same as [../baypay-ops/OBSERVABILITY.md](../baypay-ops/OBSERVABILITY.md): Avery Chen, Riley Okonkwo, Priya Nair, Sam Okada, Jordan Voss, Morgan Hale.

Example payment id for security/DR labs: `c1402b22-0000-4000-8000-111111111402`.

## What you must not do

- Apply ACM, Route 53, KMS, a second-region stack, or multi-AZ RDS in a 90-minute lab.
- Commit private keys, `changeme`, or `AdministratorAccess` as the lesson.
- Treat “add a region” as the only 99.99% answer.
- Recreate `PaymentCluster` as the HA design.
- Put instructor RCAs in this file. INCIDENT-1402 is symptoms in the student pack only.

## Optional PAKS

- `docs/20-security/overview.md`
- `docs/18-reliability-and-resilience/overview.md`
- `docs/16-cloud-architecture/multi-region-architecture.md`
