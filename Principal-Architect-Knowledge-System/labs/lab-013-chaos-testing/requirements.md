# Lab 013: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Fault injector (latency, errors, dep down) | Must |
| FR-2 | YAML experiment manifest | Must |
| FR-3 | Experiment runner with duration | Must |
| FR-4 | Abort on SLO breach | Must |
| FR-5 | Blast radius targeting | Must |
| FR-6 | Markdown report output | Should |
| FR-7 | Demo service with /api/work | Must |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Fault toggle latency | < 100ms |
| NFR-2 | Abort reaction time | < 30s after breach |
| NFR-3 | Reproducible experiments | Manifest-driven |

## Acceptance Criteria

### AC-1: Latency fault

500ms injection → p99 latency increase measurable.

### AC-2: Abort

Set `error_rate_gt: 0.1`; inject 50% errors → experiment aborts.

### AC-3: Report

Report file includes hypothesis and pass/fail vs hypothesis.

## Out of Scope

- Kubernetes cluster chaos
- Production AWS FIS integration
- Automated remediation

## Related Documentation

- [Resilience Patterns](/docs/microservices/resilience-patterns)
