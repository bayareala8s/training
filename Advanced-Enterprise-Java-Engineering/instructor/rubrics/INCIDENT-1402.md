# Rubric — INCIDENT-1402 Certificate expiration

**Type:** INCIDENT  
**awsLab:** no (files only)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “the cert expired” with no quoted **ACM status** (`PENDING_VALIDATION` or `FAILED`, not `ISSUED`) and no quoted **missing validation CNAME** (`_2f91d4c0.payments.apps.baypay.example` / NXDOMAIN) must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Leaf expired **2026-09-01 00:00 UTC**; ACM replacement **PENDING_VALIDATION** (or FAILED); validation CNAME absent; tasks RUNNING; `:8080` 200 | Expired named; ACM or DNS side missing | “Security group” or “Postgres” or kube `payment-tls` / wrong CN as RCA |
| Diagnostic method | Gate 1→2→3; handshake before ACM; ACM status **and** missing `_2f91d4c0` quoted | Used all files; skipped a hypothesis | Opened solutions or `route53-records.txt` first |
| Production awareness | Restore HTTPS (attach last-valid **or** re-create validation + issue); no TLS-off; no DB/`dmgr-east` bounce | Restart tasks only | Disable TLS or bounce Postgres |
| Trade-off analysis | DNS-as-code vs console cleanup; ticket 30 days / page 7 days; last-valid leaf vs wait for issue | Mentions alerts or Terraform | HTTP-only as strategy |
| Security / reliability | Avery handshake retries; no private key; least-privilege describe; identity domain eats 99.99% | Mentions HTTPS | Pastes a private key or invents `BAYPAY_DB_PASSWORD` |
| Communication | RUNNING tasks + failed handshake named; does not invent a DB outage | Usable, slightly over-confident | Blames “TLS” with no date, ACM status, or DNS fact |
| Efficiency | 45–75 minutes; no live ACM/Route 53 apply | Complete but slow | Incomplete worksheet or live apply to “reproduce” |

Stabilization that only says “the cert expired, renew it” without ACM status and the validation name loses Diagnostic method even if the catalog title matches.

Importing INC-K8S-1005 (`payment-tls`, CN `*.baypay.internal`) as this pack’s RCA caps Technical accuracy at 1 unless the student contrasts ACM/DNS validation.

**Pass guideline:** weighted score ≥ 70, ACM status quoted, missing validation CNAME quoted, stabilize = restore HTTPS, remediate includes DNS as code and 30/7-day alerts, TLS stays on.
