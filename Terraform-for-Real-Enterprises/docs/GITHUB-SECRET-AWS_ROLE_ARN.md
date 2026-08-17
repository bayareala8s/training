# GitHub Secret — Week 4 OIDC (ACTION REQUIRED)

OIDC is configured in AWS account **277374794397**. Add one repository secret so CI can plan against live dev state.

## Secret to add

| Field | Value |
|-------|--------|
| **Repository** | `bayareala8s/training` |
| **Secret name** | `AWS_ROLE_ARN` |
| **Secret value** | `arn:aws:iam::277374794397:role/github-terraform` |

## Option A — GitHub UI (recommended)

1. Open: https://github.com/bayareala8s/training/settings/secrets/actions
2. Click **New repository secret**
3. Name: `AWS_ROLE_ARN`
4. Value: `arn:aws:iam::277374794397:role/github-terraform`
5. Click **Add secret**

## Option B — GitHub CLI

```bash
gh auth login
gh secret set AWS_ROLE_ARN \
  --repo bayareala8s/training \
  --body "arn:aws:iam::277374794397:role/github-terraform"
```

## Verify CI

After the secret is set and the workflow is pushed:

1. Open https://github.com/bayareala8s/training/actions
2. Run or re-run workflow **Terraform CI**
3. Job **plan-dev** should complete with a plan against remote dev state (no mock vars)

If `plan-dev` fails with "Not authorized to perform sts:AssumeRoleWithWebIdentity":

- Confirm secret name is exactly `AWS_ROLE_ARN`
- Confirm workflow runs from `bayareala8s/training` (trust policy allows `repo:bayareala8s/training:*`)

## AWS resources created by setup-oidc.sh

| Resource | ARN / name |
|----------|------------|
| OIDC provider | `arn:aws:iam::277374794397:oidc-provider/token.actions.githubusercontent.com` |
| IAM role | `arn:aws:iam::277374794397:role/github-terraform` |
| Inline policy | `github-terraform-plan` (read/plan scoped) |

## Widen permissions for apply job (Lab 4.2 only)

The current role is **plan-only**. Before uncommenting `apply-dev` in the workflow, attach a broader policy or use the Week 2 `terraform-runner-policy.json` pattern with least privilege.

## Related

- [WEEK-04-GITHUB-SETUP.md](WEEK-04-GITHUB-SETUP.md)
- [scripts/github/setup-oidc.sh](../scripts/github/setup-oidc.sh)
