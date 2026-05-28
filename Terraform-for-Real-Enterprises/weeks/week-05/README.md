# Week 5 – Environment Promotion & Drift Detection

## Learning Objectives

- Promote the same module/config across dev → test → prod with environment-specific vars
- Detect and explain drift (console changes vs state)
- Refactor Terraform safely using moved blocks and targeted plans

## Topics

- Dev/Test/Prod promotion
- Drift detection strategies
- Infrastructure consistency
- Refactoring Terraform safely

## Labs

| Lab | Description |
|-----|-------------|
| **5.1** | Wire `environments/dev`, `test`, `prod` with shared modules |
| **5.2** | Introduce drift manually; run `terraform plan` and document delta |
| **5.3** | Remediate drift (import, refresh-only, or corrective apply) |

## Deliverables

1. **Environment promotion workflow** — Documented variable strategy and promotion checklist
2. **Drift remediation report** — What drifted, root cause, fix, prevention

## Suggested Time

8–9 hours

## Submission

PR: `week-05: env promotion and drift report` including `docs/drift-report-week05.md`.
