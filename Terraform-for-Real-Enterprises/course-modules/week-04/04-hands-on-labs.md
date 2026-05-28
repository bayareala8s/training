# Week 4 — Hands-On Labs (Detailed)

**Total lab time:** ~5–7 hours · **Repository paths:** [`labs/week-04/`](../../labs/week-04/)

---

## Lab 4.1 — GitHub Actions Terraform CI

**Duration:** 3 hours · **Guide:** [labs/week-04/LAB-01-github-actions.md](../../labs/week-04/LAB-01-github-actions.md)

### Objectives

- Add workflow: fmt, validate, plan on pull request
- Configure working directory and Terraform version
- Begin OIDC setup for AWS credentials

### Detailed procedure

1. **Copy workflow template:**

```bash
mkdir -p .github/workflows
cp labs/week-04/workflows/terraform-ci.yml .github/workflows/terraform-ci.yml
```

2. **Edit workflow** for your fork:
   - `WORKING_DIRECTORY`: `labs/shared/environments/dev`
   - `TF_VERSION`: match `.terraform-version` (e.g. `1.7.5`)
   - Confirm `paths` filters match your change patterns
3. **OIDC setup** (recommended)—follow [labs/week-04/docs/oidc-setup.md](../../labs/week-04/docs/oidc-setup.md):
   - Create IAM OIDC provider for `token.actions.githubusercontent.com`
   - Create `github-terraform` role with trust `sub` for your repo
   - Add GitHub secret `AWS_ROLE_ARN`
   - Uncomment `aws-actions/configure-aws-credentials` in plan job when ready
4. **Open test PR:**

```bash
git checkout -b week-04-ci
# small change e.g. modules/vpc/README.md
git commit -am "test: trigger CI"
git push -u origin week-04-ci
```

5. **Verify** GitHub Actions: `validate` and `security` jobs; `plan` job (may use `-backend=false` until OIDC complete).

### Success criteria

- [ ] Workflow file in `.github/workflows/`
- [ ] PR shows green or explainable yellow (`soft_fail`) jobs
- [ ] Link to CI run submitted

### Common issues

| Symptom | Resolution |
|---------|------------|
| Workflow not triggered | Check `paths` filter; edit under `modules/` or `labs/shared/` |
| `id-token: write` missing | Add permissions block |
| Plan fails init | Use `-backend=false` for validate-only phase per template |

---

## Lab 4.2 — Plan → Review → Apply Gates

**Duration:** 2 hours · **Guide:** [labs/week-04/LAB-02-approval-gates.md](../../labs/week-04/LAB-02-approval-gates.md)

### Objectives

- Configure GitHub Environments `dev` and `prod`
- Separate plan (PR) from apply (`main` + approval)
- Reinforce OIDC over static secrets

### Detailed procedure

1. **Create environments** in GitHub: Settings → Environments → `dev`, `prod`
   - Required reviewers: 1 (lab) / 2 (prod discussion)
   - Deployment branches: restrict `prod` to `main`
2. **Enable apply job** in workflow (uncomment per template):

```yaml
environment: dev
```

3. **Configure secrets:**
   - `AWS_ROLE_ARN` for plan/apply role
   - Separate ARNs per environment if stretch goal
4. **Merge test PR** to `main` (or instructor simulates) and observe apply waiting for approval.
5. **Screenshot** approval gate before apply (redact names if needed).

### Success criteria

- [ ] Environments exist with protection rules documented
- [ ] Apply does not run without approval
- [ ] Written policy: who approves prod (2–4 sentences)

### Common issues

| Symptom | Resolution |
|---------|------------|
| Apply runs on PR | Check `if: github.ref == 'refs/heads/main'` |
| Approval not required | Environment not referenced in job |

---

## Lab 4.3 — Infrastructure Validation

**Duration:** 2 hours · **Guide:** [labs/week-04/LAB-03-validation.md](../../labs/week-04/LAB-03-validation.md)

### Objectives

- Run `tflint` and `checkov` locally and in CI
- Fix or document findings in remediation log

### Detailed procedure

1. **Local scans:**

```bash
cd modules/vpc
tflint --init && tflint
checkov -d . --framework terraform
```

2. **Review CI `security` job** in [`labs/week-04/workflows/terraform-ci.yml`](../../labs/week-04/workflows/terraform-ci.yml).
3. **Create** `docs/security/week-04-ci-findings.md`:

| Check ID | Severity | Resource | Action |
|----------|----------|----------|--------|
| ... | HIGH | ... | fixed / accepted risk #ticket |

4. **Remediate** at least one HIGH finding or document compensating control.
5. **Re-run** CI on PR; confirm improvement or justified `soft_fail`.

### Success criteria

- [ ] Findings document with ≥ 3 entries
- [ ] At least one fix merged
- [ ] CI link showing security job outcome

---

## Lab submission

Submit:

1. URL to green (or justified) PR workflow run
2. Screenshot of environment approval gate
3. `docs/security/week-04-ci-findings.md`
4. Pipeline diagram (Mermaid): PR → plan → merge → apply

---

## Cost control

OIDC plans may refresh AWS APIs. After testing:

```bash
make lab-stop
```

Resources must include `Course=terraform-enterprise`.
