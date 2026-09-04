# AEJE-D-045 — OOMKilled

- Type: incident
- Module: 10
- Maps to: INCIDENT-1002
- Complexity: 3

```mermaid
flowchart TB
  Limit[512Mi limit] --> Xmx[-Xmx 512m]
  Xmx --> Kill[OOMKilled]
```
