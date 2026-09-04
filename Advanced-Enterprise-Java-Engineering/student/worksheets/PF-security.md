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
| Date | |
| Path (files only — required) | |
| Region (must be `us-west-2` for the HA design) | |
| Paper DR region (name only; do not apply) | |
| Reference commit or branch | |

---

## 2. 99.99% failure domains (ARCHITECT-1401)

Cite AEJE-D-064. Teaching host `payments.apps.baypay.example`. Architecture goal **99.99%** (~52 minutes/year). Module 13 operated SLO stays **99.9%** unless you write an explicit contract change.

| Domain | What fails | Merchant symptom | Survives multi-AZ single-region? | What still kills the year |
|---|---|---|---|---|
| Task | | | | |
| AZ | | | | |
| ALB / edge | | | | |
| Identity / TLS | | | | |
| Datastore | | | | |
| Region | | | | |

**Fifty-two minutes (one paragraph):** what fits, what does not. Contrast the Module 13 monthly 99.9% budget.

**Multi-AZ single-region sketch (4–6 sentences):** ALB, tasks, paper datastore, port, health path. Why this **is** allowed to be the 99.99% design.

**Why “just add a region” is not the only answer:**

**Operated SLO:** still 99.9%? If you would change it, who signs and what is the new monthly budget?

---

## 3. Refusals (ARCHITECT-1401)

| Refusal | Your sentence |
|---|---|
| No NAT / EKS / multi-AZ RDS apply | |
| No ACM / Route 53 apply to “prove” TLS | |
| No `PaymentCluster` / `dmgr-east` as HA | |
| No second-region apply as the 99.99% answer | |

---

## 4. Incident inset (INCIDENT-1402)

Cite AEJE-D-065. Use **your** INC-SEC-1402 worksheet words. Do not paste `solutions/INCIDENT-1402/`. Quote pack evidence only.

| Field | Your answer |
|---|---|
| Symptom (merchant HTTPS + task status) | |
| Gate 1 quote (handshake / dates) | |
| Gate 2 quote (ACM status — not a lucky title) | |
| Gate 3 quote (Route 53 names present or not) | |
| What you ruled out (and which gate) | |
| Stabilize (restore HTTPS — your words) | |
| Remediate (alerts, records as code — your words) | |
| What you did **not** do (TLS off, DB bounce, `dmgr-east`) | |

---

## 5. Threat model (SECURITY-1404)

Cite AEJE-D-067. STRIDE or a named equivalent. Architecture notes only.

**In scope (your words):**

**Out of scope (your words):**

| Surface | Threat (architecture language) | Control | Gap / ticket |
|---|---|---|---|
| `POST /api/v1/payments` | | | |
| `GET /api/v1/payments` | | | |
| `POST/GET /api/v1/refunds` | | | |
| `Idempotency-Key` | | | |
| Frozen account `…222` | | | |
| Secrets / IAM | | | |
| Edge TLS | | | |
| Modular monolith boundary | | | |

**Idempotency paragraph** (same key / same body; same key / different body; Avery retry; captured key as a **control** problem — no replay recipe):

**Frozen account paragraph** (who enforces `…222`; what “internal” must not skip):

**IAM / secrets** (execution vs task; `alias/baypay-payments`; what you grepped for):

**Modular monolith** — what payments and refunds may call, and what they must not assume:

---

## 6. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, and Riley Okonkwo, in one sitting, why 99.99% can be multi-AZ single-region, why identity/TLS is a failure domain, how frozen `…222` and `Idempotency-Key` sit on the authorize path, and why Avery Chen’s POST must complete a handshake on `payments.apps.baypay.example` — not only HTTP to `:8080`.

---

## Honesty

- [ ] I did not open `solutions/ARCHITECT-1401/`, `solutions/INCIDENT-1402/`, or `solutions/SECURITY-1404/` before attempting the work
- [ ] I requested INC-SEC-1402 evidence in the documented gate order
- [ ] Every AWS/TLS claim has a source (TRUST.md, OBSERVABILITY.md, or a pack file)
- [ ] I did not paste an instructor RCA
- [ ] I did not put an access key, private key, or live password in this file
- [ ] I did not write exploit steps or payloads
- [ ] I did not apply ACM, Route 53, NAT, EKS, RDS, or `us-east-1`
- [ ] I did not treat `PaymentCluster` as HA or as the threat-model edge
