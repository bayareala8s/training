# Rubric — INTERVIEW-1603 Troubleshooting interview

**Type:** INTERVIEW  
**awsLab:** no (files + oral/written method)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky RCA title (“expired cert”, “cardinality”, “Path=/”) with **no Gate 1 quotes** and **no next evidence class** must **not** max Diagnostic method (20%).

Do **not** require students to name or lecture instructor RCAs from INCIDENT-1301, INCIDENT-1402, INCIDENT-1104, or INCIDENT-1205. Symptom class is enough.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Quotes coexistence (RUNNING + HTTPS fail **or** rate/P99 + quiet 5xx + pending 0); ≥3 unproven hypotheses; ND bounce withdrawn | Quotes thin; hypotheses present | Treats leftover ND or “database is down” as proven; invents omitted files |
| Diagnostic method | Gate 1 quotes from the brief **then** next **evidence class**; lucky title not treated as proven | Used the brief; skipped next gate | Opened this `solutions/` first, **or** lucky RCA with no those quotes, **or** pasted 1301/1402/1104/1205 instructor RCA |
| Production awareness | No TLS-off; no Postgres/`dmgr-east` bounce; no ACM/AMP/RDS apply | Refused bounce; still “would apply to see graphs” | Executes or recommends those mutates |
| Trade-off analysis | Paper next-gate vs apply-to-reproduce; why HTTP `:8080` ≠ merchant HTTPS (A) or why 5xx-quiet still pages (B) | One honest trade-off | Requires live graphs to have a method |
| Security / reliability | Avery `c1603c33-…` named; no PAN; TLS stays on | Mentions merchant fail | Secrets or TLS-off “to restore HTTP” |
| Communication | 20-minute update: known / unknown / will-not / next gate | Usable, slightly over-confident | Announces a proven outage title |
| Efficiency | 45–75 minutes; one class finished | Complete but slow | Blank method, or both classes slogan-only |

Importing an instructor RCA as **proven** for this brief caps Diagnostic method at 1 and Technical accuracy at 3 unless the student withdraws it and still quotes the brief.

**Pass guideline:** weighted score ≥ 70, Gate 1 quotes, unproven list, next evidence class, no ND/DB bounce, no TLS-off, no instructor-RCA lecture. Lucky title alone does not pass method. Live Bedrock/AWS neither raises nor lowers the score if unused; if used as the path, cap Production awareness.
