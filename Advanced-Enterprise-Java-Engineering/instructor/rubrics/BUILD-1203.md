# Rubric — BUILD-1203 Configuration automation

**Type:** BUILD  
**awsLab:** no  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. Ansible CLI absence must not fail the lab. A playbook that only `file:` mkdir is not a high Technical score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Local connection; templates payment env **and** Liberty `server.env`; `BAYPAY_DB_HOST` from a var; JDBC URL uses that host | One template complete | Starter unchanged |
| Diagnostic method | 20% | Listed missing template tasks and vars before editing | Added tasks until YAML “looked full” | Opened `solutions/` first |
| Production awareness | 15% | Same host contract for Boot and Liberty; AEJE-D-058; `db-east.baypay.example` | Files render; Liberty skipped | Invented a live SSH estate |
| Trade-off analysis | 15% | Ansible vs image-baked env vs Terraform `templatefile` | Preference with little why | No trade-off |
| Security / reliability | 10% | Password not a git literal; no SSH password in inventory | Password omitted entirely | `changeme` or a real secret committed |
| Communication | 10% | PF-iac automation section readable | Incomplete excerpt | Empty worksheet |
| Efficiency | 5% | File checklist; syntax-check optional | Finished in session | Required a remote host or AWS |

**Pass guideline:** weighted score ≥ 70, both env files templated from the host var, no password literal. `--syntax-check` neither required nor extra credit that replaces missing Liberty `server.env`.
