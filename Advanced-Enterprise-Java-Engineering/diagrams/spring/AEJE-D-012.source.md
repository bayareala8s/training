# AEJE-D-012 — Actuator health and readiness

- Type: component
- Module: 3
- Maps to: BUILD-305
- Complexity: 2

```mermaid
flowchart LR
  K8s[Probe] --> Live[/actuator/health/liveness]
  K8s --> Ready[/actuator/health/readiness]
  Ready --> DB[DataSource health]
```
