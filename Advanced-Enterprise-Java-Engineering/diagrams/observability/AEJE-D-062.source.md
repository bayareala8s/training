# AEJE-D-062 — Throughput collapse and P99 spike

- Type: incident
- Module: 13
- Maps to: INCIDENT-1301
- Complexity: 3

```mermaid
flowchart LR
  Rel[new release] --> Red[rate down]
  Red --> P99[P99 up]
  P99 --> Gate[gated evidence]
```
