# AEJE-D-061 — BayPay operations dashboard

- Type: component
- Module: 13
- Maps to: BUILD-1300
- Complexity: 3

```mermaid
flowchart TB
  Rate[POST rate] --> Dash[ops dashboard]
  P99[P99 duration] --> Dash
  Burn[SLO burn] --> Dash
  Hikari[Hikari pending] --> Dash
```
