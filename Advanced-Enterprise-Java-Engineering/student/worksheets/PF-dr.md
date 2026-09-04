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
| Date | |
| Path (files only — required) | |
| Primary region (gone) | |
| Paper secondary (must be `us-east-1`; do not apply) | |
| Reference commit or branch | |

---

## 2. Tabletop declaration (DR-1403)

Cite AEJE-D-066. One paragraph: `us-west-2` is unreachable (ALB, tasks, teaching datastore). Avery Chen (`11111111-1111-1111-1111-111111111111`, account `…221`) will retry. You are not applying anything.

---

## 3. RTO / RPO

Start from TRUST.md. If you change a number, write the business justification in the same cell.

| Workload | RPO | RTO | Pattern | Justification (or “TRUST.md default”) |
|---|---|---|---|---|
| Payment authorize / complete | | | | |
| Merchant reporting | | | | |
| Leftover `BayPayCell` / `dmgr-east` | | | | |

Teaching payment id you must address: `c1402b22-0000-4000-8000-111111111402`.

---

## 4. Pattern pick (payments)

Circle one and defend it: **pilot light** · **warm standby** · **backup-restore**

**Why this pattern matches your payments RTO:**

**Why the other two lost this quarter:**

**What reporting uses (may differ):**

**Active-active (if you considered it — what new failure domain?):**

---

## 5. Data and idempotency

| Field | Your answer |
|---|---|
| What is replicated or backed up (not PAN) | |
| What happens on Avery’s `Idempotency-Key` retry after the cut | |
| What must not double-authorize for `c1402b22-…1402` | |
| Secret / KMS plan (paper only; teaching alias) | |

In 4–6 sentences, explain the ledger-intent story without storing PAN.

---

## 6. Do-not-fail-over list

| Item | Your sentence |
|---|---|
| `BayPayCell` / `dmgr-east` / `PaymentCluster` | |
| Student `apply` in `us-east-1` | |
| NAT / EKS / RDS apply “to rehearse” | |
| Disable TLS “because DR” | |
| Flip Route 53 on hope | |

---

## 7. First 60 minutes

Numbered paper runbook. Name Priya Nair, Riley Okonkwo, Sam Okada, Jordan Voss by role.

1.  
2.  
3.  
4.  
5.  

What you verify before anyone talks about DNS:

---

## 8. 99.99% versus this page

One paragraph: ARCHITECT-1401 is in-region failure domains (~52 minutes/year). This page is “the region is gone.” Module 13 SLO stays 99.9% unless you already changed it on PF-security.md.

---

## 9. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, Jordan Voss, and Riley Okonkwo, in one sitting, why payments and reporting buy different patterns, why `dmgr-east` is not a bunker, how idempotency saves Avery from a double charge, and why you will not apply `us-east-1` in a 90-minute lab.

---

## Honesty

- [ ] I did not open `solutions/DR-1403/` before attempting this sheet
- [ ] Every RTO/RPO claim has a source (TRUST.md or my written justification)
- [ ] I did not paste an instructor solution
- [ ] I did not put an access key or a live password in this file
- [ ] I did not apply ACM, Route 53, NAT, EKS, RDS, or `us-east-1`
- [ ] I did not treat `PaymentCluster` as a DR target
- [ ] I did not collapse ARCHITECT-1401 into “just add a region”
