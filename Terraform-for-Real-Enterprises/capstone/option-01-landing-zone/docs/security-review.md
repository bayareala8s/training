# Security Review — Capstone Option 1

| Area | Finding | Status |
|------|---------|--------|
| Secrets in Git | Only `.example` tfvars/backend committed | Pass |
| Public exposure | Lab SG egress-only; no open SSH | Pass |
| Encryption | S3 state encrypt=true; VPC flow logs to CW | Pass |
| IAM | CI should use OIDC role (course `github-terraform`); no long-lived keys in repo | Pass (documented) |
| Least privilege | Runner policy should scope EC2/VPC/S3/DynamoDB (Week 2/7) | Acceptable for lab |
| Tags | Course + Environment + Owner required | Pass |
| Guardrails | Variable validation on environment/owner | Pass |

## Accepted risks (lab)

- Single AWS account simulates multi-account (documented).
- NAT instance instead of NAT Gateway in shared (cost).
- Checkov soft-fail in CI until baseline cleaned.

## Remediation backlog

1. Attach SCPs in real Organizations (deny leave org, deny unencrypted volumes).
2. Enable AWS Config recorder in shared-services account.
3. Harden CI apply with GitHub Environment approvals.
