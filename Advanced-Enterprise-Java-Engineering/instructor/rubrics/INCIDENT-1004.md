# Rubric — INCIDENT-1004

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “wrong key” with no env-name-versus-Secret-key table must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Secret keys `password` + `BAYPAY_DB_USER`; env name `BAYPAY_DB_PASSWORD`; `optional: true`; empty password; auth / fail-fast | “Bad Secret” named; key mismatch mentioned; mapping fuzzy | “Postgres password rotated” or invented credential as RCA |
| Diagnostic method | Gate 1→2→3; Deployment env opened to answer name vs key; logs quoted | Used all files; skipped a hypothesis | Opened solutions or env YAML first |
| Production awareness | Add correct key or fix `valueFrom`; no DB bounce; no git password | Restart only | Bounce Postgres or commit `changeme` as the fix |
| Trade-off analysis | Kyverno / contract test vs checklist; `optional: true` blast radius | Mentions policy | `envFrom` chart names as strategy without a mapping |
| Security / reliability | Values stay `***`; never commit real secrets; fail-fast on empty password | Mentions redaction | Pastes a fabricated password |
| Communication | No secret values; injection scoped; does not claim a stolen DB | Usable, slightly over-confident | Blames “auth” in the first sentence with no key names |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

A worksheet that includes a live or invented password cannot score 5 on Security / reliability.
