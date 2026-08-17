# Lab Demo & Run Guide — Step by Step

**Course:** Terraform for Real Enterprises · **BayAreaLa8s**

This guide is for **instructors** demoing live and **students** running labs independently. Work in order; later weeks assume Week 1 infrastructure is in place.

---

## Current lab status

Run before each cohort to refresh this section:

```bash
make lab-status
aws ec2 describe-vpcs --region us-west-2 \
  --filters Name=tag:Course,Values=terraform-enterprise \
  --query 'Vpcs[].[Tags[?Key==`Environment`].Value|[0],VpcId,CidrBlock]' --output table
```

| Environment | Default CIDR | NAT pattern |
|-------------|--------------|-------------|
| dev | `10.10.0.0/16` | NAT instance (stoppable) |
| test | `10.20.0.0/16` | NAT instance (stoppable) |
| prod | `10.30.0.0/16` | NAT Gateway (destroy on `make lab-pause`) |

| Check | How to verify |
|-------|----------------|
| Terraform validate | `make validate` |
| Cost pause | `make lab-pause` / `make lab-resume` |
| GitHub CI | https://github.com/bayareala8s/training/actions |
| OIDC secret | [GITHUB-SECRET-AWS_ROLE_ARN.md](GITHUB-SECRET-AWS_ROLE_ARN.md) |

### Pre-demo (start of every session)

```bash
# Monorepo: cd training/Terraform-for-Real-Enterprises
# Standalone: cd into course repo root
export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc   # if registry blocked
make lab-resume && make lab-status
```

### End of session (save cost)

```bash
make lab-pause
```

---

## All 22 labs — at-a-glance

| Lab | Week | Type | Infrastructure needed | Ready? |
|-----|------|------|----------------------|--------|
| 1.1 Install | 1 | Local | None | ✅ |
| 1.2 Provider | 1 | Local | Optional S3 bucket | ✅ |
| 1.3 Backend | 1 | AWS | dev stack | ✅ deployed |
| 2.1 Organizations | 2 | Design | Docs only | ✅ |
| 2.2 Cross-account IAM | 2 | IAM | Role create or document | ✅ |
| 2.3 Cross-account apply | 2 | AWS | dev plan | ✅ |
| 3.1 VPC module | 3 | Code | dev plan | ✅ |
| 3.2 Compose modules | 3 | Code | validate all envs | ✅ |
| 3.3 Publish module | 3 | Git | tag + CHANGELOG | ✅ |
| 4.1 GitHub Actions | 4 | GitHub | workflow on `training` | ✅ workflow live |
| 4.2 Approval gates | 4 | GitHub | Environments + secret | ⚠️ add `AWS_ROLE_ARN` secret |
| 4.3 Validation | 4 | Local/CI | tflint + checkov | ✅ |
| 5.1 Promotion | 5 | AWS | dev + test + prod | ✅ all three deployed |
| 5.2 Drift | 5 | AWS | dev running | ✅ |
| 5.3 Remediate | 5 | AWS | dev apply | ✅ |
| 6.1 Failed deploy | 6 | AWS | dev (break/fix) | ✅ |
| 6.2 State recovery | 6 | State | S3 state versions | ✅ |
| 6.3 Rollback | 6 | Git | rollback-plan.sh | ✅ |
| 7.1 IAM least privilege | 7 | IAM | policy JSON | ✅ |
| 7.2 Tagging | 7 | AWS | tagged instances | ✅ |
| 7.3 Compliance | 7 | Checkov | modules + labs | ✅ |
| 8 Capstone | 8 | Full | student project | ✅ rubric ready |

---

## Verification status (automated smoke test)

| Check | Result | Notes |
|-------|--------|-------|
| `terraform validate` (dev, test, prod) | **Pass** | All three environment configs valid |
| Dev / test / prod `apply` | **Pass** | 23 resources each in remote state |
| `start-lab.sh` / `stop-lab.sh` | **Pass** | EC2 stop → start cycle verified |
| Week 4 GitHub Actions | **Live** | OIDC role created; secret required for plan job |
| Week 2 multi-account | **Design lab** | Single-account mode with isolated state keys |

