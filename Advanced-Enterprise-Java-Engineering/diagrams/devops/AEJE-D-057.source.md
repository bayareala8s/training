# AEJE-D-057 — Failed deployment and rollback

- Type: incident
- Module: 12
- Maps to: INCIDENT-1205
- Complexity: 3

```mermaid
flowchart LR
  Bad[new tag unhealthy] --> CB[circuit breaker]
  CB --> Old[last healthy 3.8.0]
```
