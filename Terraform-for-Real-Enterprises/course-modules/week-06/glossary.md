# Week 6 — Glossary

| Term | Definition |
|------|------------|
| **Failed apply** | `terraform apply` exiting with errors after partial progress |
| **Partial apply** | Some resources created/updated before failure halted run |
| **Tainted resource** | Resource marked for replacement on next apply after apply error |
| **untaint** | Removes taint when resource is verified healthy |
| **State rollback** | Restoring prior state snapshot (e.g. S3 version) |
| **Git rollback** | Reverting commits and re-applying older desired configuration |
| **Forward fix** | New commit/plan resolving incident without reverting |
| **state pull** | Download current state JSON from backend |
| **state rm** | Remove resource address from state without destroying cloud resource |
| **force-unlock** | Administrative release of stuck state lock |
| **RPO** | Recovery Point Objective—acceptable data/state loss window |
| **RTO** | Recovery Time Objective—acceptable time to restore service |
| **Runbook** | Operational document for incident/recovery procedures |
| **Game day** | Scheduled exercise simulating failure scenarios |
| **Break-glass** | Emergency elevated access with audit requirements |