**Account:** `277374794397` · **Region:** `us-west-2`

---

## Part 0 — One-time setup (everyone)

### 0.1 Tools

```bash
terraform version          # >= 1.5.0
aws --version              # AWS CLI v2
aws sts get-caller-identity
git --version
```

Optional: `tflint`, `checkov`, `jq`

### 0.2 AWS credentials

```bash
export AWS_PROFILE=your-lab-profile   # or SSO login
export AWS_REGION=us-west-2
```

### 0.3 Clone the course repo

```bash
git clone git@github.com:bayareala8s/training.git
cd training/Terraform-for-Real-Enterprises
```

### 0.4 Provider registry workaround (if `terraform init` fails)

Some networks block the Terraform registry. Use the course installer:

```bash
./scripts/aws/install-provider.sh 5.90.0
export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc
```

### 0.5 Never commit secrets

```bash
# These files are gitignored — create from examples only
cp labs/shared/environments/dev/backend.hcl.example labs/shared/environments/dev/backend.hcl
cp labs/shared/environments/dev/terraform.tfvars.example labs/shared/environments/dev/terraform.tfvars
# Edit owner, bucket, region as needed
```

---

## Part 1 — Instructor quick smoke test

Run before each cohort to confirm AWS + Terraform still work:

```bash
cd Terraform-for-Real-Enterprises
export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc   # if needed

./scripts/aws/verify-labs.sh all
```

This runs: validate all envs → apply dev → stop/start EC2 → destroy dev.

**Keep dev running for demos** instead of full teardown:

```bash
./scripts/aws/verify-labs.sh validate
./scripts/aws/verify-labs.sh apply
./scripts/aws/verify-labs.sh test
# Skip teardown until cohort ends
```

**End of day cost control:**

```bash
make lab-stop
```

**End of course:**

```bash
make lab-teardown    # or: ./scripts/aws/teardown-all.sh
```

---

## Part 2 — Week-by-week labs

### Legend

| Type | Meaning |
|------|---------|
| **Local** | No AWS deploy; toolchain or docs only |
| **AWS** | Creates or changes AWS resources |
| **GitHub** | Needs a GitHub repository |
| **Design** | Architecture documentation |

---

## Week 1 — Foundations

**Shared stack path:** `labs/shared/environments/dev/` · **Bootstrap:** `labs/week-01/bootstrap/`

### Lab 1.1 — Install Terraform & Toolchain

| | |
|---|---|
| **Type** | Local |
| **Duration** | 60–90 min |
| **Guide** | [labs/week-01/LAB-01-install.md](../labs/week-01/LAB-01-install.md) |

**Student steps:**

1. Install Terraform, AWS CLI, Git (see lab for OS-specific commands).
2. Run `terraform version` and `aws sts get-caller-identity`.
3. Configure SSO or named profile; set `AWS_PROFILE`.

**Instructor demo (5 min):**

1. Show your terminal with version output.
2. Explain why enterprises pin Terraform and use SSO instead of long-lived keys.
3. Show `ExpiredToken` fix: `aws sso login`.

**Deliverable:** Screenshot of versions + account ID.

---

### Lab 1.2 — Configure AWS Provider

| | |
|---|---|
| **Type** | Local (optional tiny S3 bucket) |
| **Duration** | 60 min |
| **Guide** | [labs/week-01/LAB-02-provider.md](../labs/week-01/LAB-02-provider.md) |

**Student steps:**

1. Create `~/tf-lab-practice/` with `versions.tf` and minimal `main.tf` (S3 marker bucket).
2. `terraform init && terraform plan && terraform apply && terraform destroy`.

**Instructor demo (10 min):**

1. Walk through `default_tags` on the provider block.
2. Run `terraform plan` — point out tag inheritance on every resource.
3. Destroy the practice bucket before moving on.

**Talking point:** `default_tags` is how enterprises enforce cost allocation without repeating tags on 500 resources.

---

### Lab 1.3 — Secure Remote State Backend

