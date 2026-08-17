## AI Automation & Agents with AWS Bedrock — Labs Guide

This guide provides **step-by-step labs** with acceptance criteria and troubleshooting hints. Labs are designed to be “production-minded”: structured outputs, validation, retries, idempotency, observability, and cost controls.

### Runnable lab code (AWS)

**Deployable implementations** live in [`labs/`](labs/README.md):

- Week 1: local Bedrock scripts
- Weeks 2–8: AWS SAM stack (Lambda, API Gateway, Step Functions, DynamoDB, CloudWatch)
- **Full test cycle (deploy → verify → teardown)**: `cd labs && ./scripts/cycle.sh`
- Start stack: `./scripts/start.sh` | Stop/teardown: `./scripts/stop.sh`
- Unit tests only: `./scripts/run-tests.sh`

### Lab conventions (use across all weeks)

- **Naming**: prefix resources with `ba-la8s-ai-<student|team>-<week>-<lab>`
- **Correlation ID**: every request includes a `correlation_id` (UUID) propagated into logs and stored with outputs.
- **Structured outputs**: LLM outputs must be valid JSON meeting a schema.
- **Validation**: reject invalid outputs and trigger a deterministic fallback.
- **Safety**: never log secrets; redact any user content that may contain credentials/PII.

---

## Week 1 Labs — First Bedrock Invocation + Cost/Latency Basics

### Lab 1.1 — Invoke a Bedrock model (Python)

**Goal**: Make a single model invocation and capture latency + token usage (or best proxy available).

**Tasks**

- Configure AWS CLI credentials for a sandbox account.
- Create a small Python script that:
  - sends a prompt to a Bedrock model
  - prints the response
  - captures timing (start/end) and logs it

**Acceptance criteria**

- Script runs successfully and prints a response.
- Output includes latency measurement.
- A short write-up explains:
  - model chosen
  - why temperature was set as it was
  - observed latency

**Troubleshooting**

- Access errors usually mean model access isn’t enabled or IAM permissions are missing.
- Throttling: add a short retry with exponential backoff for transient errors.

### Lab 1.2 — Compare outputs across prompts/settings

**Goal**: Evaluate response differences under varying prompts/settings.

**Tasks**

- Run the same task using:
  - two prompt variants (strict vs open-ended)
  - two temperatures (e.g., low vs moderate)
- Record differences in:
  - output quality
  - consistency
  - latency (roughly)

**Acceptance criteria**

- A short table comparing the runs (prompt/settings → observations).
- A conclusion with a recommended default configuration for “automation workloads”.

---

## Week 2 Labs — Secure Bedrock Integration + Prompt Evaluation

### Lab 2.1 — Least-privilege Bedrock invocation from Lambda

**Goal**: Invoke Bedrock from Lambda using a least-privilege role.

**Tasks**

- Create a Lambda function that invokes a Bedrock model.
- Create an IAM role for the Lambda with only the permissions needed.
- Log:
  - correlation ID
  - model ID (non-sensitive)
  - latency
  - success/failure status (no sensitive content)

**Acceptance criteria**

- Lambda can invoke the model successfully.
- IAM policy is least-privilege (no `*` on all actions/resources unless justified).
- Logs demonstrate correlation ID and timing.

**Troubleshooting**

- If invocation fails in Lambda but works locally, verify:
  - correct region
  - correct execution role policy
  - VPC config (if used) and endpoints

### Lab 2.2 — Prompt versioning + evaluation harness

**Goal**: Create a lightweight evaluation workflow for prompts.

**Tasks**

- Define a “golden set” of 10–20 test cases in JSON.
- Create a script that:
  - runs each case against prompt version A and B
  - collects outputs
  - scores results using a simple rubric (pass/fail or 1–5)

**Acceptance criteria**

- A `prompt_eval_results` artifact (markdown or JSON) showing:
  - test cases
  - results
  - summary scores
- A decision note: which prompt version wins and why.

---

## Week 3 Labs — Structured Outputs + Decision Engine

### Lab 3.1 — Structured JSON classification output

**Goal**: Force a strict JSON response for classification.

**Required output shape (example)**

- `label`: one of a fixed enum
- `confidence`: number \(0..1\)
- `reason`: short string (bounded length)

**Tasks**

- Write a prompt that requires **only JSON** output.
- Implement a validator that:
  - ensures valid JSON
  - enforces `label` ∈ allowed set
  - enforces `confidence` bounds
  - enforces max length on `reason`

**Acceptance criteria**

- Invalid outputs are rejected.
- On rejection, system returns a deterministic fallback (e.g., `label="unknown"`).
- Unit tests (or simple test runner) cover:
  - valid response
  - invalid JSON
  - invalid enum
  - missing fields

### Lab 3.2 — Routing engine (AI + rules hybrid)

**Goal**: Route a request to a handler using rules + AI.

**Tasks**

- Implement rules for obvious cases (keywords, known patterns).
- If rules don’t decide, call the model to decide route.
- Use confidence thresholding:
  - if confidence < threshold → fallback route or human review queue

**Acceptance criteria**

- Demonstrates:
  - rules hit
  - AI decision hit
  - low-confidence fallback path
- Logs include:
  - correlation ID
  - route selected
  - confidence

---

## Week 4 Labs — Step Functions Orchestration + Resilience

### Lab 4.1 — Orchestrate classify → validate → act

**Goal**: Build a state machine that calls Bedrock, validates output, then runs an action.

**Tasks**

- Create a Step Functions workflow with:
  - task: invoke model
  - task: validate output
  - choice: valid vs invalid
  - task: action (stub) + persist result

**Acceptance criteria**

