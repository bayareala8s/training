# Lab 1.3 — Secure Remote State Backend

**Duration:** 2–3 hours · **Week 1**

## Objectives

- Bootstrap S3 + DynamoDB for Terraform state
- Migrate workload environments to remote backend
- Deploy baseline dev environment

## Steps

### 1. Bootstrap state infrastructure

```bash
cd labs/week-01/bootstrap
cp terraform.tfvars.example terraform.tfvars
# Edit: unique state_bucket_name, student_id
terraform init
terraform apply
```

Save outputs: bucket name, DynamoDB table, `backend_config` snippet.

### 2. Configure dev environment backend

```bash
cd ../../shared/environments/dev
cp backend.hcl.example backend.hcl
cp terraform.tfvars.example terraform.tfvars
# Edit backend.hcl with your bucket and table
# Edit terraform.tfvars with owner, region, AZs
```

### 3. Initialize with remote backend

From repo root:
```bash
make init ENV=dev
make plan ENV=dev
make apply ENV=dev
```

### 4. Verify state in S3

```bash
aws s3 ls s3://YOUR-BUCKET/environments/dev/
```

### 5. Test start/stop scripts

```bash
make lab-stop
make lab-status
make lab-start
```

Confirm EC2 instances (lab host + NAT) transition stopped → running.

## Deliverables

- [ ] Bootstrap applied; outputs documented in personal README
- [ ] `dev` environment uses remote state with locking
- [ ] VPC + optional compute running with course tags
- [ ] Evidence: `terraform state list` output (redact account if needed)

## Security checklist

- [ ] S3 public access blocked
- [ ] Versioning enabled on state bucket
- [ ] DynamoDB lock table exists
- [ ] No `.tfvars` committed to Git

## Next week

[Week 2 — Multi-account](../week-02/LAB-01-organizations.md)
