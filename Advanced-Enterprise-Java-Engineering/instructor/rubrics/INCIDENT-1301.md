# Rubric — INCIDENT-1301

**Type:** INCIDENT  
**awsLab:** no (files only)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “database,” “GC,” or “just a bad deploy” with no quoted **series count**, no quoted **scrape duration**, and no quoted **`customerId` / `accountId`** must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | 3.9.0 registered **`customerId`** and **`accountId`** (and optionally Idempotency-Key) on `payment.create`; series **~12k → ~2.6M**; scrape **~200 ms → multi-second / timeout**; throughput **~180 → ~22** RPS; P99 **~120 ms → ~4.8 s**; 5xx not primary | Named the deploy or one number; one label quoted | “Postgres down,” “GC / DEBUG toString,” or “IAM” as RCA without contrast |
| Diagnostic method | Gate 1→2→3; RED before scrape/JVM; scrape/series quoted; both label names quoted from gate 3 | Used all files; skipped a hypothesis | Opened solutions or `meter-registration.txt` first |
| Production awareness | Stabilize on **`3.8.4`** or **tag removal**; no Postgres bounce; no `dmgr-east` bounce; no heap dump as first act; not treated as INC-JVM-805 | Restart / scale only | Bounce DB or dmgr-east; ship another 3.9.x with the same tags |
| Trade-off analysis | Rollback vs disable tags; recording rules + scrape budget vs raw timers; logs/traces vs series for one merchant | Mentions rollback or labels | Treats rollback as the only fix forever |
| Security / reliability | Avery late 201 (not 500); no PAN on the worksheet; least-privilege read + rollback | Mentions merchant delay | Invents `BAYPAY_DB_PASSWORD` or puts PAN in comms |
| Communication | Rate + P99 + 5xx-not-the-page; scrape/series named; does not invent a DB outage | Usable, slightly over-confident | Blames “the JVM” with no scrape or label quote |
| Efficiency | 45–75 minutes; no live AMP/AWS | Complete but slow | Incomplete worksheet or live apply to “reproduce” |

Stabilization that only says “tune GC” or “bounce the pool” while **3.8.4** is the last healthy image loses Production awareness.

**Pass guideline:** weighted score ≥ 70, student quotes **`customerId` and `accountId`** plus **scrape duration and series count**, stabilize = **3.8.4** or extra-tag removal, no database or `dmgr-east` bounce.