| | |
|---|---|
| **Type** | **AWS** (bootstrap + full dev stack) |
| **Duration** | 2–3 hours |
| **Guide** | [labs/week-01/LAB-03-backend.md](../labs/week-01/LAB-03-backend.md) |

**Option A — Use org shared state (this course default):**

`backend.hcl` already points at `bayareala8s-terraform-state` with key `terraform-enterprise/environments/dev/terraform.tfstate`.

**Option B — Student-owned bootstrap:**

```bash
cd labs/week-01/bootstrap
cp terraform.tfvars.example terraform.tfvars
# Edit student_id and unique state_bucket_name
terraform init && terraform apply
```

**Deploy dev environment:**

```bash
cd labs/shared/environments/dev
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
# Edit owner in terraform.tfvars

cd ../../../..   # repo root
make init ENV=dev
make plan ENV=dev
make apply ENV=dev
```

**Verify (expected output):**

```bash
terraform output
# vpc_id = "vpc-..."
# lab_instance_id = "i-..."
```

**What gets deployed (20 resources):**

- VPC `10.10.0.0/16`, 2 public + 2 private subnets, IGW
- NAT **instance** (not NAT Gateway — cheaper for labs)
- Lab EC2 in private subnet (`bal8s-tf-dev-lab-host`)
- VPC flow logs → CloudWatch

**Instructor demo (20 min):**

1. `aws ec2 describe-vpcs --filters Name=tag:Course,Values=terraform-enterprise`
2. Console: VPC → show subnets, route tables (private → NAT instance).
3. `terraform state list` — tie resources to modules.
4. `aws s3 ls s3://YOUR-BUCKET/terraform-enterprise/environments/dev/`
5. Demo cost control:

```bash
make lab-stop && make lab-status
make lab-start && make lab-status
```

**Deliverable:** Remote state working + `terraform state list` (redact account if needed).

---

## Week 2 — Multi-account architecture

**Path:** `labs/week-02/` · IAM templates in `labs/week-02/iam/`

### Lab 2.1 — Multi-Account Architecture Design

| | |
|---|---|
| **Type** | Design |
| **Duration** | 2 hours |
| **Guide** | [labs/week-02/LAB-01-organizations.md](../labs/week-02/LAB-01-organizations.md) |

**Student steps:**

1. Draw OU model: Security, Infrastructure, Workloads (dev/test/prod).
2. Create `docs/architecture/week-02-accounts.md` with Mermaid diagram.
3. Fill account matrix (ID, purpose, state key per account).

**Single-account mode:** Document logical separation via different state keys (`environments/dev`, `test`, `prod`) — same pattern as this repo.

**Instructor demo (15 min):**

1. Show diagram from `diagrams/png/00-multi-account-summary.png`.
2. Explain why prod should not share an account with dev sandboxes.
3. Walk through state key isolation in S3 prefix layout.

---

### Lab 2.2 — Cross-Account IAM Roles

| | |
|---|---|
| **Type** | AWS IAM (or documented) |
| **Duration** | 2–3 hours |
| **Guide** | [labs/week-02/LAB-02-cross-account-iam.md](../labs/week-02/LAB-02-cross-account-iam.md) |

**Student steps:**

1. Review `iam/terraform-runner-trust.json` and `iam/terraform-runner-policy.json`.
2. Create role `bal8s-terraform-runner` (update trust policy with your account/OIDC ARN).
3. Test:

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::ACCOUNT_ID:role/bal8s-terraform-runner \
  --role-session-name lab-test
