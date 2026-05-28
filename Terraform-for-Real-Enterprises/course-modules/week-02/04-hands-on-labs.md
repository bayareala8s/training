# Week 2 — Hands-On Labs (Detailed)

**Total lab time:** ~5–6 hours · **Repository paths:** [`labs/week-02/`](../../labs/week-02/)

---

## Lab 2.1 — Multi-Account Architecture Design

**Duration:** 2 hours · **Guide:** [labs/week-02/LAB-01-organizations.md](../../labs/week-02/LAB-01-organizations.md)

### Objectives

- Document an OU/account model for dev, test, prod, and shared services
- Map Terraform state files to account boundaries
- Relate Week 1 bootstrap bucket to a production “state account” pattern

### Detailed procedure

1. **Study reference architecture** in the lab guide (Security OU, Infrastructure OU, Workloads OU).
2. **Create** `docs/architecture/week-02-accounts.md` in your fork with Mermaid or draw.io diagram showing:
   - GitHub Actions / tooling → Shared Services → workload accounts
   - State backend location (account + S3 key per environment)
3. **Complete account matrix** with columns: Account name, Account ID (placeholder if single-account), Purpose, State backend key.
4. **Single-account lab mode:** If you have one AWS account, document logical separation using state keys (`environments/dev`, etc.) and list **residual risks**.

### Verification checklist

- [ ] Diagram includes at least 4 logical accounts (or explicit single-account caveat)
- [ ] Matrix maps each environment to a state key
- [ ] Narrative paragraph explains who runs Terraform in each account

### Success criteria

- [ ] File committed or submitted per instructor instructions
- [ ] Peer can understand blast radius from diagram alone

### Common issues

| Symptom | Resolution |
|---------|------------|
| “I don’t have Organizations access” | Use placeholder IDs; label as design-only |
| State in every account vs central | Pick one pattern; justify in README |

---

## Lab 2.2 — Cross-Account IAM Roles

**Duration:** 2–3 hours · **Guide:** [labs/week-02/LAB-02-cross-account-iam.md](../../labs/week-02/LAB-02-cross-account-iam.md)

### Objectives

- Create trust policy for Terraform runner role
- Scope permissions with least privilege
- Configure or document provider `assume_role`

### Detailed procedure

1. **Review templates:**
   - [`labs/week-02/iam/terraform-runner-trust.json`](../../labs/week-02/iam/terraform-runner-trust.json)
   - [`labs/week-02/iam/terraform-runner-policy.json`](../../labs/week-02/iam/terraform-runner-policy.json)
2. **Update trust policy** with your tooling account ID, or future GitHub OIDC role ARN (comment placeholder for Week 4).
3. **Create role** `bal8s-terraform-runner`:

```bash
cd labs/week-02
aws iam create-role \
  --role-name bal8s-terraform-runner \
  --assume-role-policy-document file://iam/terraform-runner-trust.json
```

4. **Attach inline policy** from `terraform-runner-policy.json`.
5. **Test assume role:**

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::WORKLOAD_ACCOUNT:role/bal8s-terraform-runner \
  --role-session-name lab-test
```

6. **Optional:** Add provider alias with `assume_role` in `labs/shared/environments/dev/main.tf` per lab guide.

### Success criteria

- [ ] Role exists with trust + scoped policy (or documented blocker if org admin required)
- [ ] Redacted `sts assume-role` output saved for submission
- [ ] Written answer: why root principal in trust is discouraged in production (3 sentences)

### Common issues

| Symptom | Resolution |
|---------|------------|
| `AccessDenied` on create-role | Use personal lab account or instructor-provided sandbox |
| Trust policy JSON error | Validate with `aws iam simulate-custom-policy` or json lint |

---

## Lab 2.3 — Cross-Account Terraform Apply

**Duration:** 2 hours · **Guide:** [labs/week-02/LAB-03-cross-account-apply.md](../../labs/week-02/LAB-03-cross-account-apply.md)

### Objectives

- Run `terraform plan` using assumed role credentials
- Document session naming and External ID pattern
- Preview how Week 4 CI replaces manual credential export

### Detailed procedure

1. **Export temporary credentials** from successful assume-role (see lab guide for `CREDS` one-liner).
2. **Run plan** from course root:

```bash
make plan ENV=dev
```

3. **Verify** plan completes without provider auth errors; capture redacted plan summary (resource counts).
4. **Update fork README** (or architecture doc) with workflow section:
   - Who can assume the role
   - External ID value (if used)
   - Session naming convention
   - Diagram update showing CI path (placeholder for Week 4)

### Cost control

After lab:

```bash
make lab-stop
```

Requires `Course=terraform-enterprise` tag on stoppable resources.

### Success criteria

- [ ] `terraform plan` succeeded with assumed-role session
- [ ] Documentation links trust policy → provider → plan
- [ ] No long-lived access keys committed to Git

### Common issues

| Symptom | Resolution |
|---------|------------|
| `ExpiredToken` | Re-run assume-role; sessions are short-lived |
| Plan shows unexpected destroy | Do not apply; compare state backend profile vs assumed role account |

---

## Lab submission

Submit PR or document bundle:

1. `docs/architecture/week-02-accounts.md` (diagram + matrix)
2. Redacted assume-role output
3. Redacted plan summary (first/last 20 lines)
4. IAM workflow narrative (200–400 words)
