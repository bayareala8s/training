## Week 7 — Enterprise AI Agent Systems

This week introduces agentic systems as **governed automation**: routing, tool selection, memory, and event-driven chaining—without sacrificing safety and auditability.

### Learning objectives

By the end of Week 7, students can:

- Explain core agent components: router/planner, tools, memory, policies/guardrails
- Implement an agent-like router that chooses workflows/tools safely
- Add a simple memory pattern (session + durable store with TTL) with strict constraints
- Chain workflows with events while maintaining idempotency and traceability

### Core concepts (lecture notes)

- **What an “agent” is in enterprise contexts**
  - Not magic autonomy; it’s a controlled system that:
    - interprets intent
    - selects an allowed tool/workflow
    - validates and logs decisions
    - escalates when risky or uncertain
- **Tool execution safety**
  - Define an allow-list of actions/tools
  - Require approvals for high-risk actions
  - Enforce structured plans and strict validation
- **Memory patterns**
  - Session memory: short summary of relevant context
  - Durable memory: DynamoDB record keyed by user/session with TTL
  - Never store secrets/raw sensitive text; store summaries and metadata
- **Event-driven chaining**
  - Use events to decouple components and scale
  - Idempotent consumers (dedupe by correlation/event ID)
  - Audit trail across the chain

### In-class activities (45–60 min)

- **Activity A — Agent policy design**
  - Define allowed tools/actions, disallowed actions, and approval triggers.
- **Activity B — Memory safety checklist**
  - Decide what fields may be stored in memory and their TTL.

### Demos (instructor-led)

- **Demo 1**: Routing agent produces a structured “plan JSON” selecting a workflow.
- **Demo 2**: Memory read/write with TTL and safe summaries.
- **Demo 3**: EventBridge chain: event → router → workflow → audit → notification (stub).

### Hands-on labs (students)

Complete:

- `LABS_GUIDE.md` → **Week 7 Labs**: Lab 7.1 and Lab 7.2

### Assignment (due end of week)

Submit:

- **Agent workflow**
  - routing policy + structured plan output
  - tool selection enforcement
- **Memory implementation**
  - DynamoDB (recommended) with TTL
  - documented “what we store” and “what we never store”
- **Event chaining evidence** (if used)
  - correlation IDs across events and runs

Rubric:

- See `ASSIGNMENTS_AND_RUBRICS.md` → **Week 7**

### Quiz (5–10 questions)

1. What are the main components of an enterprise AI agent system?
2. Why should tool execution be allow-listed?
3. What is one safe way to store memory for an agent?
4. Why must event-driven consumers be idempotent?
5. When should an agent escalate to human review?

### Architecture diagram

- [`diagrams/drawio/08-week07.drawio`](../diagrams/drawio/08-week07.drawio) · [PNG](../diagrams/png/08-week07.png) · [SVG](../diagrams/svg/08-week07.svg)

Contrast the diagram's **tool policy** box with hype about "fully autonomous agents."

### Expected artifacts (portfolio-ready)

