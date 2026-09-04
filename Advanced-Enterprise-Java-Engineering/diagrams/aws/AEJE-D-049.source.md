# AEJE-D-049 — ECS vs EKS vs OpenShift

- Type: executive
- Module: 11
- Maps to: ARCHITECT-1102
- Complexity: 4

```mermaid
flowchart LR
  ECS[ECS Fargate] --- EKS[EKS]
  EKS --- OCP[OpenShift]
  Pay[payment-service] --> ECS
```