- State machine succeeds on valid outputs.
- Invalid outputs follow the fallback path.
- Workflow includes retries with exponential backoff for transient errors.

### Lab 4.2 — Failure simulation

**Goal**: Prove reliability via failure injection.

**Tasks**

- Force failures (at least two):
  - throttling / rate limit
  - validator failure
  - downstream action timeout
- Capture evidence: logs, screenshots, or structured run history.

**Acceptance criteria**

- A short “retry report” describing:
  - what failed
  - how it retried
  - where it stopped and why (if it stopped)

---

## Week 5 Labs — AI Automation APIs

### Lab 5.1 — Build `/classify`, `/summarize`, `/route`

**Goal**: Build a small API platform.

**Tasks**

- Create API Gateway endpoints backed by Lambda:
  - `POST /classify`
  - `POST /summarize`
  - `POST /route`
- Enforce request schema validation (at API layer or Lambda).
- Implement response schema validation (in Lambda).

**Acceptance criteria**

- Each endpoint has:
  - example request/response
  - error response format
  - correlation ID propagated
- Rate limiting is configured (usage plan or Lambda controls).

### Lab 5.2 — Cost-aware request shaping

**Goal**: Add cost controls to prevent runaway usage.

**Tasks**

- Enforce:
  - max input length
  - max output length
  - safe default temperature
- Add simple caching where appropriate (optional).

**Acceptance criteria**

- Requests exceeding limits return a structured error.
- A short note explains chosen limits and tradeoffs.

---

## Week 6 Labs — Observability + Governance

### Lab 6.1 — Audit pipeline for AI interactions

**Goal**: Create an audit trail of AI inputs/outputs with redaction.

**Tasks**

- Emit an “AI interaction event” containing:
  - correlation ID
  - timestamp
  - model ID
  - input/output sizes (not raw secrets)
  - validation status
  - route/action taken
- Store events in DynamoDB or S3.

**Acceptance criteria**

- You can retrieve audit events for a correlation ID.
- Evidence demonstrates redaction/avoidance of sensitive logging.

### Lab 6.2 — CloudWatch dashboard + alerts

**Goal**: Build monitoring for reliability and spend proxies.

**Tasks**

- Dashboard includes:
  - request count
  - error rate
  - p95 latency (or proxy)
  - retries
  - validation failures
- Add at least one alert (e.g., error rate spike).

**Acceptance criteria**

- Screenshots or exported dashboard definition.
- Alert triggers in a controlled test scenario (`labs/week06/trigger_alarm.py` after `source .stack.env`).

---

## Week 7 Labs — Agent System Patterns

### Lab 7.1 — Routing “agent” workflow

**Goal**: Implement an agent-like router that chooses tools/workflows safely.

**Tasks**

- Build a router that chooses among:
  - summarize workflow
  - classify + route workflow
  - action workflow (stub)
- Enforce a tool policy:
  - allowed actions list
  - approval required for risky actions

**Acceptance criteria**

- Demonstrates tool selection via structured plan output.
- Logs include correlation ID + tool chosen + policy decision.

### Lab 7.2 — Memory pattern

**Goal**: Persist minimal “memory” safely.

**Tasks**

- Store:
  - session context summary (not raw secrets)
  - last route/action
  - timestamps
- Use DynamoDB with TTL (recommended).

**Acceptance criteria**

- Memory retrieved and used to influence routing.
- Clear constraints documented on what is stored and what is forbidden.

---

## Week 8 — Capstone build sprint

Capstone details and rubrics are in `CAPSTONE_HANDBOOK.md`.

**Runnable capstone labs:** [`labs/week08/README.md`](labs/week08/README.md)

### Lab 8.1 — Option A: Incident Triage Platform

**Goal**: End-to-end incident triage with summarize, classify, route, ticket stub, and audit.

```bash
curl -sS -X POST "$API_ENDPOINT/capstone/incident" \
  -H "Content-Type: application/json" \
  -d '{"text":"API 503 in production","correlation_id":"lab8-a-1"}' | jq .
```

**Acceptance criteria**: Returns `ticket_stub`, `summary`, classification, routing; audit retrievable by correlation ID.

### Lab 8.2 — Option B: Document Classification Platform

**Goal**: Classify document excerpts and route to processing queues with validation.

```bash
curl -sS -X POST "$API_ENDPOINT/capstone/document" \
  -H "Content-Type: application/json" \
  -d '{"document_text":"INVOICE #123 Amount $500","correlation_id":"lab8-b-1"}' | jq .
```

**Acceptance criteria**: Valid JSON `doc_type`, `queue`, confidence gate to `human_review` when low.

### Lab 8.3 — Option C: Approval Workflow

**Goal**: High-risk actions require approval; low-risk auto-execute.

```bash
# Request
curl -sS -X POST "$API_ENDPOINT/capstone/approval/request" \
  -d '{"action_text":"Delete production DB","correlation_id":"lab8-c-1"}' | jq .
# Decide (use approval_id from response)
curl -sS -X POST "$API_ENDPOINT/capstone/approval/decide" \
  -d '{"approval_id":"APR-...","decision":"approve","correlation_id":"lab8-c-1"}' | jq .
```

**Acceptance criteria**: Pending → approved flow; DynamoDB approval record; audit events.

### Lab 8.4 — Option D: Enterprise Agent

**Goal**: Governed agent with tool policy routing to capstone services.

```bash
curl -sS -X POST "$API_ENDPOINT/capstone/agent" \
  -d '{"text":"Summarize DB failover incident","session_id":"s1","correlation_id":"lab8-d-1"}' | jq .
```

**Acceptance criteria**: Tool selection, policy decision, memory update, audit event.

### Verify all capstone labs

```bash
cd labs && ./scripts/verify-capstone.sh
```

