# Week 2 — Knowledge Check

**Format:** 15 questions · **Time:** 20 minutes closed-book (or open-book for self-paced)

---

## Questions

1. Name two business reasons enterprises use multiple AWS accounts instead of one account with many VPCs.
2. What is the difference between an SCP and an IAM policy?
3. What is the purpose of a landing zone?
4. Which account type typically hosts organization CloudTrail logs in a well-architected design?
5. What AWS API call does Terraform automation use to obtain temporary credentials in a workload account?
6. What is the “confused deputy” problem in cross-account access?
7. How does `sts:ExternalId` help secure cross-account role trust?
8. Where should a centralized Terraform state bucket often live in a multi-account model?
9. What provider block configuration allows Terraform to run against a different account than the caller’s default credentials?
10. Why should CI session names be descriptive (e.g. `github-pr-42`)?
11. Name one symptom that an SCP—not IAM—is blocking a Terraform apply.
12. What OU commonly contains dev, test, and prod workload accounts?
13. In single-account lab mode, what document must students still produce to show they understand multi-account design?
14. What course tag must remain on resources for `scripts/aws/` start/stop?
15. How does Week 4 CI authentication differ from Week 2 manual `assume-role` export?

---

## Answer key (instructors only)

| # | Answer |
|---|--------|
| 1 | Any two: blast radius isolation, billing boundaries, compliance boundaries, quota isolation, clearer audit scope |
| 2 | SCP sets maximum permissions ceiling for accounts/OUs; IAM grants permissions to principals within an account; SCP cannot grant access alone |
| 3 | Pre-configured multi-account environment with guardrails, identity, logging, and account vending baseline |
| 4 | Log archive account (Security OU) |
| 5 | `sts:AssumeRole` (or `AssumeRoleWithWebIdentity` for OIDC) |
| 6 | Third party or wrong principal could assume a role intended for another customer/context without proper conditions |
| 7 | Ensures only intended third party with shared secret can assume role; mitigates cross-customer assume-role attacks |
| 8 | Dedicated state/shared services account (or per-account with cross-account access—accept either with justification) |
| 9 | `assume_role` block in `provider "aws"` |
| 10 | CloudTrail auditability; incident forensics; distinguishes human vs automation sessions |
| 11 | AccessDenied despite correct IAM role policy; API denied at organization level; works in one OU not another |
| 12 | Workloads OU (or Non-Production / Production subdivisions) |
| 13 | Architecture diagram + account matrix documenting logical/target multi-account separation |
| 14 | `Course=terraform-enterprise` |
| 15 | Week 4 uses GitHub OIDC JWT + `AssumeRoleWithWebIdentity`; no manual export of access keys |

**Passing score:** 80% (12/15)
