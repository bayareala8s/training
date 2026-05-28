# Week 6 — Instructor Notes

## Pre-class checklist

- [ ] Confirm S3 versioning enabled on student state buckets (bootstrap)
- [ ] Warn against prod state restore exercises
- [ ] Verify `scripts/terraform/rollback-plan.sh` is executable
- [ ] Prepare break-glass policy slide for `force-unlock`

## Timing adjustments

| If running short | Cut |
|------------------|-----|
| 30 min | DR multi-region deep dive to capstone preview |
| 20 min | Lab 6.3 to homework |

| If running long | Add |
|-----------------|-----|
| 30 min | Game day: corrupt local copy of pulled state (not S3) and restore |
| 15 min | CloudTrail demo for state bucket PutObject |

## Live demo script — failed apply (20 min)

1. Add invalid AMI resource in **instructor sandbox only**
2. Show non-zero exit; `state list`
3. Remove resource; plan; discuss taint if present
4. **Do not** demo in shared org prod

## Live demo script — S3 versions (10 min)

1. `list-object-versions` on dev state key
2. Show version ID and LastModified
3. Explain restore without performing in shared account unless isolated

## Common student mistakes

| Mistake | Teaching moment |
|---------|-----------------|
| Immediate re-apply after failure | Plan first; understand partial state |
| Restoring state without AWS inventory | Scenario B insurance |
| `force-unlock` without checking CI | Stale job vs real lock |
| Git revert without plan review | May propose unexpected destroys |

## Discussion prompts

1. “When is forward fix safer than revert?”
2. “What is your state bucket RPO?”
3. “Who is allowed to run `state rm` in prod?”

## Safety rules

- **Dev only** for invalid AMI lab
- State restore requires instructor approval in shared sandboxes
- Document all `force-unlock` in ticket

## Link to next week

“Recovery runbooks mean nothing without least privilege and scanning.” Preview Checkov failure blocking PR.
