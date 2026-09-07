# Portfolio worksheet — Security model and 99.99% HA

**Artifact:** Module 14 / [ARCHITECT-1401](../../labs/ARCHITECT-1401/README.md) · [INCIDENT-1402](../../labs/INCIDENT-1402/README.md) · [SECURITY-1404](../../labs/SECURITY-1404/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-064 (failure domains) · AEJE-D-065 (HTTPS handshake incident) · AEJE-D-067 (threat model)  
**Trust notes:** [datasets/baypay-security/TRUST.md](../../datasets/baypay-security/TRUST.md)  
**Ops notes:** [datasets/baypay-ops/OBSERVABILITY.md](../../datasets/baypay-ops/OBSERVABILITY.md)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste instructor solutions. Do not put access keys, private keys, or `BAYPAY_DB_PASSWORD` values in this file. Do not write exploit steps or payloads. `terraform apply`, ACM, Route 53, and a second region are **not** required — say that you stayed on paper.

The Module 14 portfolio artifact is this page (**security model + 99.99% HA**) plus [PF-dr.md](PF-dr.md) (**DR strategy**).

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | 2026-09-07 |
| Path (files only — required) | **files only** — PF-security.md. No ACM / Route 53 / RDS / NAT / `us-east-1` apply. |
| Region (must be `us-west-2` for the HA design) | **`us-west-2`** |
| Paper DR region (name only; do not apply) | `us-east-1` (DR-1403; named only) |
| Reference commit or branch | Downloads workspace; `solutions/ARCHITECT-1401/` not opened |

---

## 2. 99.99% failure domains (ARCHITECT-1401)

Cite AEJE-D-064. Teaching host `payments.apps.baypay.example`. Architecture goal **99.99%** (~52 minutes/year). Module 13 operated SLO stays **99.9%** unless you write an explicit contract change.

| Domain | What fails | Merchant symptom | Survives multi-AZ single-region? | What still kills the year |
|---|---|---|---|---|
| Task | One Fargate JVM OOM/crash (`desired_count = 1`) | Late or dropped `POST /api/v1/payments` until replace | **Yes** if `desired_count` ≥ 2 and ALB health on `8080` | One fat JVM (`-Xmx` = cgroup) or count=1 — 100% of authorize |
| AZ | `us-west-2a` (or one subnet) gone | Timeout / 5xx if all tasks live in that AZ | **Yes** if tasks + ALB subnets in ≥2 AZs | All tasks / one ALB subnet in a single AZ |
| ALB / edge | Regional balancer or DNS name `payments.apps.baypay.example` | Harbor Market cannot reach the host (or hits a dead TG) | ALB is **multi-AZ and still regional** — AZ loss of one node ok | ALB/DNS/region object down; Jordan treating ALB as “already multi-region” |
| Identity / TLS | ACM leaf, DNS validation, IAM deny, KMS `alias/baypay-payments` | Merchants fail **HTTPS**; jump-box HTTP to `:8080` can still 200 | In-region: expiry pages, least privilege | Forgotten leaf / failed handshake for a day; HTTP≠HTTPS. Same 52 minutes as a dead AZ. |
| Datastore | Teaching Postgres / Hikari writer | Creates stall or 5xx if the writer AZ dies | **On paper** multi-AZ — do **not** apply RDS | Single-AZ datastore; student `apply` is a lab fail, not extra credit |
| Region | `us-west-2` gone or impaired | Authorize stops for the outage | **No** — the whole drawing is one region | A 60–90 min region loss **spends (and exceeds) the year**. That is DR-1403, not “add a region” as HA. |

**Fifty-two minutes (one paragraph):** what fits, what does not. Contrast the Module 13 monthly 99.9% budget.

99.99% is ~**52 minutes/year** (TRUST.md architecture goal). That **fits** a replaced task and a **short AZ blip** if we are already multi-AZ. It does **not** fit a **90-minute region loss**, a **leaf merchants cannot handshake for a day**, or a **single-AZ RDS**. A 30-minute ALB misconfig plus a 25-minute IAM outage **spends the year**. Module 13 still operates **99.9%** (~**43 minutes / 30-day month**) on the same SLI — that is a *monthly* ops budget, not this yearly design target. Do not relabel the Grafana tile.

**Multi-AZ single-region sketch (4–6 sentences):** ALB, tasks, paper datastore, port, health path. Why this **is** allowed to be the 99.99% design.

Merchants enter HTTPS at **`payments.apps.baypay.example`**. TLS terminates at a **multi-AZ ALB** in `us-west-2`; tasks listen on **`8080`**. ECS/Fargate `desired_count` ≥ 2 with tasks in **at least two AZs**. Health: `/actuator/health/liveness` and `/actuator/health/readiness` on **8080**. Datastore is **paper multi-AZ** Postgres (Hikari `jdbc/baypay`) — described, never applied. Secrets Manager + KMS `alias/baypay-payments`; task role ≠ execution role. This **is** the 99.99% design: four nines is in-region failure domains, not a second-region apply. Kubernetes/OpenShift remain valid homes if Pods and Ingress span AZs (ARCHITECT-1102).

**Why “just add a region” is not the only answer:**

`us-east-1` is **DR** (RTO/RPO — TRUST.md starts authorize at **60 minutes** regional). Adding a region buys geography and split-brain cost; it does not fix a forgotten leaf, a single-AZ writer, or `desired_count = 1`. 99.99% ≠ automatic multi-region. Point this lab at AEJE-D-064; point DR-1403 at “the region is gone.”

**Operated SLO:** still 99.9%? If you would change it, who signs and what is the new monthly budget?

**Still 99.9%.** OBSERVABILITY.md stays locked. A 99.99% *operated* SLO is ~**4 minutes/month** — Priya would page on that burn. Who would sign: Priya Nair (SRE) + Finance, in writing, after the design is actually multi-AZ and identity/TLS is paged. We will **not** change it in this 90-minute paper lab. Architecture goal ≠ dashboard tile.

---

## 3. Refusals (ARCHITECT-1401)

| Refusal | Your sentence |
|---|---|
| No NAT / EKS / multi-AZ RDS apply | COST-1105 already priced NAT; EKS is a home (ARCHITECT-1102), not this quarter’s apply; multi-AZ RDS is **paper** — a 90-minute `apply` is a lab failure, not honesty. |
| No ACM / Route 53 apply to “prove” TLS | Teaching host and 90-day leaf live on TRUST.md; requesting ACM or changing Route 53 does not prove the handshake and is out of scope. |
| No `PaymentCluster` / `dmgr-east` as HA | Two Liberty members in `BayPayCell` are the **source estate** (Module 6 decommission). Failover to `dmgr-east` is a finding, not a strategy. ND-in-Docker is not HA. |
| No second-region apply as the 99.99% answer | `us-east-1` is named for DR-1403 only. “Just add a region” does not survive a dead leaf or a single-AZ datastore. |

---

## 4. Incident inset (INCIDENT-1402)

Cite AEJE-D-065. Use **your** INC-SEC-1402 worksheet words. Do not paste `solutions/INCIDENT-1402/`. Quote pack evidence only.

| Field | Your answer |
|---|---|
| Symptom (merchant HTTPS + task status) | Harbor Market curl **60** on `:443`; Avery `c1402b22-…-111402` never left the browser. Tasks **RUNNING 2/2**; jump-box `:8080` liveness **200**. |
| Gate 1 quote (handshake / dates) | `verify error:num=10:certificate has expired`; `notAfter=Sep 1 00:00:00 2026 GMT`; `notBefore=Jun 3`. TCP completed — not an SG drop. |
| Gate 2 quote (ACM status — not a lucky title) | Domain `payments.apps.baypay.example`: **EXPIRED** (`e1402a11-…`, **InUse true**) + **PENDING_VALIDATION** (`p1402b22-…`, InUse false). **No ISSUED.** Validation CNAME `_2f91d4c0.payments…` → `_7c3a1e9f4d2b.acm-validations.aws.` |
| Gate 3 quote (Route 53 names present or not) | Merchant **A ALIAS** to `pay-alb-prod-1402…` **present**. `_health.payments` TXT present. **`_2f91d4c0.payments…` CNAME NXDOMAIN.** No other `_*.payments` CNAMEs. |
| What you ruled out (and which gate) | Postgres / SG (gate 1: TCP + verify fail; Actuator 200). “Just expired” without ACM status (gate 2). Missing merchant ALIAS (gate 3: ALIAS still there). Cluster Secret / INC-K8S-1005 (omitted; this is edge ACM). |
| Stabilize (restore HTTPS — your words) | Restore the validation CNAME; wait **ISSUED**; attach `p1402b22-…` on ALB `:443`. No last-valid ISSUED to swap. |
| Remediate (alerts, records as code — your words) | Validation CNAMEs in Terraform; ACM inventory before deleting “unused” names. TRUST.md: **ticket ≤30d, page ≤7d** — none fired. |
| What you did **not** do (TLS off, DB bounce, `dmgr-east`) | Did **not** disable TLS, bounce Postgres/`dmgr-east`, “fix” a security group, scale tasks, or apply `us-east-1`. |

---

## 5. Threat model (SECURITY-1404)

Cite AEJE-D-067. STRIDE or a named equivalent. Architecture notes only.

**In scope (your words):**

`POST/GET /api/v1/payments`, `POST/GET /api/v1/refunds`, `Idempotency-Key`, frozen account `…222`, IAM/secrets (`alias/baypay-payments`, task ≠ execution), edge TLS on `payments.apps.baypay.example` (`us-west-2`), and the **modular monolith boundary**. People: Avery Chen (`…1111`, active `…221`), Riley / Priya / Sam / Jordan. Teaching payment `c1402b22-0000-4000-8000-111111111402`. Method: **STRIDE**.

**Out of scope (your words):**

Real card-network certification, an employer’s PCI ROC, attacking a live account, exploit PoCs / payloads, PAN storage, scanners against prod, `PaymentCluster` / IHS as the edge, KMS/ACM/RDS/`us-east-1` apply.

| Surface | Threat (architecture language) | Control | Gap / ticket |
|---|---|---|---|
| `POST /api/v1/payments` | **T/R/D:** forged or repudiated authorize; flood that burns the 99.9% budget | TLS at ALB; `Idempotency-Key` required; accounts module must decline frozen `…222`; no PAN persist; JSON logs + `traceparent` (not metric labels) | Ticket: authorize must call `Account.canOriginate()` — not a controller-only `if`. DoS pages on SLO burn / Hikari pending, not CPU>80%. |
| `GET /api/v1/payments` | **I/S:** disclose another merchant’s payment (`c1402b22-…1402`) | Authn to customer/account; return only Avery’s ids; no PAN in row | Ticket: object-level check on `paymentId` (not “any authenticated GET”). Do not put `customerId` on Prometheus labels. |
| `POST/GET /api/v1/refunds` | **E/T:** refund that skips frozen or invents a payment | Same accounts + idempotency store; refund ties to an existing payment; required `Idempotency-Key` (409 on body mismatch) | Ticket: refunds ↛ “internal authorize.” Partial refund still hits `…222`. Leaky refund profile is a lab, not a prod skip. |
| `Idempotency-Key` | **S/T:** same key used as a **second charge** or a confused refund | Store key + body hash; same key/same body → original resource; same key/different body → **409**; TLS in transit | Ticket: store must be **shared** across payments and refunds modules (and paper DR replica). Key is not a secret and **not** a metric label. |
| Frozen account `…222` | **E:** an “internal” path authorizes or refunds `…222` | `AccountStatus.FROZEN` fail-closed; `canOriginate()` only ACTIVE (`…221` may pay) | Ticket: every module that moves money calls **accounts**, not a local copy of status. Riley cannot skip “because the refund is in a hurry.” |
| Secrets / IAM | **I/E:** JVM inherits `GetSecretValue` / `kms:*` / `AdministratorAccess` | **Task role ≠ execution role.** Execution: pull, logs, `valueFrom` + `kms:Decrypt` on `alias/baypay-payments`. Task: near-empty for JDBC. No `changeme`, no keys in git/image | Ticket: reject task=`AdministratorAccess` or copied execution ARN (SECURITY-1103). Grep: no password strings next to `BAYPAY_DB_PASSWORD` in task JSON. |
| Edge TLS | **S/T:** merchants talk HTTP or a stale leaf; jump-box `:8080` treated as “up” | HTTPS `payments.apps.baypay.example`; TLS terminates at ALB; 90-day leaf; **ticket ≤30d, page ≤7d** | Ticket: expiry page (TRUST.md) — not a calendar. HTTP `:8080` is not a customer control. DNS validation records are inventory, not “unused.” |
| Modular monolith boundary | **E:** one deployable used as a license to skip checks | Payments → accounts + idempotency; refunds → accounts + idempotency; one JVM, **several** trust checks | Ticket: no raw SQL that bypasses frozen; no “internal authorize” from refunds; not `PaymentCluster` as the model. Extracting refunds later buys a **new network** boundary — do not pretend the monolith has none. |

**Idempotency paragraph** (same key / same body; same key / different body; Avery retry; captured key as a **control** problem — no replay recipe):

`Idempotency-Key` is both a **safety control** and a **surface**. Same key + same body (Avery retries `c1402b22-…1402` after a timeout) must return the **original** payment or refund — not a second capture. Same key + different body is a **conflict (409)**, not a new authorize. A key that leaks is a **control** problem: TLS + short retention + the store binding key→hash; we do not write how to reuse it. Across a regional cut (DR-1403) the **same store semantics** must exist on the replica. Never put the key on a Micrometer label (INCIDENT-1301 class).

**Frozen account paragraph** (who enforces `…222`; what “internal” must not skip):

**Accounts module** owns `AccountStatus`. Only **ACTIVE** (`…221`) may originate. `…222` is **FROZEN** — a decline, not a missing customer. Payments **and** refunds must call that check; a controller `if` or an “internal” refund that skips it is **elevation**. Teaching id `c1402b22-…1402` is Avery’s happy-path id on `…221` — it does not license `…222`. One deployable is not a skip.

**IAM / secrets** (execution vs task; `alias/baypay-payments`; what you grepped for):

Execution role: image pull, logs, inject `BAYPAY_DB_*` from Secrets Manager, `kms:Decrypt` on **`alias/baypay-payments`**. Task role: JVM — **near-empty** for JDBC; must not be the execution ARN and must not be `AdministratorAccess`. A compromised process inherits the **task** role only. Grep (paper): no `changeme`, no access keys in the container, no password literal in task-def JSON. I did not apply KMS.

**Modular monolith** — what payments and refunds may call, and what they must not assume:

Payments **may** call accounts (frozen) and the idempotency store, then persist ledger intent (no PAN). Refunds **may** call the same two and a **existing** payment. Neither may assume “same JAR = trusted”: no raw SQL around `canOriginate()`, no internal authorize, no skipping `Idempotency-Key`. Observability stays coarse labels. Edge remains the ALB, not `PaymentCluster`.

---

## 6. Interview snippet (Staff, 6–8 sentences)

99.99% is ~52 minutes/year and can be **multi-AZ single-region `us-west-2`** — not `PaymentCluster`, not “add `us-east-1`.” Region loss is DR-1403. Identity/TLS: Avery must handshake `payments.apps.baypay.example`; jump-box `:8080` is not the customer path (INC-SEC-1402: EXPIRED + PENDING_VALIDATION / NXDOMAIN CNAME). STRIDE (AEJE-D-067): `Idempotency-Key` is a control **and** a surface — same key/same body replays; same key/different body **409**; never a second capture for `c1402b22-…1402`. Frozen `…222` is fail-closed in the **accounts** module; refunds and “internal” calls do not skip it. Task role ≠ execution role; `alias/baypay-payments`; no `AdministratorAccess`. One JVM, several trust checks. No scanner-on-prod, no payloads, no PCI ROC. Module 13 SLO stays **99.9%**.

---

## Honesty

- [x] I did not open `solutions/ARCHITECT-1401/`, `solutions/INCIDENT-1402/`, or `solutions/SECURITY-1404/` before attempting the work
- [x] I requested INC-SEC-1402 evidence in the documented gate order
- [x] Every AWS/TLS claim has a source (TRUST.md, OBSERVABILITY.md, or a pack file)
- [x] I did not paste an instructor RCA
- [x] I did not put an access key, private key, or live password in this file
- [x] I did not write exploit steps or payloads
- [x] I did not apply ACM, Route 53, NAT, EKS, RDS, or `us-east-1`
- [x] I did not treat `PaymentCluster` as HA or as the threat-model edge
