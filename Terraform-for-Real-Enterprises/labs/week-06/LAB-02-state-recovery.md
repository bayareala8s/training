# Lab 6.2 — Terraform State Recovery

**Duration:** 2–3 hours · **Week 6**

## Objectives

- Use `terraform state` subcommands
- Restore state from S3 versioning

## Steps

### 1. State inspection

```bash
cd labs/shared/environments/dev
terraform state list
terraform state show 'module.vpc.aws_vpc.this'
```

### 2. State pull backup

```bash
terraform state pull > /tmp/state-backup-$(date +%Y%m%d).json
```

### 3. S3 version restore (console or CLI)

```bash
aws s3api list-object-versions \
  --bucket YOUR-STATE-BUCKET \
  --prefix environments/dev/terraform.tfstate
```

Restore previous version if needed (lab sandbox only).

### 4. Remove tainted resource (if applicable)

```bash
terraform untaint 'module.compute[0].aws_instance.lab'
```

## Deliverable

Updated [docs/runbooks/terraform-recovery.md](../../docs/runbooks/terraform-recovery.md).

## Next

[Lab 6.3 — Rollback workflow](LAB-03-rollback.md)
