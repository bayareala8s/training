# AEJE-D-058 — Ansible configuration automation

- Type: deployment
- Module: 12
- Maps to: BUILD-1203
- Complexity: 2

```mermaid
flowchart LR
  Vars[group_vars] --> Play[playbook]
  Play --> Env[server.env template]
```
