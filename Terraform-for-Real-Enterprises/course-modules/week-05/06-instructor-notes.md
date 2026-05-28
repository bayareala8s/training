# Week 5 — Instructor Notes

## Pre-class checklist

- [ ] Confirm students completed Week 4 CI (plan on PR)
- [ ] Verify `labs/shared/environments/test` and `prod` examples are current
- [ ] Ensure students have unique S3 state keys per environment
- [ ] Share drift report template path (`docs/templates/drift-report.md` if present)

## Timing adjustments

| If running short | Cut |
|------------------|-----|
| 30 min | Scenario D (healthcare parity) to reading |
| 45 min | Optional driftctl demo |

| If running long | Add |
|-----------------|-----|
| 30 min | Live `moved` block demo in dev |
| 20 min | Compare saved plan vs fresh plan after 10-minute delay |

## Live demo script — drift (15 min)

1. Apply dev baseline
2. Add console SG rule; run plan—highlight `~` in-place change
3. Revert with apply; show clean plan
4. Show promotion checklist on slide while test apply runs in background (pre-recorded acceptable)

## Live demo script — promotion (10 min)

1. Show three `backend.hcl` keys side by side
2. `make plan ENV=test` — point at CIDR and tag differences in tfvars
3. Emphasize **never** shared state key

## Common student mistakes

| Mistake | Teaching moment |
|---------|-----------------|
| Applying prod tfvars to dev directory | Backend key + var file pairing |
| “Drift is always bad” | Adopt-via-code path for intentional changes |
| Skipping test apply | Scenario A retail outage |
| `state mv` without backup | `state pull` first—every time |

## Discussion prompts

1. “Should prod console access exist at all for infrastructure?”
2. “Who approves `forces replacement` in plan output?”
3. “How often should we run read-only prod plans?”

## Accessibility

- Provide filled promotion checklist template
- Pair students for console drift step (screen reader: use CLI drift alternative)

## Link to next week

Preview failed apply: “What if test apply stops halfway?” Tease state versioning lab.