```

**Instructor demo (15 min):**

1. Whiteboard: tooling account → `AssumeRole` → workload account.
2. Show trust policy `Principal` and `Condition` blocks.
3. Contrast with Week 4 OIDC (no static keys in GitHub).

---

### Lab 2.3 — Cross-Account Terraform Apply

| | |
|---|---|
| **Type** | AWS (plan with assumed role) |
| **Duration** | 2 hours |
| **Guide** | [labs/week-02/LAB-03-cross-account-apply.md](../labs/week-02/LAB-03-cross-account-apply.md) |

**Student steps:**

1. Export temporary credentials from `sts assume-role` (see lab).
2. `make plan ENV=dev` — confirm plan succeeds under assumed role.
3. Document workflow in personal README.

**Instructor demo (10 min):**

1. Show plan output with session credentials (no long-lived keys in shell history long-term).
2. Preview Week 4: CI replaces manual export.

---

## Week 3 — Modules

**Modules:** `modules/vpc/`, `modules/compute/`

### Lab 3.1 — Build & Extend VPC Module

| | |
|---|---|
| **Type** | Code + plan |
| **Duration** | 3 hours |
| **Guide** | [labs/week-03/LAB-01-vpc-module.md](../labs/week-03/LAB-01-vpc-module.md) |

**Student steps:**

1. Read `modules/vpc/main.tf`, `variables.tf`, `outputs.tf`.
2. `make plan ENV=dev` — no changes expected if stack is current.
3. Add enhancement (S3 VPC endpoint OR database subnet tier).
4. Tag module `v1.0.0`.

**Instructor demo (20 min):**

1. Trace `module.vpc` call in `labs/shared/environments/dev/main.tf`.
2. Show NAT instance vs NAT Gateway variables (`use_nat_instance`, `enable_nat_gateway`).
3. Live: add optional input, run `terraform plan` — show only targeted changes.

---

### Lab 3.2 — Compose Networking Modules

| | |
|---|---|
| **Type** | Code + validate |
| **Duration** | 2 hours |
| **Guide** | [labs/week-03/LAB-02-compose.md](../labs/week-03/LAB-02-compose.md) |

**Student steps:**

1. Trace: `module.vpc.private_subnet_ids[0]` → `module.compute.subnet_id`.
2. `make validate` — all three environments must pass.

**Instructor demo (10 min):**

1. Draw data flow: VPC outputs → compute inputs.
2. Run `make validate` live; explain dev vs test vs prod tfvars differences.

---

### Lab 3.3 — Publish Internal Module

| | |
|---|---|
| **Type** | Git / process |
| **Duration** | 1–2 hours |
| **Guide** | [labs/week-03/LAB-03-publish.md](../labs/week-03/LAB-03-publish.md) |

**Student steps:**

1. Add `modules/vpc/CHANGELOG.md`.
2. Tag release; document `git::` source vs local path.

**Instructor demo (10 min):**

1. Show semantic versioning policy (PATCH / MINOR / MAJOR).
2. Demo consumer upgrade: change `ref=v1.0.0` → `ref=v1.1.0` in module source.

---

## Week 4 — CI/CD

**Workflow (live):** `Terraform-for-Real-Enterprises/.github/workflows/terraform-ci.yml` on `bayareala8s/training`  
**OIDC role:** `arn:aws:iam::277374794397:role/github-terraform`  
**Secret setup:** [GITHUB-SECRET-AWS_ROLE_ARN.md](GITHUB-SECRET-AWS_ROLE_ARN.md)

### Lab 4.1 — GitHub Actions Terraform CI

| | |
|---|---|
| **Type** | **GitHub** |
| **Duration** | 3 hours |
| **Guide** | [labs/week-04/LAB-01-github-actions.md](../labs/week-04/LAB-01-github-actions.md) |

**One-time setup (instructor):**

1. OIDC already created via `scripts/github/setup-oidc.sh`
2. Add GitHub secret `AWS_ROLE_ARN` = `arn:aws:iam::277374794397:role/github-terraform`
3. Workflow already on `main` — jobs: `validate` (matrix), `security`, `plan-dev`

**Student steps:**

1. Fork `bayareala8s/training` or work in monorepo path `Terraform-for-Real-Enterprises/`
2. Branch `week-04-ci`, edit e.g. `modules/vpc/README.md`, open PR
3. Watch Actions tab — all jobs should pass after secret is set

**Instructor demo (20 min):**

1. Open https://github.com/bayareala8s/training/actions — show **Terraform CI** workflow
2. Walk through `validate` matrix (dev, test, prod)
3. Show `security` (Checkov) and `plan-dev` (live plan vs dev remote state)
4. Explain `paths:` filter and `TF_COURSE_ROOT` for monorepo layout

**Without secret:** `plan-dev` fails on OIDC step — add secret first.

---

### Lab 4.2 — Plan → Review → Apply

| | |
|---|---|
| **Type** | GitHub Environments |
| **Duration** | 2 hours |
| **Guide** | [labs/week-04/LAB-02-approval-gates.md](../labs/week-04/LAB-02-approval-gates.md) |

**Student steps:**

1. Create GitHub Environments `dev` and `prod` with required reviewers.
2. Uncomment `apply` job with `environment: dev`.
3. Merge to `main` → approval gate → apply.

**Instructor demo (15 min):**

1. Screenshot: "Review deployments" waiting for approver.
2. Emphasize: prod branch protection + environment rules = change control.

---

### Lab 4.3 — Infrastructure Validation

| | |
|---|---|
| **Type** | Local + CI |
| **Duration** | 2 hours |
| **Guide** | [labs/week-04/LAB-03-validation.md](../labs/week-04/LAB-03-validation.md) |

**Student steps:**

```bash
cd modules/vpc
tflint --init && tflint
checkov -d . --framework terraform
```

Create `docs/security/week-04-ci-findings.md` with remediation table.

**Instructor demo (10 min):**

1. Run Checkov live; pick one finding and show fix or documented exception.

---

## Week 5 — Promotion & drift

**Requires dev stack running.** Test and prod stacks already deployed for promotion demos.

### Lab 5.1 — Environment Promotion

| | |
|---|---|
| **Type** | **AWS** (test + prod) |
| **Duration** | 2–3 hours |
| **Guide** | [labs/week-05/LAB-01-promotion.md](../labs/week-05/LAB-01-promotion.md) |

**Already deployed (instructor demo — no apply needed):**

| Env | VPC | CIDR | NAT |
|-----|-----|------|-----|
| dev | `vpc-06c28fd07c8a86c16` | `10.10.0.0/16` | NAT instance |
| test | `vpc-03181c22f1a945073` | `10.20.0.0/16` | NAT instance |
| prod | `vpc-008d013a3d5cfd084` | `10.30.0.0/16` | NAT Gateway |

**Student steps (if starting fresh):**

```bash
# Repeat for test and prod with respective backend.hcl + terraform.tfvars
make init ENV=test && make apply ENV=test
make init ENV=prod && make apply ENV=prod
```

**Promotion checklist** in `docs/runbooks/environment-promotion.md`.

**Instructor demo (20 min):**

1. AWS Console → VPC → filter tag `Course=terraform-enterprise` — show **three VPCs**
2. Compare `labs/shared/environments/{dev,test,prod}/terraform.tfvars.example`
3. `make plan ENV=test` — show no changes (stable promotion target)
4. Walk promotion runbook: PR → plan test → apply test → plan prod → change window → apply prod

---

### Lab 5.2 — Simulate Infrastructure Drift

| | |
|---|---|
| **Type** | AWS + plan |
| **Duration** | 2 hours |
| **Guide** | [labs/week-05/LAB-02-drift.md](../labs/week-05/LAB-02-drift.md) |

**Student steps:**

1. Ensure dev applied: `make apply ENV=dev`
2. **Console drift:** add security group rule OR change unmanaged tag OR stop instance manually.
3. `make plan ENV=dev` — capture diff in `docs/drift-report-week05.md`.

**Instructor demo (15 min):**

1. Live console: add ingress rule on lab security group.
2. `terraform plan` — show Terraform wants to revert.
3. Discuss: drift = reality vs desired state.

---

### Lab 5.3 — Remediate Drift

| | |
|---|---|
| **Type** | AWS apply |
| **Duration** | 1–2 hours |
| **Guide** | [labs/week-05/LAB-03-remediate.md](../labs/week-05/LAB-03-remediate.md) |

**Remediation matrix:**

| Situation | Action |
|-----------|--------|
| Console change wrong | `terraform apply` reverts |
| Console change correct | Update `.tf`, then apply |
| Resource not in state | `terraform import` |
| Stale state | careful `refresh` / plan |

**Instructor demo (10 min):**

1. Apply revert — show SG rule removed.
2. Mention nightly scheduled plan as stretch goal.

---

## Week 6 — Recovery & rollback

**Uses dev stack + S3 state versioning.**

### Lab 6.1 — Simulate Failed Deployment

| | |
|---|---|
| **Type** | AWS (intentional failure) |
| **Duration** | 2 hours |
| **Guide** | [labs/week-06/LAB-01-failed-deploy.md](../labs/week-06/LAB-01-failed-deploy.md) |

**Student steps:**

1. Add bad `aws_instance` with `ami-invalid` to dev `main.tf`.
2. `make apply ENV=dev` — observe error / partial state.
3. Remove bad resource; `terraform plan`.

**Instructor demo (15 min):**

1. Show failed apply output.
2. `terraform state list` — what landed in state vs AWS.
3. Never panic-delete in console without checking state.

---

### Lab 6.2 — Terraform State Recovery

| | |
|---|---|
| **Type** | State ops |
| **Duration** | 2–3 hours |
| **Guide** | [labs/week-06/LAB-02-state-recovery.md](../labs/week-06/LAB-02-state-recovery.md) |

**Student steps:**

```bash
cd labs/shared/environments/dev
terraform state list
terraform state show 'module.vpc.aws_vpc.this'
terraform state pull > /tmp/state-backup-$(date +%Y%m%d).json

