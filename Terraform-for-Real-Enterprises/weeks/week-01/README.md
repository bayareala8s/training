# Week 1 – Enterprise Infrastructure as Code Foundations

> **Full module:** [course-modules/week-01](../../course-modules/week-01/) — detailed lecture, assignment, quiz, instructor notes

## Learning Objectives

- Explain why enterprises adopt Terraform and how it differs from CloudFormation
- Describe state, backends, and infrastructure lifecycle at a production level
- Stand up a secure remote state backend and baseline repo layout

## Topics

- Terraform fundamentals
- Terraform vs CloudFormation
- Enterprise IaC challenges
- State management concepts
- Infrastructure lifecycle management

## Labs

| Lab | Guide |
|-----|--------|
| **1.1** Install toolchain | [labs/week-01/LAB-01-install.md](../../labs/week-01/LAB-01-install.md) |
| **1.2** AWS provider | [labs/week-01/LAB-02-provider.md](../../labs/week-01/LAB-02-provider.md) |
| **1.3** Remote state | [labs/week-01/LAB-03-backend.md](../../labs/week-01/LAB-03-backend.md) |

### Lab 1.3 checklist

- [ ] S3 bucket: encryption, versioning, public access blocked
- [ ] DynamoDB table for state locking
- [ ] `backend.tf` referencing backend (bootstrap pattern documented)
- [ ] Baseline resource (e.g. tagging demo or minimal VPC placeholder)

## Deliverables

1. **Enterprise Terraform repo structure** — Use [starter-templates/enterprise-repo](../../starter-templates/enterprise-repo)
2. **Remote backend configuration** — Document bootstrap vs workload state
3. **Baseline infrastructure deployment** — `terraform plan` / `apply` success with remote state

## Suggested Time

8–9 hours (lecture + labs)

## Further Reading

- [Terraform: State](https://developer.hashicorp.com/terraform/language/state)
- [AWS: S3 backend](https://developer.hashicorp.com/terraform/language/settings/backends/s3)

## Submission

Open a PR titled `week-01: remote backend and repo baseline` with links to your fork and a short README section describing your backend design.
