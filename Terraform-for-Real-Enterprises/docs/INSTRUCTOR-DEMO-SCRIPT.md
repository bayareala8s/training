# Instructor Demo Script — Every Lab

**Course:** Terraform for Real Enterprises · **BayAreaLa8s**  
**Repo:** `training/Terraform-for-Real-Enterprises`  
**Full run guide:** [LAB-DEMO-GUIDE.md](LAB-DEMO-GUIDE.md)

Use this document when **demoing live**. Each section is numbered steps only—no student deliverables.

---

## Before any demo session (5 min)

1. Open terminal in course root:
   ```bash
   cd training/Terraform-for-Real-Enterprises
   export AWS_REGION=us-west-2
   export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc   # if terraform init fails
   ```
2. Confirm AWS access:
   ```bash
   aws sts get-caller-identity
   ```
3. Start lab compute:
   ```bash
   make lab-start && make lab-status
   ```
4. Open AWS Console → **us-west-2** → VPC (for architecture demos).
5. Optional second screen: GitHub → https://github.com/bayareala8s/training/actions

**Live stacks (account `277374794397`):** dev `10.10`, test `10.20`, prod `10.30` + NAT Gateway.

---

## Week 1 — Foundations

### Lab 1.1 — Install Terraform & Toolchain (~5 min demo)

1. Run `terraform version` — point out `>= 1.5.0` requirement.
2. Run `aws --version` and `aws sts get-caller-identity` — show Account ID and region.
3. Show `AWS_PROFILE` or SSO profile in env.
4. Demo `aws sso login` flow if using SSO (or explain why enterprises avoid long-lived keys).
5. **Say:** “Every lab starts with verified toolchain and identity.”

---

### Lab 1.2 — Configure AWS Provider (~10 min demo)

1. Open a scratch dir or show lab file `labs/week-01/LAB-02-provider.md` provider block.
2. Highlight `default_tags` on the `provider "aws"` block.
3. Run `terraform init` and `terraform plan` on the practice S3 bucket (or walk through without apply).
4. Show plan output — tags appear on resources without repeating on each resource block.
5. **Say:** “Enterprises use default_tags for cost allocation and governance at scale.”

---

### Lab 1.3 — Secure Remote State Backend (~20 min demo)

1. Show `labs/shared/environments/dev/backend.hcl.example` — S3 key per environment.
2. Run from repo root:
   ```bash
   make plan ENV=dev
   ```
   Expect **no changes** (stack already live).
3. Run `cd labs/shared/environments/dev && terraform state list` — ~23 resources.
4. Console → VPC → filter tag `Course=terraform-enterprise` → open dev VPC `10.10.0.0/16`.
5. Show subnets: 2 public, 2 private; route table private → NAT **instance** (not Gateway in dev).
6. EC2 → show `bal8s-tf-dev-lab-host` in private subnet.
7. S3 → `bayareala8s-terraform-state` → prefix `terraform-enterprise/environments/dev/`.
8. Demo cost control:
   ```bash
   make lab-stop && make lab-status
   make lab-start && make lab-status
   ```
9. **Say:** “Remote state + locking = team safety; tags = cost control scripts work.”

---

## Week 2 — Multi-account architecture

### Lab 2.1 — Multi-Account Design (~15 min demo)

1. Display `diagrams/png/00-multi-account-summary.png`.
2. Whiteboard or slide: Root → Security OU, Infrastructure OU, Workloads OU (dev/test/prod).
3. Open S3 state bucket — show **three state keys**: `dev/`, `test/`, `prod/` under same prefix.
4. **Say:** “Real enterprises separate accounts; this course uses one account with logical isolation.”
5. Show empty template: students fill `docs/architecture/week-02-accounts.md`.

---

### Lab 2.2 — Cross-Account IAM (~15 min demo)

1. Open `labs/week-02/iam/terraform-runner-trust.json` — explain `Principal` and `Condition`.
2. Open `labs/week-02/iam/terraform-runner-policy.json` — scoped vs wildcard.
3. Console → IAM → Roles → show `github-terraform` (Week 4 OIDC) as contrast.
4. Demo trust concept: tooling account / CI → `AssumeRole` → workload account.
5. **Say:** “No long-lived keys in CI—Week 4 replaces manual assume-role.”

