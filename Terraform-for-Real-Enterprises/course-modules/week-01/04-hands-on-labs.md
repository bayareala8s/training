# Week 1 — Hands-On Labs (Detailed)

**Total lab time:** ~4 hours · **Repository paths:** [`labs/week-01/`](../../labs/week-01/)

---

## Lab 1.1 — Install Terraform & Toolchain

**Duration:** 60–90 min · **Guide:** [labs/week-01/LAB-01-install.md](../../labs/week-01/LAB-01-install.md)

### Objectives

Install and verify Terraform ≥ 1.5, AWS CLI v2, Git; configure AWS credentials.

### Detailed procedure

1. **Install Terraform** using HashiCorp tap (macOS) or apt (Linux).
2. Pin version with `.terraform-version` in repo root (`1.7.5`).
3. **Install AWS CLI v2** and run `aws sts get-caller-identity`.
4. Configure **AWS SSO** or named profile `bal8s-lab`.
5. Optional: `tflint`, `checkov`, `jq` for later weeks.

### Verification checklist

```bash
terraform version          # >= 1.5.0
aws --version              # aws-cli/2.x
aws sts get-caller-identity
git --version
```

### Success criteria

- [ ] Correct AWS account ID displayed
- [ ] Region documented in student notes (default `us-west-2`)

### Common issues

| Symptom | Resolution |
|---------|------------|
| `ExpiredToken` | `aws sso login` |
| Wrong account | Check `AWS_PROFILE` |

---

## Lab 1.2 — Configure AWS Provider

**Duration:** 60 min · **Guide:** [labs/week-01/LAB-02-provider.md](../../labs/week-01/LAB-02-provider.md)

### Objectives

Practice provider blocks, version constraints, `default_tags`, and a minimal apply/destroy cycle.

### Concepts reinforced

- `required_providers` pinning
- Tagging strategy for course automation (`Course=terraform-enterprise`)
- Plan output interpretation

### Success criteria

- [ ] Successful `terraform apply` and `terraform destroy` in practice directory
- [ ] Written answer: benefits of `default_tags` (3 sentences minimum)

---

## Lab 1.3 — Secure Remote State Backend

**Duration:** 2–3 hours · **Guide:** [labs/week-01/LAB-03-backend.md](../../labs/week-01/LAB-03-backend.md)

### Objectives

Bootstrap S3 + DynamoDB; configure dev environment remote backend; deploy baseline infrastructure.

### Step-by-step (summary)

#### Part A — Bootstrap

```bash
cd labs/week-01/bootstrap
cp terraform.tfvars.example terraform.tfvars
# Set globally unique state_bucket_name and student_id
terraform init
terraform apply
```

Record outputs: bucket, DynamoDB table, backend snippet.

#### Part B — Configure dev backend

```bash
cd ../../shared/environments/dev
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
# Edit backend.hcl with your bucket/table
```

#### Part C — Deploy dev

From course root:

```bash
make init ENV=dev
make plan ENV=dev
make apply ENV=dev
```

#### Part D — Cost control exercise

```bash
make lab-stop
make lab-status
make lab-start
```

### Resources created

- VPC (public/private subnets)
- NAT instance (stoppable—see `scripts/aws/`)
- Optional lab EC2 instance
- VPC flow logs → CloudWatch

### Success criteria

- [ ] `aws s3 ls s3://YOUR-BUCKET/environments/dev/` shows state file
- [ ] `terraform state list` shows module resources
- [ ] All resources tagged `Course=terraform-enterprise`
- [ ] No `.tfvars` or secrets in Git

### Cleanup policy

- **End of day:** `make lab-stop`
- **End of course week:** keep infra for Week 2; do not destroy bootstrap bucket

---

## Lab submission

Submit PR or document:

1. Screenshot: `aws sts get-caller-identity`
2. Redacted: `terraform state list`
3. Backend architecture paragraph (5–8 sentences)
