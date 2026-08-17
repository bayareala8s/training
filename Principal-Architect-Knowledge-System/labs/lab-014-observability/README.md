---
id: lab-014-observability
title: Observability Platform
domain: observability
difficulty: advanced
estimated_hours: 8
prerequisites: [observability-fundamentals, distributed-tracing, slo-sli-error-budgets]
related_docs:
  - /docs/observability/observability-fundamentals
  - /docs/observability/distributed-tracing
  - /docs/reliability-and-resilience/slo-sli-error-budgets
status: complete
---

# Lab 014: Observability Platform

Instrument a sample service with **metrics, structured logs, and trace correlation** — RED method with Prometheus exposition.

Related chapter: [Observability Fundamentals](/docs/observability/observability-fundamentals).

## Architecture

```mermaid
flowchart TB
    Svc[Instrumented API] --> Metrics[/metrics]
    Svc --> Logs[JSON Logs]
    Svc --> Traces[/v1/traces]
    Metrics --> Prom[Prometheus]
    Prom --> Grafana[Grafana]
```

1. **Metrics** — `http_requests_total` counter with route/status labels
2. **Logs** — JSON with `trace_id`, `span_id`, `request_id`
3. **Traces** — in-memory buffer of recent correlated entries

## Quick start

```bash
cd labs/lab-014-observability
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
python -m src.main --demo
python -m src.main --serve    # http://localhost:8104
```

**Docker:**

```bash
docker compose -p lab014 -f docker/docker-compose.yml up --build -d
curl http://localhost:8104/health
chmod +x scripts/demo_observability.sh && ./scripts/demo_observability.sh
```

Grafana: http://localhost:3000 (admin/admin — lab only).

## Demo flow

| Step | Endpoint | What happens |
|------|----------|--------------|
| 1 | `POST /v1/requests/simulate` | Generate instrumented request |
| 2 | `GET /metrics` | Prometheus text exposition |
| 3 | `GET /v1/traces` | Recent correlated log entries |
| 4 | `POST /v1/chaos/inject` | Error/latency spike simulation |

**Swagger:** http://localhost:8104/docs

## Tests

```bash
pytest tests/ -v
```

## Interview discussion

**Expected signals:**

- Three pillars with correlation (trace_id in logs)
- RED vs USE — when to apply each
- Cardinality explosion risks in labels

**Red flags:**

- Logs only, no metrics SLOs
- High-cardinality labels on every user_id

## References

- [Observability Fundamentals](/docs/observability/observability-fundamentals)
- [Distributed Tracing](/docs/observability/distributed-tracing)
- OpenTelemetry specification
