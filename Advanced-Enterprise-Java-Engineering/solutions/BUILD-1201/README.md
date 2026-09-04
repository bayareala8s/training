# BUILD-1201 — Instructor solution

**Do not share these files with students before they submit a validate-green root.**

This folder is the answer key for the Terraform **environment skeleton**. Students are not required to `terraform apply`.

## Files

| File | Role |
|---|---|
| [provider.tf](provider.tf) | `required_providers.aws`, provider region `var.region`, ACCOUNT.md default tags |
| [variables.tf](variables.tf) | `region` default `us-west-2`, repository name, expiration |
| [ecr.tf](ecr.tf) | One immutable, scanned ECR repository plus untagged lifecycle |
| [outputs.tf](outputs.tf) | `repository_url`, `repository_arn`, `region` |

A student root that matches contracts (provider pin, `us-west-2`, tags, one ECR, outputs, `terraform validate`) passes even if lifecycle JSON or encryption block differs.

## What the starter got wrong

- Bare `provider "aws"` with **no** `terraform.required_providers`.
- Hardcoded **`us-east-1`**, which violates ACCOUNT.md.
- No `variable "region"`.
- No repository resource and no outputs.

The starter was valid-looking HCL. It was not a BayPay sandbox.

## Required contracts

```text
terraform:  required_providers { aws = hashicorp/aws }
region:     variable default us-west-2; provider uses var.region
tags:       Course=AEJE Module=12 Lab=BUILD-1201 Environment=student Expiration
ecr:        baypay/payment-service; prefer IMMUTABLE + scan_on_push
outputs:    repository_url, repository_arn
scope:      no ALB, ECS service, NAT, RDS, EKS, access keys
validate:   terraform init -backend=false && terraform validate
```

## Checklist (same as the student lab)

- [x] `required_providers.aws`
- [x] `variable "region"` default `us-west-2`
- [x] Provider uses `var.region`
- [x] ACCOUNT.md tags
- [x] One ECR repository
- [x] Outputs present
- [x] No secrets
- [x] `terraform validate` succeeds

## Optional apply

Not required. If a student applies, score Efficiency on destroy + no ALB, not on whether they pushed an image. Deduct Security if keys appear in `.tf` or state is committed.

## Scoring notes

Full marks require the provider pin, region contract, tags, ECR, outputs, and validate. A root that adds NAT/ALB “for realism” fails Production awareness and Cost. `us-east-1` left in place fails Technical accuracy even if ECR syntax is perfect.
