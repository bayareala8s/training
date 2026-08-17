# Lab 016: Requirements

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Tool registry with JSON Schema | Must |
| FR-2 | Agent runtime loop (plan/execute) | Must |
| FR-3 | Policy engine with deny/allow/approve | Must |
| FR-4 | Human approval workflow | Must |
| FR-5 | Session memory | Must |
| FR-6 | Audit log per tool invocation | Must |
| FR-7 | Token budget per tenant | Should |
| FR-8 | max_steps termination | Must |

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Policy check latency | < 10ms local |
| NFR-2 | Audit write durability | Persist before tool returns |
| NFR-3 | No runaway loops | max_steps default 10 |

## Acceptance Criteria

### AC-1: Policy block

Denied tool never executes; audit records denial.

### AC-2: Approval flow

`send_email` enters pending; resumes after approval.

### AC-3: Budget

Exceeding token budget terminates run with clear error.

## Out of Scope

- Arbitrary code interpreter tools
- Multi-agent swarm coordination
- Production identity federation

## Related Documentation

- [Agent Platform Architecture](/docs/agentic-ai-architecture/agent-platform-architecture)
