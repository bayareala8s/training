# Lab 1.2 — Configure AWS Provider

**Duration:** 60 minutes · **Week 1**

## Objectives

- Use provider constraints and `default_tags`
- Run a minimal plan/apply with local state (practice only)

## Steps

### 1. Create practice directory

```bash
mkdir -p ~/tf-lab-practice && cd ~/tf-lab-practice
```

### 2. Create `versions.tf`

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"

  default_tags {
    tags = {
      Course    = "terraform-enterprise"
      Project   = "bayareala8s-tf-course"
      ManagedBy = "terraform"
      Lab       = "1.2-provider"
    }
  }
}
```

### 3. Create `main.tf`

```hcl
resource "aws_s3_bucket" "lab_marker" {
  bucket = "bal8s-lab-marker-${data.aws_caller_identity.current.account_id}-practice"

  lifecycle {
    prevent_destroy = false
  }
}

data "aws_caller_identity" "current" {}
```

> **Note:** S3 bucket names must be globally unique. Adjust prefix with your student ID.

### 4. Initialize and plan

```bash
terraform init
terraform plan
```

### 5. Apply and destroy (cleanup)

```bash
terraform apply
terraform destroy
```

## Enterprise discussion

- Why `default_tags` beats repeating tags on every resource
- Why provider version constraints matter in teams

## Deliverable

Short paragraph: how `default_tags` helps governance and cost allocation.

## Next

[Lab 1.3 — Remote State Backend](LAB-03-backend.md)
