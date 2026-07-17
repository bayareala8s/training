# Common Mistakes — Module 07

**Audience:** Students and instructors  
**Case study:** NorthStar Financial Services (fictional)

---

## Concept mistakes

1. **Treating Zero Trust as a product purchase** — Buying tools without redrawing trust boundaries and IAM leaves residual risk unchanged.
2. **Confusing encryption with access control** — SSE-KMS does not fix wildcard `GetObject` on sensitive prefixes.
3. **Copy-paste RTO/RPO** — Applying payment-auth targets to every file store inflates cost and erodes credibility.
4. **STRIDE as a vocabulary quiz** — Listing the six letters without abuse cases, owners, or priorities fails the lab bar.
5. **“Compliant” as a binary badge** — Executives need residual risk, evidence freshness, and exception expiry—not slogans.

---

## Lab mistakes

1. **Skipping Block Public Access** — Even “temporary” public ACLs are unacceptable for Restricted analogues.
2. **Admin-only IAM story** — Using a single power-user role and never modeling least privilege.
3. **Enabling CRR without a restore story** — Replication without promotion/restore steps is incomplete DR.
4. **No recovery drill** — Versioning enabled ≠ recovery proven.
5. **Leaving resources running** — Forgotten buckets with versioning + replication drive surprise cost.
6. **Using production or real PII** — Lab data must be synthetic only.

---

## Leadership mistakes

1. **Fear without options** — Escalating risk without costed control alternatives.
2. **Hiding exceptions** — Informal forever-exceptions become systemic debt.
3. **Over-promising audit readiness** — One lab matrix is a teaching artifact, not a GRC program.

---

## How instructors should intervene

| Signal | Coaching move |
| ------ | ------------- |
| Wildcard IAM | Ask “which abuse case does this enable?” |
| No evidence paths | Require one concrete ARN/path per control |
| Unrealistic RTO | Ask who pays for the pattern that achieves it |
| No cleanup | Block submission credit until cleanup confirmation |
