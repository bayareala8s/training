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
| Date | 2026-09-07 |
| Path (`files only` / optional extra-credit Bedrock / other) | **files only** — `labs/AI-1501/work/output.json` (JSON parse ok). No Bedrock. |
| Region if AWS was sketched (must be `us-west-2`) | **`us-west-2`** (named only) |
| Demo customer (Avery Chen `11111111-1111-1111-1111-111111111111`, account `…221`) | Avery Chen `…1111` / active `…221` |
| Example payment you cited (`c1501d33-…` / `c1502e44-…` / `c1504f55-…`) | AI-1501 `c1501d33-…1501`; AI-1502/03 `c1502e44-…1502`; AI-1504 **`c1504f55-0000-4000-8000-111111111504`** |
| Reference commit or branch | Downloads workspace; class fixture left mixed; `solutions/AI-1501/` not opened |

---

## 2. Four-bucket rewrite (AI-1501–1503)

Cite **AEJE-D-068**. Use **your** `output.json` words. Do not paste `solutions/AI-150N/`.

### AI-1501 — mixed summary → contract

| Field | Your answer |
|---|---|
| Evidence quotes (rate, P99, 5xx, Hikari pending — file + text) | `labs/AI-1501/starter/evidence-excerpt.txt`: rate **182 → 22 RPS**; P99 **118 ms → 4.82 s**; 5xx **~0.03–0.07**; Hikari pending **0**; servlet **187/200**. Avery `c1501d33-…1501` **201 in 5.14 s**. Excerpt: no database metrics file. |
| Hypotheses (ids + `unproven` / `weakened` / `withdrawn`) | **H1 withdrawn** (writer down). **H2 unproven** (3.9.0 / BAYPAY-13011 holding threads). **H3 unproven** (JVM saturation / scrape candidate). None `proven`. |
| What you withdrew (e.g. “the database is down”) and why | H1. Hikari pending **0**; Riley said do not bounce db-east; excerpt lists **no** DB metrics / RDS event. `invented/db-down.txt` was never opened. |
| Recommended investigation | Next omitted kind: **scrape duration / series count / JVM**. Confirm last healthy **3.8.4**. Not a bounce. |
| Suggested remediation (`approvalRequired` must be true) | After scrape/JVM, roll to **3.8.4** if the timeline still holds. `approvalRequired: true`. No Postgres / `dmgr-east` bounce. |
| `humanApproval` status / who would sign | **`pending`**. BayOps-auto is not a human. Riley / Priya / on-call would sign a mutate. |

### AI-1502 — ranked hypotheses

| Field | Your answer |
|---|---|
| HTTPS / RUNNING / `:8080` quotes | `labs/AI-1502/starter/evidence-excerpt.txt`: `verify error:num=10:certificate has expired`; `notAfter=Sep 1 2026`; curl **(60)**; Avery `c1502e44-…1502` stayed in the browser. Tasks **RUNNING 2/2**. Jump-box `:8080` liveness **200**. |
| Ranked hypotheses (none `proven`) | **H1 unproven** — edge/leaf/handshake on `:443`. **H2 withdrawn** — app-down (RUNNING + 200). **H3 withdrawn** — `dmgr-east` / cell bounce (no cell dump; not on HTTPS). **H4 withdrawn** — Postgres (no metrics; handshake never reached Spring). |
| Next investigation (cert / ACM / DNS **class** — your words) | Paper **ACM describe** (status / InUse / validation) and **Route 53 list** for the payments host. Not opened yet. No `request-certificate`. Sam’s DNS-cleanup rumor stays a rumor. |
| What you refused to bounce | **`dmgr-east` / `PaymentCluster`**, Postgres. Did not disable TLS. |

### AI-1503 — approval-aware runbook

| Field | Your answer |
|---|---|
| Unsafe starter moves you refused (TLS-off, `dmgr-east`, Postgres, auto-approve) | Disable TLS on the ALB; bounce `dmgr-east` / `PaymentCluster`; bounce Postgres; `approvalRequired: false`; `humanApproval` = **BayOps-auto**. |
| Cert / edge check you put first | Non-mutating: describe the leaf on `:443` (`notAfter`, CN), confirm what the listener presents, then decide ACM describe / Route 53 list. |
| Who must sign before a mutate | **Riley Okonkwo** or **Priya Nair** (named). I recorded **`rejected`** of the unsafe starter (`by`: Riley, `2026-09-02T07:25:00Z`). Restore-HTTPS stays unsigned until after describe. |

Evidence may quote only opened files — Morgan’s `invented/db-down.txt` and `provenRootCause` string are contract fails. Hypotheses stay `unproven` / `weakened` / `withdrawn`. Investigation is the **next** omitted kind, not a bounce. Every mutate has `approvalRequired: true`. Auto-approve is a fail even if the action happens to be safe: BayOps-auto is not Riley or Priya. AI-1503: cert/edge **describe first**; refuse TLS-off, `dmgr-east`, and Postgres theater. Restore HTTPS is the stabilize — HTTP on the listener is a second incident.

---

## 3. Which AI-1504 claims were fabricated (your words + quotes)

