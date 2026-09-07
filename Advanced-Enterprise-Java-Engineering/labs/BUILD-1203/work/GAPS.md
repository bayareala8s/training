# BUILD-1203 — starter gaps (before edit)

| Missing | Starter |
|---|---|
| `inventory.ini` localhost / local | Absent |
| `group_vars` host / port / db / user | Playbook only has `output_dir` |
| `templates/payment-service.env.j2` | Absent |
| `templates/server.env.j2` (Liberty) | Absent |
| `template` tasks | Only `file:` mkdir |
| Password | Correctly **not** a literal — keep that |

Connection / `gather_facts: false` already present. Fixes in `work/` only.