aws s3api list-object-versions \
  --bucket bayareala8s-terraform-state \
  --prefix terraform-enterprise/environments/dev/terraform.tfstate
```

Update `docs/runbooks/terraform-recovery.md`.

**Instructor demo (15 min):**

1. S3 console: state file versions.
2. `terraform untaint` if resource was tainted.

---

### Lab 6.3 — Rollback Automation Workflow

| | |
|---|---|
| **Type** | Git + script |
| **Duration** | 2 hours |
| **Guide** | [labs/week-06/LAB-03-rollback.md](../labs/week-06/LAB-03-rollback.md) |

**Student steps:**

```bash
git revert HEAD --no-edit
./scripts/terraform/rollback-plan.sh --env dev --ref HEAD~1
```

Complete recovery runbook.

**Instructor demo (10 min):**

1. Git revert → CI plan → approved apply = infrastructure rollback.
2. Dry-run rollback script output.

---

## Week 7 — Security & governance

### Lab 7.1 — IAM Least Privilege

| | |
|---|---|
| **Type** | IAM policy edit |
| **Duration** | 2 hours |
| **Guide** | [labs/week-07/LAB-01-iam.md](../labs/week-07/LAB-01-iam.md) |

**Student steps:**

1. Audit `labs/week-02/iam/terraform-runner-policy.json`.
2. Replace `ec2:*` with scoped actions.
3. Optional: IAM Access Analyzer.

**Instructor demo (10 min):**

1. Compare wildcard vs scoped policy side by side.

---

### Lab 7.2 — Tagging Policies

| | |
|---|---|
| **Type** | Code + AWS verify |
| **Duration** | 1–2 hours |
| **Guide** | [labs/week-07/LAB-02-tagging.md](../labs/week-07/LAB-02-tagging.md) |

**Required tags:** `Course`, `Project`, `ManagedBy`, `Environment`, `Owner`

**Verify:**

```bash
aws ec2 describe-instances \
  --filters "Name=tag:Course,Values=terraform-enterprise" \
  --query 'Reservations[].Instances[].Tags' --output table
