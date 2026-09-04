# AEJE-D-002 — SOLID and immutability

- Type: concept
- Module: 1
- Maps to: L-1.2
- Complexity: 1

```mermaid
flowchart LR
  Cmd[Payment command] --> Money[Money value]
  Money --> Payment[Payment entity]
  Payment --> SM[State machine]
```
