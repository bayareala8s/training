# BUILD-1300 — starter vs OBSERVABILITY.md (before edit)

| Contract | Starter |
|---|---|
| Rate `POST /api/v1/payments` | Present |
| 5xx errors (not ordinary 4xx as burn) | **Missing** |
| P99 histogram quantile | **Missing** |
| JVM heap used/max | **Missing** |
| Hikari `jdbc/baypay` active **and** pending | **Missing** |
| Servlet / Tomcat busy/max | **Missing** |
| SLO **99.9%** + error-budget / burn | **Missing** |
| Labels `uri`/`method`/`outcome`/`status` only | Rate panel OK — do not add customer/account/paymentId |

Jordan called rate “a start.” Priya will not page from it. Fixes in `work/` only.
