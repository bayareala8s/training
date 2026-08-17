# Week 5 — Glossary

| Term | Definition |
|------|------------|
| **Environment promotion** | Controlled movement of reviewed infrastructure changes through dev, test, and prod |
| **Configuration drift** | Difference between actual infrastructure and Terraform desired state/state |
| **Promotion gate** | Checkpoint (plan review, test apply, approval) before next environment |
| **Saved plan** | Binary plan file applied with `terraform apply plan.out` for reproducibility |
| **Refresh** | Updating state attributes from cloud APIs during plan |
| **forces replacement** | Plan indication that resource will be destroyed and recreated |
| **moved block** | HCL declaring resource address migration without destroy/create |
| **state mv** | CLI command relocating an address in state |
| **Remediation** | Correcting drift via apply, import, or code update |
| **Adopt (drift)** | Updating Terraform code to match intentional manual changes |
| **Revert (drift)** | Applying Terraform to undo unauthorized manual changes |
| **Blast radius** | Scope of impact from a change or failure |
| **Change advisory** | Formal approval body for production changes |
| **Smoke test** | Quick validation after deploy (health, tags, connectivity) |
| **Representative tfvars** | Test variables that mirror prod topology sufficiently for validation |
