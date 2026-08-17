# Lab 013: Architecture

## Overview

**Closed-loop chaos** — hypothesize, inject, measure, learn — aligned with principled chaos engineering practice.

```mermaid
flowchart LR
    subgraph Control Plane
        M[Experiment Manifest]
        R[Runner]
        A[Abort Controller]
    end
    subgraph Data Plane
        S[Service Under Test]
        D[Dependencies]
    end
    subgraph Observability
        P[Prometheus]
        B[Error Budget]
    end
    M --> R
    R --> S
    R --> D
    S --> P
    P --> B
    B --> A
    A --> R
```

## Experiment Lifecycle

```mermaid
sequenceDiagram
    participant Op as Operator
    participant R as Runner
    participant S as Service
    participant M as Metrics

    Op->>R: start experiment
    R->>S: enable fault
    loop duration
        R->>M: sample SLI
        M-->>R: success_rate, latency
        alt abort condition
            R->>S: disable fault
            R-->>Op: ABORTED
        end
    end
    R->>S: disable fault
    R-->>Op: report
```

## Experiment Manifest (YAML)

```yaml
name: dep-slow
hypothesis: "Degraded dependency increases latency but error rate stays < 1%"
fault:
  type: dependency_latency
  target: redis
  latency_ms: 500
duration_seconds: 120
blast_radius:
  instances: ["demo-1"]
abort_on:
  error_rate_gt: 0.05
  success_rate_lt: 0.99
```

## Safety Properties

| Property | Mechanism |
|----------|-----------|
| Blast radius | Target tags / single instance |
| Abort | Automated SLO breach detection |
| Audit | Experiment log with timestamps |

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `FaultInjector` | Apply/remove faults |
| `ExperimentRunner` | Orchestrate lifecycle |
| `SLICollector` | Pull metrics |
| `ErrorBudget` | Track burn during experiment |
| `ReportGenerator` | Game day summary |

## Docker Topology

`demo-service`, `redis`, `prometheus` (optional), `chaos-runner`.

## Related Documentation

- [Chaos Engineering](/docs/reliability-and-resilience/chaos-engineering)
- [SLO, SLI, and Error Budgets](/docs/reliability-and-resilience/slo-sli-error-budgets)
