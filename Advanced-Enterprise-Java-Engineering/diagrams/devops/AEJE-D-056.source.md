# AEJE-D-056 — CI/CD pipeline

- Type: component
- Module: 12
- Maps to: BUILD-1204
- Complexity: 3

```mermaid
flowchart LR
  Push[git push] --> Test[Java 21 tests]
  Test --> Build[image]
  Build --> ECR[ECR SHA]
```
