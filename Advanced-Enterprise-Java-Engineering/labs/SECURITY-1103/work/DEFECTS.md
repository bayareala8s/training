# SECURITY-1103 — starter defects (before edit)

| File | Defect |
|---|---|
| `iam-combined.json` | **One** role `baypay-payment-combined` used as both execution and task |
| `iam-combined.json` | Attaches **`AdministratorAccess`** |
| `task-definition.json` | `executionRoleArn` and `taskRoleArn` are the **same ARN** |
| `task-definition.json` | Plaintext `BAYPAY_DB_URL`, `BAYPAY_DB_USER`, **`BAYPAY_DB_PASSWORD=changeme`** in `environment` |
| (absent) | No Secrets Manager `valueFrom`, no CMK policy |

This is AEJE-D-050: if the values are in git, the vault is theater. If the task role is admin, a compromised JVM is the account.

Fixes live in this `work/` tree. Starter left for classmates. Teaching account `123456789012`. No apply.
