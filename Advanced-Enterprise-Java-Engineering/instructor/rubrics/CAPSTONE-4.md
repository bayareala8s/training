# Rubric — CAPSTONE-4

**Type:** CAPSTONE  
**awsLab:** no (files only)  
**Pack:** INC-CAP-4  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “database,” “just a bad deploy,” or a fluent “FraudClient has no timeout” guess with no quoted **rate / P99 / 503**, no quoted **canary 3.10.0 1/3**, no quoted **WAITING / FraudClient**, no quoted **dependency in-flight / zero successes**, and no **BayOps reject** must **not** max Diagnostic method (20%).

Do **not** walk the room to the instructor RCA in the first 20 minutes. Opening `solutions/CAPSTONE-4/` before the worksheet fails Diagnostic method.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | 3.10.0 canary (BAYPAY-CAP41) added sync `FraudClient` to `https://fraud.baypay.example/v1/score`; **no connect/read timeout**; HTTP workers **WAITING** on `FraudClient.score`; rate **~180→~61** RPS; P99 **~122 ms→~8.6 s**; **503** loud; Hikari pending **0**; Avery `c1404e44-…` | Named the canary or one waiter; one number quoted | “Postgres Multi-AZ,” “cardinality,” “expired cert,” “Path=/,” “9080 debug,” or INC-JVM-804 FX as RCA without contrast |
| Diagnostic method | Gates 1→2→3→4→5; hypothesis before each later file; quotes from comms, RED, deploy, dump, dependency; BayOps evaluated last | Used all files; skipped a hypothesis | Opened solutions or `thread-dump.txt` / `bayops-draft.json` first; accepted planted **proven** stamp |
| Production awareness | Stabilize = **stop canary / roll back `3.8.4`** (or disable fraud flag / add timeouts and shed the canary); **no** Postgres bounce; **no** `dmgr-east`; **no** TLS-off; **no** blind scale | Restart / scale only | Bounce DB or leftover cell; disable TLS; ship another 3.10.x with unbounded `FraudClient` |
| Trade-off analysis | Rollback vs flag-off vs timeouts-in-place; timeouts + breaker vs larger Tomcat pool; canary % + pipeline smoke vs Friday ship; paper BayOps vs live Bedrock | Mentions rollback or timeouts | Treats rollback as the only fix forever, or “max=2000” as strategy |
| Security / reliability | Avery 503 named; no PAN on the worksheet; least-privilege read + rollback; no secrets in a model prompt | Mentions merchant 503 | Invents `BAYPAY_DB_PASSWORD` or puts PAN in comms / BayOps JSON |
| Communication | Rate + P99 + 503; canary 1/3 named; Hikari-not-the-page; BayOps reject named; does not announce a DB outage | Usable, slightly over-confident | Blames “the database” or “the JVM” with no waiter / dependency quote |
| Efficiency | 90–150 minutes; no live AMP/AWS/Bedrock | Complete but slow | Incomplete worksheet or live apply to “reproduce” |

Stabilization that only says “bounce the pool,” “bounce `dmgr-east`,” or “scale to 20” while **3.8.4** is the last healthy image loses Production awareness.

BayOps: planted `provenRootCause` / invented `evidence/db-failover.json` / `BayOps-auto` bounce of `dmgr-east` must be **rejected**. Four buckets + `humanApproval` not auto-approved. A lucky “the AI is wrong” with no missing-file quote and no proven-RCA quote must **not** max Diagnostic method.

**Pass guideline:** weighted score ≥ 70; student quotes **rate, P99, 503, Hikari pending**, **3.10.0 1/3**, **WAITING / FraudClient**, and **in-flight / zero successes**; stabilize = **3.8.4** or canary stop / flag-off / timeouts; BayOps Multi-AZ / `dmgr-east` **rejected**; no database or leftover-cell bounce. Live Bedrock neither raises nor lowers the score.

## Contrast (do not require students to name these RCAs)

Score a **1** on Technical accuracy if the student pastes another pack’s instructor label as *this* RCA without quoting INC-CAP-4 files: INC-JVM-804 (FX), INC-PROD-1301 (cardinality), INC-SEC-1402 (cert / CNAME), INC-AWS-1104 (`Path=/`), INC-AWS-1205 (9080 debug). Same *class* of hang as 804 is acceptable if they still quote **FraudClient** and **fraud.baypay.example** from *this* dump.
