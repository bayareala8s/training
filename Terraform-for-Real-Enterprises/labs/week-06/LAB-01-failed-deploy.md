# Lab 6.1 — Simulate Failed Deployment

**Duration:** 2 hours · **Week 6**

## Objectives

- Experience a failed `terraform apply`
- Practice safe recovery without corrupting state

## Steps

### 1. Introduce intentional error

In `labs/shared/environments/dev/main.tf`, temporarily add:

```hcl
resource "aws_instance" "bad" {
  ami           = "ami-invalid"
  instance_type = "t3.micro"
  subnet_id     = module.vpc.public_subnet_ids[0]
}
```

### 2. Run apply

```bash
make apply ENV=dev
```

Observe partial apply behavior.

### 3. Revert code

Remove bad resource; run `terraform plan`.

## Deliverable

Notes on what remained in state vs AWS after failure.

## Next

[Lab 6.2 — State recovery](LAB-02-state-recovery.md)
