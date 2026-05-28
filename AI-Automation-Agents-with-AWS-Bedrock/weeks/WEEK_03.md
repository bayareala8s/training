## Week 3 — AI Decision Engines & Structured Outputs

This week builds the core reliability mechanism for AI automation: **structured outputs + deterministic validation + safe fallbacks**.

### Learning objectives

By the end of Week 3, students can:

- Produce strict JSON outputs suitable for downstream automation
- Validate model outputs deterministically (schema, enums, bounds, length limits)
- Build routing decisions with confidence thresholds and fallbacks
- Combine AI + rules to improve reliability and governance

### Core concepts (lecture notes)

- **Structured outputs**
  - “JSON-only” responses with explicit keys, enums, and numeric bounds
  - Bounded reasoning: short `reason` field, max length, no sensitive content
- **Validation**
  - Parse JSON strictly; reject anything else
  - Validate types, required fields, enums, bounds, and max lengths
  - Treat validation failures as expected events with safe handling
- **Confidence scoring**
  - Confidence may be produced by the model, but must be validated and used cautiously
  - Use thresholds to decide: auto-route vs fallback/human review
- **Hybrid AI + rules**
  - Rules first for obvious cases and compliance constraints
  - AI for ambiguity and natural language variety
  - Deterministic fallback for low confidence and invalid outputs

### In-class activities (45–60 min)

- **Activity A — Define your schema**
  - Create an output schema for classification and routing:
    - `label` enum
    - `confidence` 0..1
    - `route` enum
    - `reason` bounded string
- **Activity B — Failure mode rehearsal**
  - Identify 5 ways outputs can fail (missing keys, invalid JSON, invalid enum, too long, low confidence).
  - Define fallback handling for each.

### Demos (instructor-led)

- **Demo 1**: Prompt that enforces JSON-only + schema-guided output.
- **Demo 2**: Validator rejects malformed output and triggers a safe default.

### Hands-on labs (students)

Complete:

- `LABS_GUIDE.md` → **Week 3 Labs**: Lab 3.1 and Lab 3.2

### Assignment (due end of week)

Submit:

- **Decision engine implementation**
  - classification + routing outputs
  - strict schema + validator + tests
- **Fallback strategy**
  - deterministic fallback behavior
  - low-confidence routing policy and rationale
- **API contract**
  - example request/response payloads
  - error response format

Rubric:

- See `ASSIGNMENTS_AND_RUBRICS.md` → **Week 3**

### Quiz (5–10 questions)

1. Why is JSON-only output preferred for automation workflows?
2. What validations would you apply to a `confidence` field?
3. What should happen when the model returns non-JSON text?
4. Give one benefit of hybrid rules + AI routing.
5. What is a good deterministic fallback for ambiguous classification?

### Architecture diagram

- [`diagrams/drawio/04-week03.drawio`](../diagrams/drawio/04-week03.drawio) · [PNG](../diagrams/png/04-week03.png) · [SVG](../diagrams/svg/04-week03.svg)

Walk through all **6 failure modes** on the diagram before students start the validation lab.

### Student diagrams

- **Sequence:** [seq-week03](../diagrams/student/png/seq-week03.png) — one request through classify → validate → route
- **Cheat sheet:** [cheat-week03](../diagrams/student/png/cheat-week03.png) — schema, validator, confidence gate
- **Anti-pattern:** [pattern-week03](../diagrams/student/png/pattern-week03.png) — raw LLM vs production pattern

### Expected artifacts (portfolio-ready)
- Documented fallback and confidence policy