```

**Instructor demo (10 min):**

1. Show tags on lab instances — tie to `make lab-stop` filter.
2. Variable validation block in `variables.tf`.

---

### Lab 7.3 — Compliance Checks in CI

| | |
|---|---|
| **Type** | Checkov |
| **Duration** | 2–3 hours |
| **Guide** | [labs/week-07/LAB-03-compliance.md](../labs/week-07/LAB-03-compliance.md) |

**Student steps:**

```bash
checkov -d modules/ -d labs/shared/ --framework terraform -o cli
checkov -d modules/ -d labs/shared/ --framework terraform -o json > /tmp/checkov.json
```

Configure `labs/week-07/.checkov.yml` skip-check with documented exceptions.

Create `docs/security/week-07-validation-report.md`.

**Instructor demo (15 min):**

1. Full report walkthrough: pass/fail, remediated vs accepted risk.

---

## Week 8 — Capstone

| | |
|---|---|
| **Type** | Full integration |
| **Duration** | 10–12 hours |
| **Guide** | [labs/week-08/LAB-capstone.md](../labs/week-08/LAB-capstone.md) · [capstone/README.md](../capstone/README.md) |

**Required demonstrations:**

- Remote state (S3 + DynamoDB)
- Reusable modules
- CI/CD (GitHub Actions)
- dev → test or prod promotion
- Security report (Week 7 template)
- Cost estimate
- `make lab-stop` in operations section

**Presentation flow (15–20 min):**

1. Business problem (2 min)
2. Architecture diagram (5 min)
3. Live: PR → plan → apply (5 min)
4. Security & cost (3 min)
5. Lessons learned (2 min)

**Cleanup after capstone:**

```bash
make lab-stop
make destroy ENV=dev
make destroy ENV=test   # if applied
# Destroy bootstrap bucket only when ALL envs destroyed
```

---

## Part 3 — Cost & operations reference

### Hourly cost drivers (dev stack)

| Resource | Approx. cost note |
|----------|-------------------|
| EC2 lab + NAT instance (t3.micro × 2) | ~$0.02/hr running |
| NAT Gateway (prod config) | ~$0.045/hr + data |
| VPC, subnets, IGW | No hourly charge |
| Flow logs | CloudWatch ingestion |
| S3 state + DynamoDB locks | Pennies |

### Daily instructor routine

```bash
# Start of session
make lab-start

