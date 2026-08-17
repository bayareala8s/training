# Week 1 Bootstrap — Remote State

One-time setup for student-owned S3 + DynamoDB state backends.

**Org shared state (default for this course):** skip bootstrap; use `backend.hcl.example` pointing at `bayareala8s-terraform-state`.

## Student-owned bootstrap

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit: unique state_bucket_name, student_id
terraform init
terraform apply
```

Save outputs: bucket name, DynamoDB table, backend config snippet.

## Next

Configure `labs/shared/environments/dev/backend.hcl` and apply dev stack per [LAB-03-backend.md](../../week-01/LAB-03-backend.md).
