# AEJE-D-066 — Regional DR, RTO and RPO

- Type: executive
- Module: 14
- Maps to: DR-1403
- Complexity: 4

```mermaid
flowchart LR
  West[us-west-2 gone] --> RPO[RPO payment vs report]
  RPO --> East[paper us-east-1]
  East --> RTO[RTO to take POSTs]
```
