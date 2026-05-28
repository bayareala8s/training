# Week 7 – Security, Compliance & Governance as Code

> **Full module:** [course-modules/week-07](../../course-modules/week-07/) — detailed lecture, assignment, quiz, instructor notes

## Learning Objectives

- Apply IAM least privilege for Terraform runners and created resources
- Enforce tagging and policy-as-code in CI
- Produce audit-ready evidence (plans, tags, guardrail reports)

## Topics

- IAM least privilege
- Policy-as-Code concepts
- Cost governance
- Compliance guardrails
- Infrastructure auditability

## Labs

| Lab | Description |
|-----|-------------|
| **7.1** | Harden Terraform deployment roles (scoped policies, no `*:*` admin) |
| **7.2** | Implement mandatory tagging via variables and OPA/Checkov/custom rules |
| **7.3** | Configure compliance checks in CI; fix or document accepted risks |

## Deliverables

1. **Governance policies** — Tag schema, IAM boundaries, optional SCP alignment notes
2. **Security validation report** — Tool output + remediation summary

## Suggested Time

8–9 hours

## Submission

PR: `week-07: governance and security report`.
