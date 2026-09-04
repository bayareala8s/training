# Portfolio worksheet — Production crisis RCA draft

**Artifact:** CAPSTONE-4 / [capstones/04-production-crisis/README.md](../../capstones/04-production-crisis/README.md) · [INC-CAP-4](../../incidents/production/INC-CAP-4/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-071 (initial WebSphere topology) · AEJE-D-072 (cloud-native target)  
**Ops notes:** [datasets/baypay-ops/OBSERVABILITY.md](../../datasets/baypay-ops/OBSERVABILITY.md)  
**BayOps contract:** [datasets/baypay-ai/BAYOPS.md](../../datasets/baypay-ai/BAYOPS.md)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste instructor solution text. Do not put PAN, CVV, access keys, or `BAYPAY_DB_PASSWORD` values in this file. Live Grafana, Prometheus, AMP, and Bedrock are optional — say whether you used them. The grade path is the gated pack.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | |
| Path (`files only` / other) | |
| Incident pack used (INC-CAP-4) | |
| Region (must be `us-west-2`) | |
| Demo customer (Avery Chen `11111111-1111-1111-1111-111111111111`, account `…221`) | |
| Example payment you cited (`c1404e44-0000-4000-8000-111111111404`) | |
| Reference commit or branch | |

---

## 2. Gate quotes (from *your* INC-CAP-4 worksheet)

Cite AEJE-D-072 as the merchant path. Copy **your** worksheet words. Do not paste `solutions/CAPSTONE-4/`.

| Field | Your answer |
|---|---|
| Gate 1 quote (comms / Harbor Market 503 / payment id) | |
| Gate 2 quote (RED: rate, P99, 5xx/503, Hikari pending) | |
| Gate 3 quote (images / canary fraction / last healthy) | |
| Gate 4 quote (thread state and waiter frames) | |
| Gate 5 quote (dependency in-flight / successes) | |
| What you still treated as unproven after gate 3 | |

---

## 3. Stabilize, remediate, recover

| Field | Your answer |
|---|---|
| Stabilize (what restores the path *now*) | |
| What you did **not** bounce or disable | |
| Remediate (what you will not ship next time) | |
| Recover check (what tiles must heal before you leave the bridge) | |

In 4–6 sentences, explain stabilize versus remediate versus recover for this SEV-1. Name the last healthy image if a file you opened named one.

---

## 4. BayOps reject (four buckets)

Cite BAYOPS.md. Evaluate `evidence/bayops-draft.json`. Do not accept an uncited proven RCA.

| Fabricated claim | Quote from the draft | Pack quote that contradicts it | Your sentence |
|---|---|---|---|
| Invented file `evidence/db-failover.json` | | | |
| Proven RCA: Postgres Multi-AZ failover | | | |
| Bounce `dmgr-east` | | | |
| Auto-approved (`BayOps-auto`) | | | |

| Field | Your answer |
|---|---|
| Evidence bucket (your rewrite) | |
| Hypotheses (ids + `unproven` / `weakened` / `withdrawn`) | |
| Recommended investigation | |
| Suggested remediation (`approvalRequired` must be true) | |
| Your `humanApproval.status` (must be `rejected` for the planted runbook) | |
| By / at / note | |

A row that only says “the AI is wrong” without the missing-file quote and the proven-RCA quote is incomplete.

---

## 5. RCA draft and prevention (your words)

| Field | Your answer |
|---|---|
| RCA draft (files + quotes; no instructor paste) | |
| Prevention (canary policy, client budgets, pipeline, approval) | |
| Why leftover ND (AEJE-D-071) was not a stabilize target | |

---

## 6. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, Jordan Voss, Riley Okonkwo, and Morgan Hale, in one sitting, how you ran this SEV-1: gate order, what you quoted before you stabilized, why Hikari pending ~0 is not a writer outage, why a BayOps proven stamp without a file is a reject, and what you still owe Harbor Market after the canary is gone. Mention Avery Chen’s create (`POST /api/v1/payments`) without putting PAN in the answer.

---

## Honesty

- [ ] I did not open `solutions/CAPSTONE-4/` before attempting the work
- [ ] I requested INC-CAP-4 evidence in the documented gate order
- [ ] Every metric or incident claim has a source (OBSERVABILITY.md, BAYOPS.md, or a pack file I opened)
- [ ] I did not paste an instructor RCA
- [ ] I quoted `evidence/db-failover.json` as **missing** and I quoted the planted **proven-RCA** field
- [ ] I did not put PAN, an access key, or a live password in this file
- [ ] I did not bounce Postgres or `dmgr-east` and I did not disable TLS
- [ ] I did not create `db-failover.json` to match the model
- [ ] I did not apply AWS, AMP, a paid Grafana, or Bedrock to pass this capstone
- [ ] If I invoked extra-credit Bedrock, I say so above and I destroy tagged `us-west-2` leftovers the same day
