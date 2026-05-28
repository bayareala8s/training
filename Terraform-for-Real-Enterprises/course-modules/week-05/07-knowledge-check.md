# Week 5 — Knowledge Check

**Format:** 15 questions · **Time:** 20 minutes closed-book (or open-book for self-paced)

---

## Questions

1. What is **environment promotion** in enterprise Terraform?
2. Why must dev, test, and prod use **separate state keys**?
3. What artifact should be reviewed before a production apply?
4. Define **configuration drift**.
5. How does `terraform plan` detect drift by default?
6. When should you update `.tf` instead of running apply to revert drift?
7. What does `forces replacement` in a plan indicate for promotion decisions?
8. Name two organizational controls that reduce console drift.
9. What is the purpose of a `moved` block?
10. When might you use `terraform state mv` instead of `moved`?
11. What is wrong with sharing one state file across dev and prod?
12. What is a saved plan file used for?
13. What exit code does `terraform plan -detailed-exitcode` return when changes are pending?
14. Name one difference between “adopt drift in code” and “revert drift with apply.”
15. What should a drift report include for prevention?

---

## Answer key (instructors only)

| # | Answer |
|---|--------|
| 1 | Moving tested, reviewed infrastructure changes through environments (dev→test→prod) with gates—not ad hoc applies |
| 2 | Isolates blast radius; prevents one apply from affecting wrong resources; separate approval domains |
| 3 | Reviewed `terraform plan` output and/or saved plan file; change advisory approval |
| 4 | Real infrastructure differs from Terraform desired config and/or state |
| 5 | Refreshes state from APIs and compares to desired configuration |
| 6 | When the console/manual change represents the desired new truth |
| 7 | Resource will be destroyed and recreated—requires explicit approval and scheduling |
| 8 | Any two: SCPs limiting console, read-only prod IAM, nightly plan jobs, Config rules, break-glass process |
| 9 | Refactor state addresses without destroying underlying resources when configured correctly |
| 10 | One-off operations, legacy migrations, when moved blocks impractical—always with backup |
| 11 | Couples environments; wrong variables can destroy prod; no separate rollback |
| 12 | Ensures apply matches reviewed plan; audit evidence |
| 13 | Exit code 2 |
| 14 | Adopt = change code to match reality; revert = apply code to overwrite reality |
| 15 | Root cause, remediation, controls (SCP/IAM/CI scheduled plan), owner/SLA |

**Passing score:** 80% (12/15)
