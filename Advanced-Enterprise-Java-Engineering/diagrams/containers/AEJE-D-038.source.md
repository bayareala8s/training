# AEJE-D-038 — OCI container layers

- Type: concept
- Module: 9
- Maps to: L-9.1
- Complexity: 1

```mermaid
flowchart LR
  Base[JRE base] --> Deps[deps layer]
  Deps --> App[app layer]
  App --> Cfg[config / user]
```
