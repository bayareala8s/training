# Enterprise Terraform Repository Layout

Recommended layout for cohort labs and capstone work.

```text
.
├── README.md
├── .gitignore
├── .terraform-version          # pin Terraform version (optional)
├── backend.tf                  # remote state (after bootstrap)
├── versions.tf                 # provider constraints
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars.example
│   │   └── backend.tf          # or backend config via -backend-config
│   ├── test/
│   └── prod/
├── modules/
│   └── vpc/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── README.md
├── bootstrap/                  # one-time: state bucket + lock table
│   └── main.tf
└── docs/
    ├── architecture.md
    └── runbooks/
```

## Principles

1. **One state per blast radius** — Separate state for network, data, and app tiers when they change at different rates.
2. **Modules own contracts** — Inputs/outputs are your API; version with tags.
3. **No secrets in Git** — Use CI OIDC, AWS Secrets Manager, or SSM Parameter Store.
4. **Tag everything** — `Environment`, `Owner`, `CostCenter`, `ManagedBy = terraform`.

## Bootstrap Order

1. Apply `bootstrap/` locally (or via separate pipeline) to create S3 + DynamoDB.
2. Migrate or configure `backend.tf` in each environment.
3. Apply `environments/dev` first, then promote patterns to test/prod.

Copy this structure into your personal cohort repository for Week 1.
