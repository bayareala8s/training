# Week 1 — Knowledge Check

**Format:** 15 questions · **Time:** 20 minutes closed-book (or open-book for self-paced)

---

## Questions

1. What is the primary purpose of Terraform state?
2. Name three risks of storing state only on a local laptop.
3. What does `terraform plan` do before showing a diff?
4. Why do enterprises pin `required_providers` versions?
5. What AWS services implement Terraform remote state and locking in this course?
6. What is the “bootstrap problem” for remote state?
7. How do `default_tags` help governance?
8. Give two differences between Terraform and CloudFormation.
9. What does `# forces replacement` in a plan indicate?
10. Why should production applies always follow a reviewed plan?
11. What file types must never be committed to Git in IaC repos?
12. What is declarative infrastructure?
13. Name two reasons to split state into multiple files/stacks.
14. What command downloads provider plugins?
15. What tag does this course use for AWS start/stop scripts?

---

## Answer key (instructors only)

| # | Answer |
|---|--------|
| 1 | Map Terraform resource addresses to real cloud resource IDs and metadata for dependency tracking |
| 2 | Any three: loss/theft, no locking/concurrency corruption, no backup/versioning, not shareable, compliance |
| 3 | Refreshes current infrastructure from APIs (default), compares to desired config, computes graph |
| 4 | Prevent breaking changes from unreviewed provider upgrades; reproducible builds |
| 5 | Amazon S3 (state storage), DynamoDB (locking) |
| 6 | State bucket cannot store its own state initially; bootstrap uses local state first |
| 7 | Consistent cost allocation, compliance tagging, automation, audit |
| 8 | Any two: multi-cloud vs AWS-only, self-managed state vs stack state, HCL vs YAML/JSON, etc. |
| 9 | Resource must be destroyed and recreated; often causes downtime or new IDs |
| 10 | Human review, change control, predictability, audit trail |
| 11 | tfvars with secrets, state files, credentials, `.terraform/` |
| 12 | Describe desired end state; tool determines steps |
| 13 | Blast radius reduction, parallel applies, different approval paths, smaller plans |
| 14 | `terraform init` |
| 15 | `Course=terraform-enterprise` |

**Passing score:** 80% (12/15)
