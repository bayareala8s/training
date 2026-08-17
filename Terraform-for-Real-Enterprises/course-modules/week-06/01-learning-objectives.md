# Week 6 — Learning Objectives

By the end of this module, students will be able to:

## Knowledge (Remember / Understand)

1. Explain how Terraform behaves during a **failed apply** (partial creation, tainted resources, state vs AWS reality).
2. Describe **state recovery** options: `state pull`, S3 object versioning, `state rm`, `import`, and professional escalation paths.
3. Contrast **Git revert rollback** with **state rollback** and when each restores service vs restores Terraform truth.
4. Define disaster recovery (DR) objectives (RTO/RPO) in the context of Terraform-managed infrastructure.

## Skills (Apply / Analyze)

5. Diagnose a failed apply lab scenario and document what exists in AWS vs state.
6. Back up state, list S3 versions, and restore a prior state object in a sandbox (with instructor approval).
7. Use `terraform state` subcommands (`list`, `show`, `rm`, `mv`, `untaint`) safely with remote backends.
8. Document a **terraform recovery runbook** including rollback script usage and CI re-apply workflow.

## Professional practice (Evaluate / Create)

9. Design a DR tabletop scenario for state bucket loss or regional outage affecting the backend.
10. Recommend monitoring and alerting for failed applies, lock contention, and state bucket anomalies.

## Bloom’s alignment

| Level | Objective # |
|-------|----------------|
| Understand | 1–4 |
| Apply | 5–8 |
| Evaluate | 9–10 |

## Certification alignment (optional study)

- HashiCorp Terraform Associate: troubleshooting, state management
- AWS DevOps Engineer: incident response, backup and restore
