# Portfolio worksheet — AI-operations evaluation

**Artifact:** Module 15 / [AI-1501](../../labs/AI-1501/README.md) · [AI-1502](../../labs/AI-1502/README.md) · [AI-1503](../../labs/AI-1503/README.md) · [AI-1504](../../labs/AI-1504/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-068 (evidence vs hypothesis) · AEJE-D-069 (BayOps architecture) · AEJE-D-070 (human approval and hallucination detection)  
**Contract:** [datasets/baypay-ai/BAYOPS.md](../../datasets/baypay-ai/BAYOPS.md)  
**Schema:** [infrastructure/bayops-ai/schema/output.schema.json](../../infrastructure/bayops-ai/schema/output.schema.json)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste instructor solution text. Do not put PAN, CVV, access keys, or `BAYPAY_DB_PASSWORD` values in this file. Live Amazon Bedrock is optional extra credit — say whether you used it. The grade path is paper fixtures plus JSON.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | |
| Path (`files only` / optional extra-credit Bedrock / other) | |
| Region if AWS was sketched (must be `us-west-2`) | |
| Demo customer (Avery Chen `11111111-1111-1111-1111-111111111111`, account `…221`) | |
| Example payment you cited (`c1501d33-…` / `c1502e44-…` / `c1504f55-…`) | |
| Reference commit or branch | |

---

## 2. Four-bucket rewrite (AI-1501–1503)

Cite **AEJE-D-068**. Use **your** `output.json` words. Do not paste `solutions/AI-150N/`.

### AI-1501 — mixed summary → contract

| Field | Your answer |
|---|---|
| Evidence quotes (rate, P99, 5xx, Hikari pending — file + text) | |
| Hypotheses (ids + `unproven` / `weakened` / `withdrawn`) | |
| What you withdrew (e.g. “the database is down”) and why | |
| Recommended investigation | |
| Suggested remediation (`approvalRequired` must be true) | |
| `humanApproval` status / who would sign | |

### AI-1502 — ranked hypotheses

| Field | Your answer |
|---|---|
| HTTPS / RUNNING / `:8080` quotes | |
| Ranked hypotheses (none `proven`) | |
| Next investigation (cert / ACM / DNS **class** — your words) | |
| What you refused to bounce | |

### AI-1503 — approval-aware runbook

| Field | Your answer |
|---|---|
| Unsafe starter moves you refused (TLS-off, `dmgr-east`, Postgres, auto-approve) | |
| Cert / edge check you put first | |
| Who must sign before a mutate | |

In 4–6 sentences, explain how the four buckets plus `humanApproval` stop a fluent “proven RCA.”

---

## 3. Which AI-1504 claims were fabricated (your words + quotes)

Cite **AEJE-D-070**. Copy **your** INC-AI-1504 worksheet words. Do not paste `solutions/AI-1504/`.

The planted dump is [infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json](../../infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json). Quote it. Then quote the pack file that contradicts it.

| Fabricated claim | Quote from the planted JSON | Pack quote that contradicts it | Your sentence |
|---|---|---|---|
| Invented file `evidence/db-failover.json` | | | |
| Proven RCA: Postgres Multi-AZ writer failover in us-west-2 at 14:02 | | | |
| Bounce `dmgr-east` / recycle PaymentCluster | | | |
| Auto-approved (`BayOps-auto`) | | | |

| Field | Your answer |
|---|---|
| Tasks `lastStatus` quote | |
| ALB 502/503 or target-health quote | |
| Inventory line that database metrics / `db-failover.json` are omitted | |

A row that only says “the AI is wrong” without the missing-file quote and the proven-RCA quote is incomplete.

---

## 4. Approval decision (AI-1504)

| Field | Your answer |
|---|---|
| Planted `humanApproval` (what it said) | |
| Your `humanApproval.status` (must be `rejected` for the planted runbook) | |
| By (Riley Okonkwo / Priya Nair / your name) | |
| At (timestamp) | |
| Note (cite the missing file) | |
| What you will not do (Postgres bounce, `dmgr-east`, TLS-off) | |

---

## 5. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, Riley Okonkwo, Jordan Voss, and Morgan Hale, in one sitting, why BayOps is an investigator and not the authority: the four buckets, why a missing `source` is a hallucination, why leftover `dmgr-east` must never auto-bounce, and what you quoted from INC-AI-1504 before you rejected approval. Mention Avery Chen’s create (`POST /api/v1/payments`) without putting PAN in the answer.

---

## Honesty

- [ ] I did not open `solutions/AI-1501/`, `solutions/AI-1502/`, `solutions/AI-1503/`, or `solutions/AI-1504/` before attempting the work
- [ ] I quoted `evidence/db-failover.json` as **missing** and I quoted the planted **proven-RCA** field
- [ ] Every evidence claim has a source (BAYOPS.md, an excerpt, or a pack file I opened)
- [ ] I did not paste instructor solution text
- [ ] I did not put PAN, an access key, a private key, or a live password in this file
- [ ] I did not create `db-failover.json` to match the model
- [ ] I did not bounce Postgres or `dmgr-east` and I did not disable TLS
- [ ] I did not require Amazon Bedrock, NAT, EKS, or OpenSearch to pass these labs
- [ ] If I invoked extra-credit Bedrock, I say so above and I destroy tagged `us-west-2` leftovers the same day
