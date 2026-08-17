# Week 7 — Knowledge Check

**Format:** 15 questions · **Time:** 20 minutes closed-book (or open-book for self-paced)

---

## Questions

1. Why is **least privilege** critical for Terraform CI roles?
2. What is wrong with storing long-lived AWS access keys in GitHub?
3. Name two purposes of mandatory **resource tags** in enterprises.
4. How do `default_tags` help on the AWS provider?
5. What does **Checkov** analyze?
6. How should teams document skipped Checkov checks?
7. What is **policy-as-code**?
8. How do **SCPs** differ from Terraform module constraints?
9. Why should Terraform state be treated as **sensitive**?
10. What is **OIDC** used for in GitHub Actions AWS auth?
11. Name one difference between plan-time and apply-time enforcement.
12. What is **ABAC** and how do tags relate?
13. What tool does this course use for Terraform linting besides Checkov?
14. Give one example SOC2 theme mapped to Terraform practice.
15. Who should approve security policy exceptions?

---

## Answer key (instructors only)

| # | Answer |
|---|--------|
| 1 | CI compromise would grant excessive cloud access; limits blast radius |
| 2 | Keys leak via repo; no short-lived/session scoping; rotation burden |
| 3 | Any two: cost allocation, automation, compliance, ABAC, ownership |
| 4 | Applies baseline tags to all supported resources automatically |
| 5 | Terraform/IaC static misconfigurations against policies/benchmarks |
| 6 | Ticket ID, owner, reason, expiry review in `.checkov.yml` or equivalent |
| 7 | Machine-readable policies evaluated against code/plan (OPA, Sentinel, Checkov) |
| 8 | SCPs are org/account API ceilings; modules guide desired config—SCP can deny what TF proposes |
| 9 | May contain sensitive attributes; maps all resource IDs |
| 10 | Federated trust to assume IAM role without static keys |
| 11 | Example: Checkov/OPA on PR vs SCP deny at API apply |
| 12 | Attribute-Based Access Control; IAM conditions match resource/principal tags |
| 13 | tflint |
| 14 | Example: CC6.1 logical access → IAM roles; CC8.1 change management → PR/plan |
| 15 | Security/platform with time-bound ticket and accountability |

**Passing score:** 80% (12/15)
