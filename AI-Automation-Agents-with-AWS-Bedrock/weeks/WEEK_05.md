## Week 5 — AI Automation APIs

This week packages your workflows into an internal platform: **API Gateway + Lambda + Bedrock**, with security, throttling, contracts, and cost-aware design.

### Learning objectives

By the end of Week 5, students can:

- Build AI-powered endpoints with clear request/response contracts
- Implement validation, structured errors, and safe defaults
- Apply rate limits and throttling strategies to control cost and abuse
- Document APIs with examples and operational notes

### Core concepts (lecture notes)

- **API contracts for AI**
  - Inputs/outputs must be explicit and versionable
  - Errors must be structured and consistent
  - Correlation IDs are mandatory for debugging and audits
- **Security**
  - Auth strategy for internal APIs (choose one approach for the cohort)
  - Least privilege runtime roles
  - Logging policy: metadata over raw content; redaction
- **Rate limiting + throttling**
  - Usage plans/quotas to bound spend
  - “Fail fast” on oversized inputs or disallowed operations
- **Cost-aware request shaping**
  - max input length
  - bounded outputs
  - safe temperature defaults
  - caching where appropriate (optional)

### In-class activities (45–60 min)

- **Activity A — API spec workshop**
  - Define request/response schemas for:
    - `POST /classify`
    - `POST /summarize`
    - `POST /route`
  - Include error schema and validation rules.
- **Activity B — Abuse and cost scenario**
  - Identify two “abuse” patterns (mass requests, giant payloads).
  - Define controls (limits, throttles, rejections).

### Demos (instructor-led)

- **Demo 1**: `/classify` with strict schema validation + fallback behavior.
- **Demo 2**: Rate limiting + a structured error response for oversized payloads.

### Hands-on labs (students)

Complete:

- `LABS_GUIDE.md` → **Week 5 Labs**: Lab 5.1 and Lab 5.2

### Assignment (due end of week)

Submit:

- Working API platform with:
  - `/classify`
  - `/summarize`
  - `/route`
- Documentation:
  - example requests/responses
  - error model
  - operational notes (limits, auth, logging/redaction)
- Evidence:
  - success run logs with correlation IDs
  - one controlled failure scenario (oversize input, invalid schema, throttled call)

Rubric:

- See `ASSIGNMENTS_AND_RUBRICS.md` → **Week 5**

### Quiz (5–10 questions)

1. Why do AI endpoints need strict request/response schemas?
2. What are two ways to control cost at the API layer?
3. What should be included in a structured error response?
4. Why are correlation IDs important?
5. What information is safe to log for AI invocations?

### Architecture diagram

- [`diagrams/drawio/06-week05.drawio`](../diagrams/drawio/06-week05.drawio) · [PNG](../diagrams/png/06-week05.png) · [SVG](../diagrams/svg/06-week05.svg)

Use during live curl demos for `/classify`, `/summarize`, `/route`.

### Expected artifacts (portfolio-ready)

