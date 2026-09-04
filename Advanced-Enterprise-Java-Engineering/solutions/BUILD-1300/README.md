# BUILD-1300 — Instructor solution

**Do not share these files with students before they submit a complete dashboard JSON.**

This folder is the answer key for the paper operations board. Students are not required to run Grafana, Prometheus, AMP, or CloudWatch.

## Files

| File | Role |
|---|---|
| [dashboard.json](dashboard.json) | Complete Grafana-style home board: RED + USE + 99.9% SLO / burn |

A student file that has the same panels and contracts passes even if they used `stat` instead of `gauge`, named Tomcat threads `tomcat_threads_*` versus a servlet-executor alias, or split Hikari active and pending into two panels.

## What the starter got wrong

- Valid-looking Grafana export: title, datasource `aeje-prom-paper`, job template, **one** rate panel.
- Missing **errors (5xx)**.
- Missing **P99** duration (histogram quantile).
- Missing **SLO 99.9%** SLI tile and **error-budget / burn**.
- Missing **Hikari** `jdbc/baypay` active/pending (and the rest of USE: heap, servlet threads).

The starter was a plausible draft. It cannot brief an on-call.

## Required contracts

```text
RED:   rate + 5xx + P99 for POST /api/v1/payments
       http_server_requests_seconds_count / _bucket
       4xx are client (except optional 429 call-out)
USE:   jvm_memory_used_bytes / max (heap)
       hikaricp_connections_active|pending|max{pool="jdbc/baypay"}
       tomcat_threads_busy_threads / tomcat_threads_config_max_threads
SLO:   99.9% availability SLI (NOT 99.99%)
       error budget ~43 min / 30d; burn = error_ratio / 0.001
labels: uri, method, outcome, status (optional coarse exception)
forbid: customerId, accountId, Idempotency-Key, paymentId, PAN
validate: read the JSON; optional python json.load
live:   not required
```

## PromQL teaching shapes

Rate:

```text
sum(rate(http_server_requests_seconds_count{uri="/api/v1/payments",method="POST"}[5m]))
```

P99:

```text
histogram_quantile(0.99, sum by (le) (rate(http_server_requests_seconds_bucket{uri="/api/v1/payments",method="POST"}[5m])))
```

SLI (30d) versus 99.9%:

```text
1 - (5xx rate / all-completions rate)
```

Burn (fast 5m, slow 1h):

```text
(5xx ratio) / 0.001
```

## Diagram

AEJE-D-061: merchants → payment-service → `/actuator/prometheus` → paper Grafana with RED, USE, and 99.9% burn.

## Scoring notes

Full marks require P99, 99.9% (not 99.99%), Hikari active **and** pending, and no merchant identifiers on labels. A rate-only file is a failed Technical score. Grafana / AMP absence must not fail the lab. Opening this folder before the student lists the missing panels fails Diagnostic method.