---

### Lab 2.3 — Cross-Account Apply (~10 min demo)

1. Show `aws sts assume-role` command from lab (do not paste real creds on screen long).
2. Run `make plan ENV=dev` with normal profile — plan succeeds against live dev.
3. **Say:** “CI will automate this; students document who can assume the role.”

---

## Week 3 — Modules

### Lab 3.1 — VPC Module (~20 min demo)

1. Open `modules/vpc/main.tf` — VPC, subnets, IGW, NAT instance vs NAT Gateway logic.
2. Open `labs/shared/environments/dev/main.tf` — `module "vpc"` call with variables.
3. Run `make plan ENV=dev` — no changes.
4. Show `use_nat_instance = true` in dev tfvars vs prod `enable_nat_gateway = true`.
5. **Say:** “Modules encapsulate complexity; consumers only pass inputs.”

---

### Lab 3.2 — Compose Modules (~10 min demo)

1. Trace in `dev/main.tf`: `module.vpc.private_subnet_ids[0]` → `module.compute.subnet_id`.
2. Run:
   ```bash
   make validate
   ```
3. **Say:** “Outputs → inputs is how enterprise stacks compose without copy-paste.”

---

### Lab 3.3 — Publish Module (~10 min demo)

1. Show semantic versioning: PATCH / MINOR / MAJOR on whiteboard.
2. Show `source = "../../../../modules/vpc"` vs git `ref=v1.0.0` pattern.
3. **Say:** “Internal registry = Git tags + CHANGELOG + upgrade policy.”

---

## Week 4 — CI/CD

### Lab 4.1 — GitHub Actions CI (~20 min demo)

1. Open https://github.com/bayareala8s/training/actions → workflow **Terraform CI**.
2. Open `Terraform-for-Real-Enterprises/.github/workflows/terraform-ci.yml`.
3. Walk jobs: `validate` (matrix dev/test/prod), `security` (Checkov), `plan-dev`.
4. Show `TF_COURSE_ROOT: Terraform-for-Real-Enterprises` for monorepo paths.
5. Open a recent run — green `validate` + `security`; `plan-dev` needs `AWS_ROLE_ARN` secret.
6. **Say:** “PR = fmt + validate + security; merge path adds plan/apply with gates.”

**Secret (one-time):** [GITHUB-SECRET-AWS_ROLE_ARN.md](GITHUB-SECRET-AWS_ROLE_ARN.md)

---

### Lab 4.2 — Plan → Review → Apply (~15 min demo)

1. GitHub → Settings → Environments — show or create `dev` with required reviewers.
2. In workflow file, point to commented `apply-dev` job and `environment: dev`.
3. **Say:** “Approval gate = change control; prod gets stricter branch + reviewer rules.”

---

### Lab 4.3 — Infrastructure Validation (~10 min demo)

1. Terminal:
   ```bash
   cd modules/vpc
   checkov -d . --framework terraform
   ```
2. Pick one finding — show fix or documented exception in `.checkov.yml`.
3. **Say:** “Shift-left security in CI catches misconfig before apply.”

---

## Week 5 — Promotion & drift

### Lab 5.1 — Environment Promotion (~20 min demo)

1. Console → VPC → filter `Course=terraform-enterprise` — show **three VPCs**:
   - dev `10.10.0.0/16`
   - test `10.20.0.0/16`
   - prod `10.30.0.0/16`
2. EC2 → NAT Gateway on **prod** only (`nat-040739191f78a6fd5`).
3. Side-by-side: `terraform.tfvars.example` for dev vs test vs prod.
4. Run:
   ```bash
   make plan ENV=test
   make plan ENV=prod
   ```
   Expect no changes (stable promotion targets).
5. Walk promotion runbook: PR → plan test → apply test → plan prod → CAB → apply prod.
6. **Say:** “Same modules, different tfvars—that’s enterprise promotion.”

