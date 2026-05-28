# Week 1 — Glossary

| Term | Definition |
|------|------------|
| **IaC (Infrastructure as Code)** | Managing infrastructure through machine-readable definition files rather than manual processes |
| **HCL** | HashiCorp Configuration Language; Terraform’s primary syntax |
| **Provider** | Plugin that implements resource types for a platform (e.g. `hashicorp/aws`) |
| **Resource** | Infrastructure object managed by Terraform (e.g. `aws_s3_bucket`) |
| **State** | JSON snapshot mapping Terraform addresses to real-world IDs |
| **Plan** | Report of proposed changes before apply |
| **Apply** | Execution of planned infrastructure changes |
| **Backend** | Configuration for where state is stored (local, S3, etc.) |
| **State locking** | Mechanism preventing concurrent writes to state |
| **Bootstrap** | Initial resources (state bucket) created outside normal backend cycle |
| **Drift** | When real infrastructure differs from Terraform configuration/state |
| **Blast radius** | Scope of impact when a change or failure occurs |
| **default_tags** | AWS provider feature applying tags to all supported resources |
| **Immutable infrastructure** | Pattern of replacing rather than patching (contrast with mutable updates) |
| **Change advisory** | Formal review before production deployment |