Cite **AEJE-D-070**. Copy **your** INC-AI-1504 worksheet words. Do not paste `solutions/AI-1504/`.

The planted dump is [infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json](../../infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json). Quote it. Then quote the pack file that contradicts it.

| Fabricated claim | Quote from the planted JSON | Pack quote that contradicts it | Your sentence |
|---|---|---|---|
| Invented file `evidence/db-failover.json` | `"source": "evidence/db-failover.json"` — “Writer endpoint moved. This is the proven root cause.” | `pack-inventory.txt`: **“evidence/db-failover.json — NOT IN THIS PACK.”** Priya: “that path does not exist here.” | A missing `source` is a **hallucination**. I did not create the file. |
| Proven RCA: Postgres Multi-AZ writer failover in us-west-2 at 14:02 | `"provenRootCause": "Postgres Multi-AZ writer failover in us-west-2 at 14:02"`; H1 `status`: `proven` | `ecs-tasks.txt`: RUNNING since **18:40Z**, `stopCode` null, no stop at 14:02. Inventory: **no** database metrics / RDS event. | Fluent `provenRootCause` still fails the contract. |
| Bounce `dmgr-east` / recycle PaymentCluster | `"Bounce dmgr-east and recycle PaymentCluster"`; `approvalRequired: false` | `ecs-tasks.txt`: “dmgr-east / PaymentCluster **do not appear**.” Timeline BAYPAY-15041: leftover cell out of HTTPS path. | An agent must never auto-bounce leftover ND. |
| Auto-approved (`BayOps-auto`) | `"status": "approved", "by": "BayOps-auto", "note": "auto-approved"` | Riley (inventory): “humanApproval stays **rejected** until a named human reads the files we actually shipped.” | BayOps-auto is not a human. |

| Field | Your answer |
|---|---|
| Tasks `lastStatus` quote | **`RUNNING`** 2/2 (`t1504a` / `t1504b`). `startedAt` 18:40Z. Image **3.8.4**. |
| ALB 502/503 or target-health quote | Merchant **`HTTP/1.1 503`** (`Server: awselb/2.0`). Clients also **502**. TargetHealth **`unhealthy`** / `Target.FailedHealthChecks` on **8080**. **Healthy host count: 0.** |
| Inventory line that database metrics / `db-failover.json` are omitted | “**evidence/db-failover.json — NOT IN THIS PACK.**” “Database metrics — no writer CPU, no RDS events, no Multi-AZ failover paste.” |

A row that only says “the AI is wrong” without the missing-file quote and the proven-RCA quote is incomplete.

---

## 4. Approval decision (AI-1504)

| Field | Your answer |
|---|---|
| Planted `humanApproval` (what it said) | **`approved`** by **`BayOps-auto`** at 21:12Z, note `"auto-approved"` |
| Your `humanApproval.status` (must be `rejected` for the planted runbook) | **`rejected`** |
| By (Riley Okonkwo / Priya Nair / your name) | **Riley Okonkwo** |
| At (timestamp) | **2026-09-03T21:15:00Z** |
| Note (cite the missing file) | Citation **`evidence/db-failover.json` is NOT IN THIS PACK**. `provenRootCause` “Postgres Multi-AZ writer failover in us-west-2 at 14:02” fails the contract. |
| What you will not do (Postgres bounce, `dmgr-east`, TLS-off) | No Postgres bounce, no `dmgr-east` / PaymentCluster bounce, no TLS-off, no invented `db-failover.json`. |

---

## 5. Interview snippet (Staff, 6–8 sentences)

BayOps is an investigator, not the authority. Four buckets plus `humanApproval` (AEJE-D-070). A missing `source` is a **hallucination**: planted dump cited **`evidence/db-failover.json`** — inventory says **NOT IN THIS PACK**. `provenRootCause` “Postgres Multi-AZ writer failover in us-west-2 at 14:02” is a contract fail even when fluent. Tasks **RUNNING** since 18:40Z while merchants get **503/502** and TG **healthy=0** — ECS up ≠ healthy target. Leftover `dmgr-east` must never auto-bounce; I **rejected** the planted runbook (Riley, 21:15Z). Avery `c1504f55-…1504` is a 503, not a domain decline. No Bedrock; `ls` of the pack is enough.

---

## Honesty

- [x] I did not open `solutions/AI-1501/`, `solutions/AI-1502/`, `solutions/AI-1503/`, or `solutions/AI-1504/` before attempting the work
- [x] I quoted `evidence/db-failover.json` as **missing** and I quoted the planted **proven-RCA** field
- [x] Every evidence claim has a source (BAYOPS.md, an excerpt, or a pack file I opened)
- [x] I did not paste instructor solution text
- [x] I did not put PAN, an access key, a private key, or a live password in this file
- [x] I did not create `db-failover.json` to match the model
- [x] I did not bounce Postgres or `dmgr-east` and I did not disable TLS
- [x] I did not require Amazon Bedrock, NAT, EKS, or OpenSearch to pass these labs
- [x] If I invoked extra-credit Bedrock, I say so above and I destroy tagged `us-west-2` leftovers the same day