---

### Lab 5.2 — Simulate Drift (~15 min demo)

1. Console → EC2 → dev lab instance security group → **Add inbound rule** (e.g. SSH from 0.0.0.0/0).
2. Terminal:
   ```bash
   make plan ENV=dev
   ```
3. Show plan wants to **remove** the rogue rule.
4. **Say:** “Drift = reality diverged from Terraform desired state.”

---

### Lab 5.3 — Remediate Drift (~10 min demo)

1. Run `make apply ENV=dev` — rule removed.
2. Re-run `make plan ENV=dev` — no changes.
3. Show remediation table (revert vs update code vs import).
4. **Say:** “Scheduled plan jobs catch drift before auditors do.”

---

## Week 6 — Recovery & rollback

### Lab 6.1 — Failed Deployment (~15 min demo)

1. **Prepare beforehand** or use a branch with bad AMI resource (do not apply on production prod).
2. Show failed `terraform apply` output (invalid AMI).
3. Run `terraform state list` — what landed vs what failed.
4. Remove bad code; `terraform plan` — clean.
5. **Say:** “Never delete in console until you know what’s in state.”

---

### Lab 6.2 — State Recovery (~15 min demo)

1. ```bash
   cd labs/shared/environments/dev
   terraform state show 'module.vpc.aws_vpc.this'
   terraform state pull > /tmp/state-backup-demo.json
   ```
2. Console → S3 → state file → **Versions** tab.
3. **Say:** “Versioned state bucket = undo button for infrastructure teams.”

---

### Lab 6.3 — Rollback Workflow (~10 min demo)

1. Run:
   ```bash
   ./scripts/terraform/rollback-plan.sh --env dev --ref HEAD~1
   ```
2. Explain Git revert → CI plan → approved apply = infra rollback.
3. Open `docs/runbooks/terraform-recovery.md` outline.

---

## Week 7 — Security & governance

### Lab 7.1 — IAM Least Privilege (~10 min demo)

1. Open `labs/week-02/iam/terraform-runner-policy.json`.
2. Compare `ec2:*` vs scoped action list side by side.
3. **Say:** “Terraform runner should not be AdministratorAccess.”

---

### Lab 7.2 — Tagging Policies (~10 min demo)

1. Run:
   ```bash
   aws ec2 describe-instances \
     --filters Name=tag:Course,Values=terraform-enterprise \
     --query 'Reservations[].Instances[].[Tags[?Key==`Name`].Value|[0],Tags]' --output table
   ```
2. Open `labs/shared/environments/dev/variables.tf` — `owner` validation block.
3. **Say:** “Tags tie to `make lab-stop`—wrong tags = runaway cost.”

---

### Lab 7.3 — Compliance Checks (~15 min demo)

1. ```bash
   checkov -d modules/ -d labs/shared/ --framework terraform
   ```
2. Show `labs/week-07/.checkov.yml` skip-check with ticket reference.
3. Walk sample row in security report template.

---

## Week 8 — Capstone (~20 min demo of expectations)

1. Open `capstone/README.md` — four track options.
2. Show checklist: remote state, modules, CI, promotion, security report, cost estimate, `lab-stop`.
3. Demo flow students must replicate:
   - Open PR → green CI
   - `make plan ENV=test`
   - Architecture diagram in `diagrams/` or `capstone/`
4. **Say:** “Capstone proves you can run the full enterprise workflow end-to-end.”

---

## End of demo day

```bash
make lab-stop
# Optional: make destroy ENV=prod   # stops NAT Gateway charges
```

---

## Quick reference — demo duration by week

| Week | Total demo time | Needs AWS console | Needs GitHub |
|------|-----------------|-------------------|--------------|
| 1 | ~35 min | Yes (1.3) | No |
| 2 | ~40 min | IAM optional | No |
| 3 | ~40 min | No | No |
| 4 | ~45 min | No | Yes |
| 5 | ~45 min | Yes | No |
| 6 | ~40 min | S3 console | Optional |
| 7 | ~35 min | Yes | No |
| 8 | ~20 min | Optional | Yes |
