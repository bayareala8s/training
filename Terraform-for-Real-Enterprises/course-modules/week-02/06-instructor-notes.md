# Week 2 — Instructor Notes

## Pre-class checklist

- [ ] Confirm whether students have Organizations admin or design-only mode
- [ ] Distribute placeholder account IDs for diagram exercises
- [ ] Review [`labs/week-02/iam/`](../../labs/week-02/iam/) templates for org-specific edits
- [ ] Remind: Week 1 state bucket “lives” in which account on landing zone slide
- [ ] Verify `make lab-stop` still works (`Course=terraform-enterprise`)

## Timing adjustments

| If running short | Cut |
|------------------|-----|
| 30 min | Scenario D to reading assignment |
| 45 min | Lab 2.3—assign plan capture as homework |

| If running long | Add |
|-----------------|-----|
| 30 min | Live SCP deny demo in sandbox OU (pre-built) |
| 20 min | Compare Control Tower vs custom landing zone |

## Live demo script — assume role (20 min)

1. Show trust policy `Principal` and `Condition` fields on slide
2. `aws sts assume-role` in terminal; highlight session name in output
3. Export creds; run `aws sts get-caller-identity` — account should be workload
4. `make plan ENV=dev` — show first 30 lines of plan
5. **Do not apply** in shared instructor account without break-glass process

## Common student mistakes

| Mistake | Teaching moment |
|---------|-----------------|
| Trust policy allows `*` principal | Confused deputy; tighten to role ARN |
| Applying with wrong account creds | State maps to wrong account → destructive plan |
| Ignoring SCP | Show AccessDenied from org vs IAM |
| Skipping architecture doc | Week 4 OIDC needs account model context |
| Using AdministratorAccess for runner | Least privilege lab policy purpose |

## Discussion prompts

1. “Should Terraform state live in the workload account or a dedicated state account?”
2. “Who is allowed to modify trust policies on `terraform-runner`?”
3. “What is the minimum OU structure for a 50-person company?”

## Accessibility

- Provide pre-filled Mermaid template for `week-02-accounts.md`
- Pair students: one diagrams, one writes IAM narrative

## Link to next week

Preview: “VPC module will be consumed identically in dev/test/prod accounts—interface stability matters.”

## Link from Week 1

Ask: “Your bootstrap bucket—is it in the management account or shared services in your design?”
