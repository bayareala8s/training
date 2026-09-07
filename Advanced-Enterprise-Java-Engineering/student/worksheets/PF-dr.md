# Portfolio worksheet — DR strategy

**Artifact:** Module 14 / [DR-1403](../../labs/DR-1403/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagram:** AEJE-D-066 (Regional DR, RTO and RPO)  
**Trust notes:** [datasets/baypay-security/TRUST.md](../../datasets/baypay-security/TRUST.md)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste instructor solutions. Do not put access keys or `BAYPAY_DB_PASSWORD` values in this file. This is a **paper tabletop**. Do not apply `us-east-1`.

The Module 14 portfolio artifact is this page (**DR strategy**) plus [PF-security.md](PF-security.md) (**security model + 99.99% HA**). Do not collapse four nines into this sheet — that design lives on PF-security.md.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | 2026-09-07 |
| Path (files only — required) | **files only** — PF-dr.md tabletop. No `us-east-1` / Route 53 / RDS apply. |
| Primary region (gone) | **`us-west-2`** |
| Paper secondary (must be `us-east-1`; do not apply) | **`us-east-1`** (named only) |
| Reference commit or branch | Downloads workspace; `solutions/DR-1403/` not opened |

---

## 2. Tabletop declaration (DR-1403)

Cite AEJE-D-066. One paragraph: `us-west-2` is unreachable (ALB, tasks, teaching datastore). Avery Chen (`11111111-1111-1111-1111-111111111111`, account `…221`) will retry. You are not applying anything.

Priya Nair’s tabletop: **`us-west-2` is gone.** The regional ALB, `payment-service` Fargate tasks, ACM leaf, and teaching Postgres in that region are unreachable. Harbor Market still POSTs as Avery Chen (`11111111-…-1111`, active USD `…221`). In-flight payment **`c1402b22-0000-4000-8000-111111111402`** may retry with the **same `Idempotency-Key`**. This is **RTO/RPO**, not an AZ blip and not a four-nines slogan. We are **not** applying a stack in `us-east-1`, not flipping Route 53 on hope, and not failing over to `dmgr-east`.

---

## 3. RTO / RPO

Start from TRUST.md. If you change a number, write the business justification in the same cell.

| Workload | RPO | RTO | Pattern | Justification (or “TRUST.md default”) |
|---|---|---|---|---|
| Payment authorize / complete | **Seconds** (idempotent retry + replicated ledger intent) | **60 minutes** regional | **Pilot light** in paper `us-east-1` | **TRUST.md default.** Chargeback / double-authorize is worse than a late 201. 60 minutes is a *human declare + scale-out* hour, not “DNS in 30 seconds.” |
| Merchant reporting | **24 hours** | **24 hours** | **Backup restore** | **TRUST.md default.** Last night’s snapshot is an allowed conversation. Do not restore authorize from the reporting dump and call it seconds. |
| Leftover `BayPayCell` / `dmgr-east` | **Not a DR target** | **Do not fail over to ND** | **Decommission (Module 6)** | **TRUST.md default.** Undefined RPO/RTO. `PaymentCluster` is the source estate, not a bunker. |

Teaching payment id you must address: `c1402b22-0000-4000-8000-111111111402`.

---

## 4. Pattern pick (payments)

Circle one and defend it: **pilot light** · **warm standby** · **backup-restore**

**Why this pattern matches your payments RTO:**

**Pilot light.** Ledger intent and a minimal control plane already exist (on paper) in `us-east-1`; we scale Fargate + attach a paper ALB after Priya **declares**. That can hit **60 minutes** if the image is already in secondary ECR and KMS can decrypt. We do not pay a second full idle stack every day this quarter (COST-1105 literacy). Scale-out time is *inside* the hour — so the runbook must not start with a DNS flip.

**Why the other two lost this quarter:**

**Warm standby** would buy a faster RTO (stack already running, scaled down) but Finance is not funding a second ALB + Fargate + replica datastore while `us-west-2` is healthy — and **applying** that bill in a 90-minute lab is a failure. **Backup-restore** is hours: it **misses** the 60-minute payments RTO and the seconds RPO. Active-active was considered and rejected (below).

**What reporting uses (may differ):**

**Backup-restore**, 24h / 24h. Same snapshot window is fine for Harbor Market settlement reports. It is **not** the authorize RPO.

**Active-active (if you considered it — what new failure domain?):**

**Split-brain / dual authorize.** Two regions accepting `POST /api/v1/payments` without a shared idempotency + ledger intent means Avery can capture **twice** for `c1402b22-…1402`. That is a new failure domain, not extra credit. Not the teaching default.

---

## 5. Data and idempotency

| Field | Your answer |
|---|---|
| What is replicated or backed up (not PAN) | **Ledger intent** (payment id, outcome, amount, currency, `Idempotency-Key`, account id). Tokenize or **never persist PAN**. Reporting warehouse dumps are a **different** backup. |
| What happens on Avery’s `Idempotency-Key` retry after the cut | Same key + same body → return the **already COMPLETED** (or in-flight) intent from the replica. Same key + different body → **conflict**, do not capture a second time. |
| What must not double-authorize for `c1402b22-…1402` | A second `201` that posts a **second** ledger row / capture. The replica must answer `existsByIdempotencyKey` for that payment. If the replica is **minutes** behind, we have already **missed seconds RPO** — say so; do not pretend backup-restore is seconds. |
| Secret / KMS plan (paper only; teaching alias) | Teaching alias stays **`alias/baypay-payments`**. Plan a **replica key / multi-Region grant** in `us-east-1` so the restore can decrypt. Do **not** create a second alias or apply KMS in lab. Secrets still Secrets Manager; task role ≠ execution role; no `AdministratorAccess` “because DR.” |

In 4–6 sentences, explain the ledger-intent story without storing PAN.

Authorize writes **intent** (who, which account `…221` or frozen `…222`, amount, `Idempotency-Key`, payment id `c1402b22-…1402`) — not PAN. That intent is what we replicate to paper `us-east-1` so RPO stays **seconds**. After the cut, Avery’s client retries; the secondary must see the **same key** and not post a second capture. Reporting’s 22:00 UTC dump can be a day stale and still meet 24h RPO; restoring payments from that dump is how you miss seconds and double-charge. Frozen `…222` still denies on the secondary — “internal because DR” must not skip it.

---

## 6. Do-not-fail-over list

| Item | Your sentence |
|---|---|
| `BayPayCell` / `dmgr-east` / `PaymentCluster` | Leftover ND is the **source estate** (Module 6). No teaching RPO/RTO. Morgan starting the cell is a finding, not a strategy. |
| Student `apply` in `us-east-1` | Paper secondary only. A 90-minute apply is a **lab failure**, not a measured RTO. |
| NAT / EKS / RDS apply “to rehearse” | Same refusals as ARCHITECT-1401 / COST-1105. Do not stand up a second platform as the DR story. |
| Disable TLS “because DR” | Merchants still enter **HTTPS** on `payments.apps.baypay.example`. HTTP on the listener is a second incident (INCIDENT-1402 class). |
| Flip Route 53 on hope | Jordan does **not** cut DNS until Priya has declared, east can decrypt, tasks are healthy on **8080**, and idempotency answers for `c1402b22-…1402`. TTL sits inside the 60-minute RTO. |

---

## 7. First 60 minutes

Numbered paper runbook. Name Priya Nair, Riley Okonkwo, Sam Okada, Jordan Voss by role.

1. **Priya Nair (SRE)** declares SEV / “region gone” — `us-west-2` ALB, tasks, and teaching datastore unreachable. Clock starts on the **60-minute** payments RTO. Reporting stays on the **24-hour** clock.
2. **Riley Okonkwo (on-call)** tells merchant success: Harbor Market retries are expected; same `Idempotency-Key` for Avery / `c1402b22-…1402`; we are **not** bouncing `dmgr-east` or Postgres in a dead region.
3. **Sam Okada (platform)** scales the **paper** pilot light in `us-east-1` (image already in secondary ECR, task ≠ execution role). Confirms KMS replica can decrypt `alias/baypay-payments`. **Does not apply** NAT / EKS / RDS / a live stack.
4. **Verify before DNS** (Riley + Sam): secondary tasks **RUNNING**, `/actuator/health/liveness` + `/actuator/health/readiness` on **8080**, ledger replica answers idempotency for in-flight keys, edge TLS plan is still HTTPS (no listener-to-HTTP).
5. **Jordan Voss (release)** moves the **paper** failover record for `payments.apps.baypay.example` **only after** step 4. No second tag, no “flip now,” no `AdministratorAccess`.

What you verify before anyone talks about DNS:

Secondary capacity actually serves authorize (health on 8080), **decrypt works**, and **`Idempotency-Key` for `c1402b22-…1402` does not double-capture**. An empty east ALB plus a flipped name is a self-inflicted outage.

---

## 8. 99.99% versus this page

One paragraph: ARCHITECT-1401 is in-region failure domains (~52 minutes/year). This page is “the region is gone.” Module 13 SLO stays 99.9% unless you already changed it on PF-security.md.

ARCHITECT-1401 / AEJE-D-064 is **in-region** four nines (~**52 minutes/year**): task, AZ, ALB, identity/TLS, paper multi-AZ datastore — still **`us-west-2`**. A 60-minute **region** loss **spends that year**; that is why this page exists, not why we “add a region to buy 99.99%.” Multi-AZ single-region remains a valid HA design. This tabletop (AEJE-D-066) is RTO/RPO when that region is the domain that failed. Module 13 operated SLO stays **99.9%** (~43 minutes/month) on PF-ops / PF-security — we did **not** change the contract.

---

## 9. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, Jordan Voss, and Riley Okonkwo, in one sitting, why payments and reporting buy different patterns, why `dmgr-east` is not a bunker, how idempotency saves Avery from a double charge, and why you will not apply `us-east-1` in a 90-minute lab.

Payments buy **pilot light** in paper `us-east-1`: RPO **seconds**, RTO **60 minutes**, replicated **ledger intent** (not PAN). Reporting stays **backup-restore 24h/24h** — last night’s dump is allowed; it is not the authorize RPO. Warm standby lost this quarter on idle bill; backup-restore misses the payments hour; active-active buys **split-brain**. `dmgr-east` / `PaymentCluster` have **no** RPO/RTO — decommission, do not fail over. Avery’s same `Idempotency-Key` for `c1402b22-…1402` must return the existing intent so we do not double-capture after the retry storm. Jordan does not flip Route 53 until health, KMS decrypt, and idempotency check. We will **not** apply `us-east-1` in a 90-minute lab; the grade is this page. Four nines stay on PF-security.md.

---

## Honesty

- [x] I did not open `solutions/DR-1403/` before attempting this sheet
- [x] Every RTO/RPO claim has a source (TRUST.md or my written justification)
- [x] I did not paste an instructor solution
- [x] I did not put an access key or a live password in this file
- [x] I did not apply ACM, Route 53, NAT, EKS, RDS, or `us-east-1`
- [x] I did not treat `PaymentCluster` as a DR target
- [x] I did not collapse ARCHITECT-1401 into “just add a region”
