

# 🔧 **Refactored: Security & Compliance (ARC-ready)**

### Security & Compliance

The platform follows a defense-in-depth model aligned with Zero Trust principles, implementing security controls across identity, network, application, and data layers to ensure secure and compliant file transfer operations.

---

### Access Control

* Enforced using AWS IAM roles and policies based on least privilege
* Roles are scoped to specific services and workflows
* No long-lived credentials; all access is role-based

---

### Encryption

**Encryption in Transit**

* SFTP transfers use SSH-based encryption (public-key cryptography + symmetric session encryption)
* API-based integrations (e.g., S3 access) use HTTPS/TLS

**Encryption at Rest**

* All data stored in S3 and DynamoDB is encrypted using AWS KMS
* Server-side encryption is enforced by default

**Secrets Management**

* AWS Secrets Manager is used for secure storage and rotation of credentials and API keys
* No secrets are hardcoded in application code or configuration

---

### Key Management & Isolation

* KMS keys are logically isolated per customer to reduce blast radius
* Key usage is enforced via IAM policies and scoped access
* Scales using centralized KMS with per-customer key segregation strategy (no key sprawl / controlled lifecycle)

---

### Data Protection & Backup

* DynamoDB Point-In-Time Recovery (PITR) is enabled for continuous data protection
* AWS Backup is used for centralized backup governance, retention, and compliance policies
* PITR provides fine-grained recovery; AWS Backup provides policy-driven backup management (non-duplicative roles)

---

### Network Security

* Services are deployed within VPCs with restricted access via security groups and endpoint policies
* No public exposure of internal services
* All communication between components is secured and restricted

---

### Compliance Gap (Current Release)

* Malware/content inspection (per FRISS Control CFL02.010) is not included in this release
* A POAM has been established to address this in a future release

---

# 🎯 What this fixes (mapping to comments)

| Comment                                 | Fix                                           |
| --------------------------------------- | --------------------------------------------- |
| “Separate encryption items”             | Split into Transit / At Rest / Secrets        |
| “SFTP does not use TLS”                 | Corrected to SSH-based encryption             |
| “KMS per customer unclear”              | Explicit section + scaling clarification      |
| “Backup confusion (PITR vs AWS Backup)” | Clearly separated responsibilities            |
| “Too verbose / unclear”                 | Reduced + structured bullets                  |
| “IDD vs Wiki detail level”              | Kept high-level, no deep implementation noise |

---

