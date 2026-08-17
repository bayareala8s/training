# Week 4 — Instructor Notes

## Pre-class checklist

- [ ] Confirm all students have GitHub forks and Actions enabled
- [ ] Pre-create OIDC provider + role in sandbox OR provide shared `AWS_ROLE_ARN`
- [ ] Test workflow run on instructor fork within 24 hours
- [ ] Document fallback: `-backend=false` plan if OIDC blocked
- [ ] Review [`labs/week-04/docs/oidc-setup.md`](../../labs/week-04/docs/oidc-setup.md) for `bayareala8s/training` org string

## Timing adjustments

| If running short | Cut |
|------------------|-----|
| 30 min | Lab 4.3—assign findings doc as homework |
| 45 min | Apply job demo—show screenshot only |

| If running long | Add |
|-----------------|-----|
| 30 min | Saved plan file artifact between jobs |
| 20 min | Branch protection + CODEOWNERS walkthrough |

## Live demo script — PR plan (25 min)

1. Open PR with trivial README change
2. Walk through Actions tabs: validate → security → plan
3. Show plan output snippet in logs or PR comment
4. Attempt merge without approval (if branch protection configured)
5. Show Environment waiting for reviewer on apply job

## Common student mistakes

| Mistake | Teaching moment |
|---------|-----------------|
| Missing `id-token: write` | OIDC 101 |
| Trust policy `sub` too broad | `repo:ORG/REPO:ref:refs/heads/main` |
| Static keys in secrets | Scenario A narrative |
| Apply on PR branch | `if` condition on ref |
| Ignoring `soft_fail` findings | Document accepted risks |
| Wrong working-directory | Init runs in empty dir |

## Discussion prompts

1. “Should plan and apply use different IAM roles?”
2. “What is the rollback story when apply succeeds but app is broken?”
3. “How long retain GitHub Actions logs for SOC2?”

## Accessibility

- Provide fork with workflow pre-copied
- Pair students for GitHub UI navigation

## Link to next week

Week 5: promotion between environments and drift—“CI green but AWS changed in console.”

## Security reminder

Never commit `AWS_SECRET_ACCESS_KEY` to demonstrate CI—use OIDC or instructor sandbox role only.
