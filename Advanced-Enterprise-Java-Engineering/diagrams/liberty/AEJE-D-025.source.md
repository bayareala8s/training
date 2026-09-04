# AEJE-D-025 — BayPay Liberty adaptation

- Type: modernization
- Module: 6
- Maps to: MODERNIZE-602
- Complexity: 3

```mermaid
flowchart LR
  EAR[payment.ear on ND] --> WAR[payment-service.war]
  WAR --> LIB[Liberty]
  LIB --> DS[jdbc/baypay-payment]
```
