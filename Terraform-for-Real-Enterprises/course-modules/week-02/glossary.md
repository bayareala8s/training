# Week 2 — Glossary

| Term | Definition |
|------|------------|
| **AWS Organizations** | Service to centrally manage multiple AWS accounts, OUs, and policies |
| **Management account** | Organization root account that creates the org and can invite/create member accounts |
| **Member account** | AWS account belonging to an organization |
| **Organizational unit (OU)** | Container for accounts within an organization hierarchy |
| **SCP (Service Control Policy)** | Organization policy that sets maximum permissions for accounts in an OU |
| **Landing zone** | Multi-account baseline with identity, security, logging, and network guardrails |
| **Control Tower** | AWS-managed landing zone solution for account vending and guardrails |
| **Shared services account** | Account hosting centralized capabilities (DNS, CI, egress, state) |
| **Blast radius** | Scope of impact when a failure or breach occurs |
| **Cross-account role** | IAM role in one account trusted by principals in another account |
| **Trust policy** | IAM policy document defining who can assume a role |
| **ExternalId** | Optional secret used in trust policies to prevent confused deputy attacks |
| **AssumeRole** | STS API returning temporary credentials for a role in same or different account |
| **Hub-and-spoke** | Network topology with central hub (TGW/firewall) connecting spoke VPCs per account |
| **Account vending** | Automated creation and baseline configuration of new AWS accounts |
| **Confused deputy** | Security issue where a service is tricked into using its permissions on wrong resources |
| **Log archive account** | Dedicated account for immutable centralized logs |
| **Terraform runner role** | IAM role used by humans or CI to execute Terraform in a workload account |
