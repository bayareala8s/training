# Capstone Option 1 — Enterprise Landing Zone

**Track:** Multi-account AWS foundation  
**Duration:** ~10–12 hours · Week 8  
**Status:** Reference implementation (ready to apply)

## Business problem

Enterprises need a **secure, governed foundation** before workloads: account boundaries, baseline networking, remote state, and CI/CD for infrastructure changes.

## What this project delivers

| Requirement | Where |
|-------------|--------|
| OU/account model | [docs/architecture/account-model.md](docs/architecture/account-model.md) |
| Shared networking + flow logs | `terraform/environments/shared/` (uses course `modules/vpc`) |
| Remote state per environment | `backend.hcl.example` |
| CI/CD plan on PR | [.github/workflows/terraform-ci.yml](.github/workflows/terraform-ci.yml) |
| Security review | [docs/security-review.md](docs/security-review.md) |
| Cost analysis | [docs/cost-analysis.md](docs/cost-analysis.md) |

## Architecture (single-account lab mode)

Same AWS account, **logical** separation via state keys + tags (matches course Week 2 single-account mode):

```text
Organization (design)
├── Shared Services  → terraform/environments/shared  (10.40.0.0/16)
└── Workloads
    └── Dev baseline → terraform/environments/workload-dev (10.41.0.0/16)
```

Multi-account production: deploy each environment with different `AWS_PROFILE` / assume-role and separate state keys.

## Quick start

```bash
# From course repo root
cd capstone/option-01-landing-zone

# Shared foundation
cd terraform/environments/shared
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
# edit owner / bucket

terraform init -backend-config=backend.hcl
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars

# Workload baseline (optional second stack)
cd ../workload-dev
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
terraform init -backend-config=backend.hcl
terraform apply -var-file=terraform.tfvars
```

## Cost control

Resources tagged `Course=terraform-enterprise`. From course root:

```bash
make lab-pause    # after demo
make lab-resume   # before next session
```

## Presentation (15–20 min)

1. Problem (2) · 2. Account model (5) · 3. Live plan/apply shared (5) · 4. Security/cost (3) · 5. Lessons (2)
