# Week 6 – Rollback, Recovery & Disaster Recovery

## Learning Objectives

- Recover from failed applies and corrupted or divergent state
- Document rollback strategies (Git revert + apply, targeted destroy, backup restore)
- Plan for regional failure and state backup

## Topics

- Terraform failure recovery
- State repair techniques
- Rollback strategies
- Region failure planning
- Backup and recovery

## Labs

| Lab | Description |
|-----|-------------|
| **6.1** | Simulate failed deployment (bad variable, dependency error) |
| **6.2** | Recover infrastructure using state pull, fix, and controlled apply |
| **6.3** | Restore state from S3 versioning or documented backup procedure |

## Deliverables

1. **Rollback automation workflow** — Script or CI job outline (even if semi-manual)
2. **Recovery procedure documentation** — Runbook: `docs/runbooks/terraform-recovery.md`

## Suggested Time

8–10 hours

## Submission

PR: `week-06: recovery runbook and rollback workflow` with evidence of successful recovery exercise.
