# Student Onboarding

**Course:** Terraform for Real Enterprises · **BayAreaLa8s**

Complete this checklist before Week 1 Lab 1.3.

---

## 1. Clone the repository

**Monorepo (published):**

```bash
git clone https://github.com/bayareala8s/training.git
cd training/Terraform-for-Real-Enterprises
```

**Standalone clone:** use the course root as your working directory.

Verify:

```bash
ls labs/week-01 labs/shared/environments/dev modules/vpc
```

---

## 2. Install tools

| Tool | Minimum version | Verify |
|------|-----------------|--------|
| Terraform | 1.5.0 | `terraform version` |
| AWS CLI | v2 | `aws --version` |
| Git | any recent | `git --version` |

**Optional (Week 4+):** `tflint`, `checkov`, `jq`

Details: [labs/week-01/LAB-01-install.md](../labs/week-01/LAB-01-install.md)

---

## 3. Configure AWS access

```bash
aws configure sso          # or aws configure --profile your-lab
export AWS_PROFILE=your-lab
export AWS_REGION=us-west-2
aws sts get-caller-identity
```

Save your **Account ID** and **region** for lab deliverables.

---

## 4. Provider install workaround (if needed)

If `terraform init` fails with registry errors:

```bash
./scripts/aws/install-provider.sh 5.90.0
export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc
```

---

## 5. Local config files (never commit)

```bash
cp labs/shared/environments/dev/backend.hcl.example labs/shared/environments/dev/backend.hcl
cp labs/shared/environments/dev/terraform.tfvars.example labs/shared/environments/dev/terraform.tfvars
```

Edit `terraform.tfvars` — set `owner` to your name or team id.

Repeat for `test` and `prod` when you reach Week 5.

---

## 6. Cost expectations

| Action | When |
|--------|------|
| `make lab-resume` | Start of each lab session |
| `make lab-pause` | End of session (**recommended** — near-zero cost) |
| `make lab-stop` | Stops EC2 only; prod NAT Gateway still bills |

NAT Gateway in prod costs ~**$0.045/hour** while provisioned. Use `make lab-pause` between sessions.

---

## 7. Lab map and demos

- Lab guides: [labs/README.md](../labs/README.md)
- Full run guide: [docs/LAB-DEMO-GUIDE.md](LAB-DEMO-GUIDE.md)
- Student workbook: [course-modules/STUDENT-WORKBOOK.md](../course-modules/STUDENT-WORKBOOK.md)

---

## 8. GitHub (Week 4)

Fork or branch `bayareala8s/training` for CI labs. Workflow path:

`Terraform-for-Real-Enterprises/.github/workflows/terraform-ci.yml`

---

## 9. Getting help

| Issue | Fix |
|-------|-----|
| `ExpiredToken` | `aws sso login` |
| Lock error on apply | Wait or check DynamoDB `terraform-locks` |
| Wrong directory | Must be course root (`Terraform-for-Real-Enterprises/`) |
| High AWS bill | `make lab-pause` and verify with `make lab-status` |

---

## Next step

[Week 1 Lab 1.3 — Remote state](../labs/week-01/LAB-03-backend.md)
