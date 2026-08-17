# Lab 3.1 — Build & Extend VPC Module

**Duration:** 3 hours · **Week 3**

## Objectives

- Understand module in `modules/vpc/`
- Add an optional feature (e.g. VPC endpoints or additional subnet tier)
- Write module README with examples

## Steps

### 1. Review existing module

```bash
cd modules/vpc
terraform fmt
cat README.md variables.tf outputs.tf main.tf
```

### 2. Run dev environment using module

```bash
make plan ENV=dev
```

### 3. Enhancement (choose one)

**Option A — S3 VPC endpoint:**
Add `aws_vpc_endpoint` for S3 in private route table.

**Option B — Database subnet tier:**
Add `database_subnets` variable and subnet resources.

### 4. Document inputs/outputs

Update `modules/vpc/README.md` with before/after example.

### 5. Version module

```bash
git tag -a modules/vpc/v1.0.0 -m "VPC module initial release"
```

## Deliverable

- Module enhancement merged
- Tagged release `v1.0.0` (or documented internal version)

## Next

[Lab 3.2 — Compose modules](LAB-02-compose.md)
