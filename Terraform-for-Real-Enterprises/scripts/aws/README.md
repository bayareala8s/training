# AWS Lab Start / Stop Scripts

Cost-control scripts for **BayAreaLa8s – Terraform for Real Enterprises**.

## Recommended: pause / resume (near-zero cost)

When you are **not** in a lab session, pause everything billable:

```bash
# End of day / weekend — stops EC2 and destroys NAT Gateways
make lab-pause

# Before next session — recreates prod NAT GW (~2 min) and starts EC2
make lab-resume

# Check what is still billing
make lab-status
```

| Command | EC2 | NAT instance (dev/test) | NAT Gateway (prod) | Typical hourly cost |
|---------|-----|-------------------------|--------------------|---------------------|
| **Running labs** | running | running | available | ~$0.05–0.09/hr |
| `make lab-stop` | stopped | stopped | **still bills** | ~$0.045/hr (NAT GW) |
| **`make lab-pause`** | stopped | stopped | **destroyed** | ~$0 (state/S3 only) |
| **`make lab-resume`** | running | running | recreated | back to lab rates |

Test the full cycle:

```bash
make lab-cycle    # pause → wait → resume
```

## Quick start (legacy stop/start)

```bash
cd scripts/aws
chmod +x *.sh lib/*.sh

./start-lab.sh      # before session (compute only)
./stop-lab.sh       # after session (compute only — NAT GW still bills)
./status-lab.sh
```

## Scripts

| Script | Purpose |
|--------|---------|
| **`pause-labs.sh`** | Stop EC2/RDS/ECS/ASG + destroy prod NAT Gateway via Terraform |
| **`resume-labs.sh`** | Terraform apply prod (if NAT missing) + start all compute |
| **`cycle-labs.sh`** | Smoke test: pause → resume |
| `start-lab.sh` | Start EC2, RDS, NAT instances, ASG, ECS |
| `stop-lab.sh` | Stop EC2, NAT instances, RDS; scale ECS/ASG to 0 |
| `status-lab.sh` | EC2, NAT GW, RDS status + cost warnings |
| `teardown-all.sh` | Stop + destroy dev stack (heavy teardown) |
| `verify-labs.sh` | Instructor validate/apply/test/teardown |

### Flags

```bash
./pause-labs.sh --skip-terraform   # stop compute only; NAT GW keeps billing
./resume-labs.sh --skip-terraform  # start EC2 only
DRY_RUN=1 ./pause-labs.sh          # preview
```

## Required tags

```hcl
tags = {
  Course      = "terraform-enterprise"
  Project     = "bayareala8s-tf-course"
  ManagedBy   = "terraform"
  Environment = var.environment
}
```

## Prerequisites

- AWS CLI v2 configured (`aws sts get-caller-identity`)
- For pause/resume NAT Gateway: Terraform + `backend.hcl` / `terraform.tfvars` (or `.example` files) in each environment
- If `terraform init` fails: `./install-provider.sh` and `export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc`

## What does NOT bill when paused

| Resource | Notes |
|----------|--------|
| Stopped EC2 | No compute charge |
| Destroyed NAT Gateway | Recreated on `resume-labs.sh` |
| VPC, subnets, IGW | No hourly charge |
| S3 state + DynamoDB | Pennies |

## Makefile (repo root)

```bash
make lab-pause
make lab-resume
make lab-cycle
make lab-start
make lab-stop
make lab-status
make lab-teardown
```

## Verify labs on AWS (instructors)

```bash
export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc  # if registry fails
./scripts/aws/verify-labs.sh all
./scripts/aws/cycle-labs.sh   # test pause/resume
```
