# Week 4 — GitHub Actions Setup Guide

Step-by-step to enable CI for **Terraform for Real Enterprises** in the `bayareala8s/training` monorepo.

## Prerequisites

- Admin on `bayareala8s/training` (or your fork)
- AWS account with IAM permissions
- `gh` CLI logged in (`gh auth login`)

---

## Step 1 — AWS OIDC (one time)

From the course directory:

```bash
chmod +x scripts/github/setup-oidc.sh
./scripts/github/setup-oidc.sh
```

If thumbprint errors occur, fetch dynamically:

```bash
THUMBPRINT=$(openssl s_client -servername token.actions.githubusercontent.com \
  -connect token.actions.githubusercontent.com:443 2>/dev/null \
  | openssl x509 -fingerprint -noout -sha1 | cut -d= -f2 | tr -d ':')
OIDC_THUMBPRINT="$THUMBPRINT" ./scripts/github/setup-oidc.sh
```

Copy the printed `AWS_ROLE_ARN`.

**GitHub secret:**

1. Open https://github.com/bayareala8s/training/settings/secrets/actions
2. New repository secret: `AWS_ROLE_ARN` = `arn:aws:iam::ACCOUNT:role/github-terraform`

---

## Step 2 — Push workflow (monorepo)

The workflow file is:

`Terraform-for-Real-Enterprises/.github/workflows/terraform-ci.yml`

It validates **dev, test, prod** matrix, runs Checkov, and plans dev with mock env vars (no AWS creds required until OIDC is uncommented).

```bash
cd training   # monorepo root
git checkout -b week-04-ci-setup
# rsync or copy updated Terraform-for-Real-Enterprises from your local clone
git add Terraform-for-Real-Enterprises/.github/workflows/terraform-ci.yml
git add Terraform-for-Real-Enterprises/docs/WEEK-04-GITHUB-SETUP.md
git commit -m "Enable Terraform CI workflow for enterprise course"
git push -u origin week-04-ci-setup
gh pr create --title "Week 4: Terraform CI workflow" --body "Adds validate + checkov + plan jobs"
```

---

## Step 3 — Verify CI on PR

Open the PR. Expected jobs:

| Job | What it does |
|-----|----------------|
| `validate` (matrix) | fmt, init -backend=false, validate for dev/test/prod |
| `security` | Checkov on `modules/` |
| `plan-dev` | terraform plan with TF_VAR_* (mock) |

All should be green without AWS secrets.

---

## Step 4 — Enable real AWS plan (optional)

In `.github/workflows/terraform-ci.yml`, uncomment:

```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: ${{ env.AWS_REGION }}
```

Push to PR branch — plan job will call AWS APIs (read-only policy).

---

## Step 5 — Approval gates (Lab 4.2)

1. GitHub → Settings → Environments → New environment: `dev`
2. Required reviewers: 1
3. Uncomment `apply-dev` job in workflow
4. Merge to `main` → approve deployment → apply runs

---

## Monorepo path note

`TF_COURSE_ROOT: Terraform-for-Real-Enterprises` in the workflow env block.

If the course is the **repository root** (standalone), set:

```yaml
TF_COURSE_ROOT: ""
```

And adjust `paths:` filters to remove the prefix.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Workflow does not trigger | Ensure changed files match `paths:` filter |
| `working-directory` not found | Check `TF_COURSE_ROOT` matches monorepo layout |
| OIDC assume role failed | Verify trust policy `sub` matches `repo:org/repo:*` |
| Plan fails without creds | Mock TF_VAR_* block must stay until OIDC enabled |

---

## Related

- [labs/week-04/docs/oidc-setup.md](../labs/week-04/docs/oidc-setup.md)
- [labs/week-04/LAB-01-github-actions.md](../labs/week-04/LAB-01-github-actions.md)
- [docs/LAB-DEMO-GUIDE.md](LAB-DEMO-GUIDE.md)
