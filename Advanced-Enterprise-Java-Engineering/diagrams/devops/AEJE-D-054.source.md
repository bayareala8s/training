# AEJE-D-054 — Git and CI flow

- Type: concept
- Module: 12
- Maps to: L-12.1
- Complexity: 1

```mermaid
flowchart LR
  PR[pull request] --> CI[mvn test]
  CI --> Img[image tag SHA]
  Img --> Deploy[deploy]
```
