# Week 3 — Instructor Notes

## Pre-class checklist

- [ ] Verify `modules/vpc` and `modules/compute` exist and `make plan ENV=dev` works
- [ ] Prepare diff showing a breaking output rename (teaching moment)
- [ ] Confirm students can create Git tags (or use course tags on instructor repo)
- [ ] Install/demo `tflint` optional for advanced students

## Timing adjustments

| If running short | Cut |
|------------------|-----|
| 30 min | Security-group stretch goal |
| 45 min | Lab 3.3—assign CHANGELOG as homework |

| If running long | Add |
|-----------------|-----|
| 30 min | Live semver bump: minor vs major PR demo |
| 20 min | `terraform test` preview if Terraform ≥ 1.6 |

## Live demo script — composition (15 min)

1. Open `labs/shared/environments/dev/main.tf`
2. Highlight `module.vpc` → `module.compute` reference chain
3. Run `terraform graph | dot -Tpng > graph.png` (optional visual)
4. Show plan dependency order without `depends_on`

## Common student mistakes

| Mistake | Teaching moment |
|---------|-----------------|
| Editing module without validating all envs | Run `make validate` |
| Output rename without major version | Semver contract |
| God module PR adding RDS to vpc | Decomposition |
| `ref=main` in examples | Copy-paste hazard |
| Forgetting README on new variable | API completeness |

## Discussion prompts

1. “What is the smallest useful module?”
2. “When should teams fork a module vs upstream a feature?”
3. “How do modules interact with SCP deny lists?”

## Accessibility

- Provide starter README table template
- Accept diagram on paper photo if needed

## Link to next week

“Your tagged `v1.0.0` module will be planned by GitHub Actions on every PR—interface stability reduces CI noise.”
