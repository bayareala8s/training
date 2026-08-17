# Hands-On Labs Index

Complete lab instructions for **Terraform for Real Enterprises**. Work in order; each week builds on the last.

**Instructors:** see the full step-by-step demo and run guide → [docs/LAB-DEMO-GUIDE.md](../docs/LAB-DEMO-GUIDE.md)

## Before you start

1. AWS account with admin lab access (or scoped lab OU)
2. Terraform >= 1.5, AWS CLI v2, Git
3. Copy `terraform.tfvars.example` → `terraform.tfvars` (never commit real tfvars)
4. After Week 1: configure S3 backend per environment

## Cost control

```bash
# From repo root
make lab-stop    # end of session
make lab-start   # before session
```

See [scripts/aws/README.md](../scripts/aws/README.md).

## Lab map

| Week | Labs | Path |
|------|------|------|
| 1 | Install, provider, remote state | [week-01](week-01/) |
| 2 | Multi-account design & cross-account IAM | [week-02](week-02/) |
| 3 | VPC module & publishing | [week-03](week-03/) |
| 4 | GitHub Actions CI/CD | [week-04](week-04/) |
| 5 | Promotion & drift | [week-05](week-05/) |
| 6 | Rollback & state recovery | [week-06](week-06/) |
| 7 | Security & governance | [week-07](week-07/) |
| 8 | Capstone | [week-08](week-08/) |

## Shared environments

| Environment | CIDR | Purpose |
|-------------|------|---------|
| dev | 10.10.0.0/16 | Daily labs, NAT instance |
| test | 10.20.0.0/16 | Promotion target |
| prod | 10.30.0.0/16 | Capstone (NAT GW optional) |

Path: `labs/shared/environments/{dev,test,prod}/`

## Quick commands

```bash
make bootstrap          # Week 1 — state bucket
make init ENV=dev
make plan ENV=dev
make apply ENV=dev
```
