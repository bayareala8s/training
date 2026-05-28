# Week 6 — Knowledge Check

**Format:** 15 questions · **Time:** 20 minutes closed-book (or open-book for self-paced)

---

## Questions

1. What may be left in AWS after a **failed apply**?
2. What does it mean when a resource is **tainted**?
3. When should you run `terraform untaint`?
4. What is the difference between **Git rollback** and **state rollback**?
5. What command backs up state to a local JSON file?
6. Why is S3 **versioning** important for state buckets?
7. When is restoring an old state version **dangerous**?
8. What does `terraform state rm` do to AWS resources?
9. What does `terraform force-unlock` do and when is it justified?
10. Name two symptoms of a stale state lock.
11. What is **RPO** in the context of state recovery?
12. What is **RTO**?
13. When is **forward fix** preferred over Git revert?
14. What should a terraform recovery runbook include?
15. Why should you run `terraform plan` before re-applying after a failure?

---

## Answer key (instructors only)

| # | Answer |
|---|--------|
| 1 | Partially created resources; state may record some created addresses |
| 2 | Marked for recreation on next apply due to apply failure |
| 3 | Only after verifying the resource is healthy and should not be replaced |
| 4 | Git rollback changes desired config; state rollback changes Terraform’s mapping snapshot—different levers |
| 5 | `terraform state pull > backup.json` |
| 6 | Allows recovery of prior state objects after corruption or bad apply |
| 7 | When AWS reality diverged from that state snapshot—plan may be destructive/wrong |
| 8 | Removes from state only; does not destroy AWS resource (orphans it from Terraform) |
| 9 | Releases DynamoDB lock; justified when stale lock after crashed CI, with audit |
| 10 | Any two: second apply hangs on lock; CI job killed mid-apply; lock ID visible in error |
| 11 | Recovery Point Objective—max acceptable data/state loss window |
| 12 | Recovery Time Objective—max acceptable downtime to restore operations |
| 13 | Small targeted fix; state healthy; faster than revert when revert plan is risky |
| 14 | Triage steps, backup/restore, lock procedure, Git revert flow, escalation, evidence logging |
| 15 | Understand proposed changes; avoid compounding partial failure |

**Passing score:** 80% (12/15)
