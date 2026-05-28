# Week 8 — Knowledge Check

**Format:** 15 questions · **Time:** 20 minutes · **Context:** Capstone integration review

---

## Questions

1. What percentage of the course grade is the capstone?
2. Name the four capstone options.
3. List three **required deliverables** from the capstone README.
4. Which week’s practice covers remote state and backends?
5. Which week covers environment promotion?
6. Which week covers drift detection and remediation?
7. Which week covers state recovery and rollback runbooks?
8. Which week covers Checkov and IAM least privilege?
9. What is the recommended presentation length?
10. Name two rubric criteria used to grade the capstone.
11. Why should prod live demo be avoided in presentations?
12. What does “Excellent (4)” mean for **CI/CD & ops** on the rubric?
13. What cost control command does this course document for labs?
14. What should you **not** destroy until all environments are gone?
15. Name one integration item required in the capstone lab checklist.

---

## Answer key (instructors only)

| # | Answer |
|---|--------|
| 1 | 30% |
| 2 | Landing zone; shared services platform; multi-region DR; internal Terraform platform |
| 3 | Any three: Terraform repos, CI/CD, diagrams, cost analysis, security review, presentation |
| 4 | Week 1 |
| 5 | Week 5 |
| 6 | Week 5 |
| 7 | Week 6 |
| 8 | Week 7 |
| 9 | 15–20 minutes |
| 10 | Any two: Architecture, Terraform quality, CI/CD & ops, Security, Docs & demo |
| 11 | Risk of failure/credentials; use dev/test or recording |
| 12 | Full PR workflow with drift/rollback considered |
| 13 | `make lab-stop` |
| 14 | Bootstrap state bucket |
| 15 | Any one: remote state, modules, CI plan on PR, promotion path, security report, etc. |

**Passing score:** 80% (12/15)
