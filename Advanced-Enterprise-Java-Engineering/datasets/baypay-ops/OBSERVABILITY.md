# BayPay operations notes — Module 13

**Fictional company. Synthetic metrics.** Students may read this file. Instructor incident RCAs live only under `solutions/`.

This is the **locked operations contract** for Production Engineering and Observability. Lessons and labs reuse these names. Do not invent a second product, a second SLO, or a live Grafana requirement.

## Defaults

| Field | Value |
|---|---|
| App | `payment-service` (Java 21, Spring Boot 3.5.5) |
| Region (when AWS is named) | `us-west-2` |
| Port | `8080` |
| Health | `/actuator/health/liveness`, `/actuator/health/readiness` |
| Golden request | `POST /api/v1/payments` with `Idempotency-Key` |
| Happy path | `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED` |
| Log shape | JSON lines; fields `ts`, `level`, `logger`, `msg`, `correlationId`, `paymentId`, `outcome` |
| Trace | W3C `traceparent` on inbound HTTP; optional OpenTelemetry exporter |
| Metrics | Micrometer / Prometheus scrape on `/actuator/prometheus` |
| Dashboard home | Paper Grafana JSON on disk (BUILD-1300). No live Grafana, CloudWatch, or AMP required to pass. |

## RED (request)

| Signal | Teaching name | Notes |
|---|---|---|
| Rate | `http_server_requests_seconds_count{uri="/api/v1/payments",method="POST"}` | Completions per second, not “threads busy” |
| Errors | 5xx + timeout on that URI; 4xx (except 429) are **client**, not SLO burn by default | |
| Duration | Histogram → P50 / P99 of that URI | P99 is the teaching tail, not average |

## USE (resources)

| Resource | Utilization | Saturation | Errors |
|---|---|---|---|
| JVM heap | used / max | old-gen near full; allocation rate | OOM / allocation failure |
| CPU | process CPU / limit | run-queue / throttling | — |
| Hikari pool `jdbc/baypay` | active / max | pending threads | connection timeout |
| Tomcat / servlet threads | busy / max | queue depth | reject / 503 |

Do not put customer id, account id, `Idempotency-Key`, or PAN on metric **label** keys. Low-cardinality labels only: `uri`, `method`, `outcome`, `status`, `exception` (coarse).

## SLI / SLO (payment create)

| Field | Value |
|---|---|
| SLI | Successful `POST /api/v1/payments` / (successful + **server** failures). Server failure = 5xx, timeout, or dependency failure that becomes 5xx. Exclude 4xx except 429 if the cohort treats 429 as capacity. |
| SLO | **99.9%** monthly availability on that SLI |
| Latency SLO | P99 **< 400 ms** for a COMPLETED create on the happy path (synthetic local / teaching prod) |
| Error budget | ~43 minutes of equivalent downtime per 30-day month at 99.9% |
| Window | 30 days rolling unless a lab says otherwise |

99.99% availability is a **Module 14 architecture** target (ARCHITECT-1401), not this module’s default SLO. Do not silently upgrade the SLO in a dashboard.

## Alerts (teaching)

Page on **SLO burn** (fast and slow windows) and on **saturation** that predicts burn (Hikari pending, thread pool maxed). Do not page on “CPU > 80%” or “log line contains ERROR” as the primary page. Ticket (not page) on scrape failures and dashboard-panel errors.

## People and demo identities (synthetic)

| Role | Name |
|---|---|
| Customer | Avery Chen `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen account | `22222222-2222-2222-2222-222222222222` |
| App on-call | Riley Okonkwo |
| SRE | Priya Nair |
| Platform | Sam Okada |
| Release | Jordan Voss |
| WAS / leftover cell | Morgan Hale |

Example payment id for ops labs: `c1300a11-0000-4000-8000-111111111300`.

## What you must not do

- Log PAN, CVV, full account numbers, or live `BAYPAY_DB_PASSWORD`.
- Attach unbounded labels (`customerId`, `accountId`, `Idempotency-Key`, raw `paymentId`) to Micrometer timers.
- Require a live Prometheus/Grafana/AMP stack to pass a lab.
- Bounce `dmgr-east` or Postgres because a graph is red.
- Put instructor RCAs in this file. INCIDENT-1301 is symptoms in the student pack only.

## Optional PAKS

- `docs/19-observability/overview.md`
- `docs/27-production-failures/overview.md`