# End of session
make lab-stop

# Weekend / between cohorts
make lab-teardown
```

### Troubleshooting

| Issue | Fix |
|-------|-----|
| `terraform init` registry error | `./scripts/aws/install-provider.sh` + `TF_CLI_CONFIG_FILE` |
| Flow log group already exists | `verify-labs.sh` pre-deletes; or manual `aws logs delete-log-group` |
| `ExpiredToken` | `aws sso login` |
| Start/stop no effect | Confirm tag `Course=terraform-enterprise` on instances |
| Lock error | Another apply running; or stale lock in DynamoDB |

---

## Part 4 — Demo day cheat sheet (2-hour session)

| Time | Activity | Command / location |
|------|----------|-------------------|
| 0:00 | Toolchain | `terraform version`, `aws sts get-caller-identity` |
| 0:10 | Architecture | `diagrams/png/00-lab-vpc-architecture.png` |
| 0:20 | Live apply | `make apply ENV=dev` or show existing stack |
| 0:35 | State | `terraform state list`, S3 state path |
| 0:45 | Modules | `modules/vpc`, `dev/main.tf` module block |
| 0:55 | Cost control | `make lab-stop` / `make lab-start` |
| 1:05 | Drift | Console SG change → `make plan ENV=dev` |
| 1:20 | CI | GitHub PR with workflow green |
| 1:35 | Promotion | Console: 3 VPCs (10.10 / 10.20 / 10.30) + prod NAT GW |
| 1:50 | Q&A | `docs/LAB-DEMO-GUIDE.md` |

---

## Related docs

- [labs/README.md](../labs/README.md) — lab index
- [GITHUB-SECRET-AWS_ROLE_ARN.md](GITHUB-SECRET-AWS_ROLE_ARN.md) — Week 4 OIDC secret
- [WEEK-04-GITHUB-SETUP.md](WEEK-04-GITHUB-SETUP.md) — full CI setup
- [scripts/aws/README.md](../scripts/aws/README.md) — start/stop scripts
- [instructor/INSTRUCTOR-GUIDE.md](../instructor/INSTRUCTOR-GUIDE.md) — cohort operations
- [TRAINING-MONOREPO.md](../TRAINING-MONOREPO.md) — monorepo layout
