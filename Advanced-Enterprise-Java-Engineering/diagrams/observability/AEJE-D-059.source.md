# AEJE-D-059 — Logs, metrics and traces

- Type: concept
- Module: 13
- Maps to: L-13.1
- Complexity: 1

```mermaid
flowchart LR
  Log[JSON logs] --> Corr[correlationId]
  Met[metrics] --> Prom[Prometheus]
  Tr[traceparent] --> Span[spans]
```
