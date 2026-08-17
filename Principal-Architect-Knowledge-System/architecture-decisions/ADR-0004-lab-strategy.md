# ADR-0004: Lab Strategy

## Status

Accepted

## Date

2026-07-24

## Context

Hands-on labs reinforce distributed-systems concepts. Labs must be reproducible, testable, and safe for local and cloud execution.

## Decision Drivers

- Reproducible local development
- Automated tests for correctness
- Failure injection for learning
- Cost awareness for cloud labs
- Multi-language support (Python, Go, Java, TypeScript)

## Considered Options

1. **Local-first with Docker, optional AWS** (LocalStack, Kind)
2. **Cloud-only labs** (AWS accounts required)
3. **Simulation-only** (no real infrastructure)

## Decision Outcome

Chosen option: **Local-first with Docker, optional AWS**, because it maximizes accessibility while allowing production-realistic cloud labs where valuable.

### Positive Consequences

- Labs runnable without cloud accounts for core algorithms
- Docker Compose for multi-service labs
- LocalStack and Kind for AWS/Kubernetes simulation
- Cloud labs include explicit cost warnings

### Negative Consequences

- LocalStack does not perfectly mirror AWS behavior
- Docker resource requirements on developer machines

## Lab Structure

Each lab directory contains: `README.md`, `architecture.md`, `requirements.md`, `src/`, `tests/`, `infra/`, `docker/`, `observability/`, `failure-tests/`, `solutions/`.

## Links

- `.cursor/rules/labs.mdc`
- `templates/lab-template.md`
- `labs/` directory
