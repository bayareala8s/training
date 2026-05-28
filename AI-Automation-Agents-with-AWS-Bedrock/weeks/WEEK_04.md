## Week 4 — Orchestrating AI with Step Functions

This week operationalizes decision engines into reliable workflows using **Step Functions**: retries/backoff, failure handling, idempotency, and safe replays.

### Learning objectives

By the end of Week 4, students can:

- Design Step Functions workflows for multi-step AI automation
- Implement retries/backoff, timeouts, and catch/fallback branches
- Apply idempotency patterns and explain safe replay behavior
- Prove resilience with failure simulation and a short reliability report

### Core concepts (lecture notes)

- **Why orchestration matters**
  - Reliability, traceability, auditable run history, consistent error handling
- **Retry and backoff**
  - Retries are for transient errors (throttling, timeouts, temporary failures)
  - Use exponential backoff; cap attempts; separate transient vs permanent failures
- **Timeouts**
  - Prevent stuck workflows; decide when to abandon and fallback
- **Catch/fallback**
  - Validation failure → deterministic fallback path
  - Downstream action failure → compensating action or “needs review”
- **Idempotency**
  - Define idempotency keys for external side effects
  - Store request/result mapping to allow safe retries and replays
- **Failure simulation**
  - Design workflows to be tested under failure conditions, not only happy paths

### In-class activities (45–60 min)

- **Activity A — Workflow storyboard**
  - Sketch: invoke → validate → branch → persist → notify
  - Annotate: retries, timeouts, error types, fallback destinations
- **Activity B — Idempotency design**
  - Choose a side effect (ticket creation, record write, notification).
  - Define: idempotency key, storage location, and replay behavior.

### Demos (instructor-led)

- **Demo 1**: Step Functions state machine: classify → validate → act → persist.
- **Demo 2**: Inject errors (throttle, validation failure) and show recovery paths.

### Architecture diagram

- [`diagrams/drawio/05-week04.drawio`](../diagrams/drawio/05-week04.drawio) · [PNG](../diagrams/png/05-week04.png) · [SVG](../diagrams/svg/05-week04.svg)

Pair with the Step Functions execution graph during the failure-injection lab.

### Student diagrams

- **Sequence:** [seq-week04](../diagrams/student/png/seq-week04.png) — retry vs catch on one execution
- **Cheat sheet:** [cheat-week04](../diagrams/student/png/cheat-week04.png) — states, retry/catch, idempotency

### Hands-on labs (students)

Complete:

- `LABS_GUIDE.md` → **Week 4 Labs**: Lab 4.1 and Lab 4.2

### Assignment (due end of week)

Submit:

- **State machine definition + diagram**
  - includes retries/backoff and catch/fallback
- **Reliability evidence**
  - run history + logs for happy path
  - run history + logs for at least one failure injection
- **Retry automation report** (1–2 pages)
  - what failed, how it retried, where it ended, and why

Rubric:

- See `ASSIGNMENTS_AND_RUBRICS.md` → **Week 4**

### Quiz (5–10 questions)

1. When should you retry vs fallback immediately?
2. What is idempotency and why does it matter for replays?
3. Give one example of a compensating action.
4. What evidence would you provide to prove resilience?
5. Why are timeouts important in orchestration workflows?

### Expected artifacts (portfolio-ready)

- Step Functions workflow with real error handling and idempotency strategy
- Failure simulation report and run evidence

