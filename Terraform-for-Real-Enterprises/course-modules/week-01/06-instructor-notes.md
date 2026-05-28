# Week 1 — Instructor Notes

## Pre-class checklist

- [ ] Confirm students have AWS account or sandbox OU access
- [ ] Pre-create IAM permission boundary doc (what students can/cannot do)
- [ ] Share estimated AWS cost (~$15–40/month dev with lab-stop discipline)
- [ ] Verify GitHub access for later weeks

## Timing adjustments

| If running short | Cut |
|------------------|-----|
| 30 min | Scenario D (CloudFormation coexistence) to reading |
| 45 min | Lab 1.2 practice—assign as homework |

| If running long | Add |
|-----------------|-----|
| 30 min | Live demo: corrupt local state file and show recovery concept |
| 20 min | Pair exercise: design state key naming convention |

## Live demo script — remote state (15 min)

1. Show empty S3 bucket versioning disabled → enable versioning live
2. Run `terraform init -migrate-state` if demonstrating migration
3. Open DynamoDB lock item during parallel `apply` (second terminal) — **careful in shared accounts**

## Common student mistakes

| Mistake | Teaching moment |
|---------|-----------------|
| Committing `terraform.tfvars` | Show secret scanner; fix with `.gitignore` |
| Same S3 bucket name | Global uniqueness—use `student-id` prefix |
| Applying bootstrap twice | Import vs fresh bucket naming |
| Skipping `make lab-stop` | Show NAT/instance charges in Cost Explorer |

## Discussion prompts

1. “Who should be allowed to run `terraform apply` in production?”
2. “What belongs in state vs in Parameter Store?”
3. “When would you split state files for one application?”

## Accessibility

- Provide pre-written `backend.hcl` template filled except bucket name
- Offer paired lab partners for students new to CLI

## Link to next week

Preview OU structure slide: “Week 1 state bucket lives in which account in a landing zone?” Tease cross-account roles.
