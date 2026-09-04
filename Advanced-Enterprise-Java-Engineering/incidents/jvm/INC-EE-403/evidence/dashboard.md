# Dashboard — payment vs ledger coverage

**Window:** 2026-08-21 16:30–18:30 UTC  
**Source:** synthetic BayPay Grafana snapshot  
**Gate:** 2

## API success

| Metric | 16:30–17:09 | 17:10–18:22 |
|---|---|---|
| `POST /api/v1/payments` 2xx | 211 | 184 |
| `POST /api/v1/payments` 5xx | 0 | 0 |
| Create p99 | 190 ms | 205 ms |
| Actuator readiness | UP | UP |

HTTP looks healthy after 17:10.

## Ledger coverage (recon)

| Metric | 16:30–17:09 | 17:10–18:22 |
|---|---|---|
| Payments ending `COMPLETED` | 208 | 184 |
| Matching `ledger_transactions` rows (PAYMENT type) | 208 | **178** |
| Coverage | 100% | **96.7%** |
| Notifications sent (`PaymentCompletedEvent`) | 208 | 184 |

## Database

| Metric | 18:22 |
|---|---|
| Writer CPU | 22% |
| Hikari active / max (pay-prod-east-1) | 11 / 50 |
| Deadlocks / 1h | 0 |
| Unique violations on `ledger_transactions_pkey` | 6 (all after 17:10) |

## Notes

Missing rows cluster after the 17:10 UTC deploy window. Pool is not exhausted. No SEV on JDBC timeouts.
