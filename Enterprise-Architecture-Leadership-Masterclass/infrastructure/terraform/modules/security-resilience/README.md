# Terraform module: security-resilience (BayLearn Module 07)

Deploys a low-cost security and resilience lab slice for NorthStar Financial Services (fictional):

- KMS CMK with key rotation
- Versioned S3 primary bucket (SSE-KMS, Block Public Access, TLS + encryption denials)
- Least-privilege IAM roles (writer / reader / auditor)
- DynamoDB on-demand control-evidence table
- SNS + CloudWatch alarms
- Optional cross-region replication (`enable_replication`)
- Lightweight Lambda to record recovery-drill metrics

## Providers

Requires default `aws` provider (primary region) and optional `aws.replica` when replication is enabled.

```hcl
provider "aws" {
  region = var.aws_region
}

provider "aws" {
  alias  = "replica"
  region = var.replica_region
}
```

## Cost warning

Keep `enable_replication = false` unless you accept CRR cost and will destroy the same day. Always run the cleanup script after class.

## Usage

See `infrastructure/terraform/environments/lab07/`.
