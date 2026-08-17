# Lab 014: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | HTTP RED metrics | Must |
| FR-2 | JSON structured logging | Must |
| FR-3 | OpenTelemetry traces to Jaeger | Must |
| FR-4 | Prometheus scrape target | Must |
| FR-5 | Grafana dashboard stub | Should |
| FR-6 | SLO PromQL rules file | Should |
| FR-7 | Trace context propagation | Must |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Instrumentation overhead | < 5% latency increase |
| NFR-2 | Metric cardinality | < 100 label combinations |
| NFR-3 | Trace export success | > 99% local |

## Acceptance Criteria

### AC-1: Metrics

10 requests → `http_requests_total` increases by 10.

### AC-2: Traces

Jaeger UI shows trace with ≥2 spans for downstream call.

### AC-3: Log correlation

Log line contains same `trace_id` as Jaeger trace.

## Out of Scope

- Full OpenTelemetry Collector pipelines
- Production HA for observability backend
- Log aggregation at scale (Loki/ELK deploy)

## Related Documentation

- [SLO, SLI, and Error Budgets](/docs/reliability-and-resilience/slo-sli-error-budgets)
