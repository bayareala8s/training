## Instructor Quiz Answer Keys

Answers for weekly quizzes in `weeks/WEEK_01.md` … `weeks/WEEK_08.md`. Accept reasonable variations; use for grading and discussion.

---

### Week 1

1. **Rules vs LLM:** Deterministic routing (e.g., known billing keywords), compliance checks with fixed logic, or sub-millisecond latency requirements where model variance is unacceptable.
2. **Structured outputs:** Enable reliable parsing, downstream automation, validation gates, and audit without fragile string parsing.
3. **Risks + mitigations (examples):** Hallucination → validation + human review; data leakage → redaction and least-privilege IAM; cost overrun → input limits and budgets; prompt injection → allow-listed tools and policy layer.
4. **LLM cost drivers:** Input/output token count, model tier, request volume, retries, and context window size.
5. **Low-confidence fallback:** Route to `human_review`, use rules-based default, or return a safe structured error — never silently guess.
6. **Never log:** Raw PII/PHI, secrets/credentials, full prompts/responses with sensitive content, API keys.

---

### Week 2

1. **Model selection criteria:** Accuracy on golden set, latency p95, cost per 1K tokens, context length, and structured-output reliability.
2. **Prompt versioning:** Prompts are production config; versioning enables rollback, A/B evaluation, and change control like application code.
3. **Golden set:** Curated labeled examples used to regression-test prompt/model changes before release.
4. **Least privilege (IAM):** Lambda/service role gets only `bedrock:InvokeModel`/`Converse` on specific foundation models — no `*` on Bedrock or unrelated services.
5. **Raw prompt logging risk:** Exposes customer data, violates compliance, increases breach impact, and creates retention/legal discovery obligations.

---

### Week 3

1. **JSON-only output:** Machines can validate schema, branch deterministically, and reject malformed responses without NLP parsing.
2. **Confidence validation:** Type is number, range 0–1, reject NaN; compare to threshold; trigger fallback below threshold.
3. **Non-JSON response:** Retry with stricter prompt, parse repair attempt, then fallback to `human_review` or rules path — log validation failure in audit.
4. **Hybrid rules + AI:** Rules handle known high-precision cases cheaply; AI handles ambiguous cases — reduces cost and improves explainability.
5. **Ambiguous classification fallback:** `human_review` queue or `general` bucket with low-confidence flag.

---

### Week 4

1. **Retry vs fallback:** Retry transient errors (throttling, timeouts); fallback immediately on validation failures or business logic errors that won't self-heal.
2. **Idempotency:** Same input produces same side effects once; critical for Step Functions retries and safe replays without duplicate tickets/charges.
3. **Compensating action example:** Mark workflow failed in DynamoDB, send rollback notification, or create reversal ticket after partial persist.
4. **Resilience evidence:** Execution history showing retry → success, or failure → Catch → fallback path with audit correlation ID.
5. **Timeouts:** Prevent hung workflows, bound cost, and trigger Catch blocks for predictable failure handling.

---

### Week 5

1. **Strict schemas:** Contract between clients and automation; enables validation, versioning, and safe evolution of AI endpoints.
2. **API cost controls:** Request size limits, rate limiting/throttling, model selection per route, caching for repeated inputs.
3. **Structured error response:** `error` code, `correlation_id`, optional `max_chars`/`details` — never stack traces or internal ARNs to clients.
4. **Correlation IDs:** Tie API request → Lambda → Step Functions → audit rows for end-to-end debugging.
5. **Safe to log:** Model ID, token/size counts, latency, validation status, route decision, correlation ID — not raw user text with PII.

---

### Week 6

1. **Correlation ID:** Unique request identifier propagated across services to query audit trail and trace a single user action.
2. **Safe audit fields:** Timestamp, model ID, input/output byte counts, validation status, route/action, latency_ms.
3. **Never log:** Secrets, full credit card/SSN content, passwords, unredacted customer payloads.
4. **Alerts should detect:** Error rate spikes, validation failure rate, latency p95 breach, throttling, or unusual invocation volume.
5. **Human approval triggers:** High-risk keywords, low confidence, policy violations, production-impacting actions, or `action_stub` tool paths.

---

### Week 7

1. **Agent components:** Planner (model), tool registry, policy/allow-list, memory store, audit layer, and optional human-in-the-loop gate.
2. **Allow-listed tools:** Prevents arbitrary code execution and limits blast radius of prompt injection or model mistakes.
3. **Safe memory:** Store summaries/metadata in DynamoDB with TTL — not raw secrets or full conversation transcripts with PII.
4. **Idempotent consumers:** EventBridge/Lambda retries can duplicate delivery; idempotency keys prevent double-processing.
5. **Escalate to human:** Low plan confidence, risky keywords, disallowed tool request, or `requires_approval` in structured plan.

---

### Week 8

1. **Minimum bar components:** Orchestration, Bedrock + structured outputs, validation/fallback, persistence, dashboard + alert, audit trail, cost controls.
2. **Demo failure scenario:** Show validation rejection, throttling retry, or approval gate — prove safe degradation not silent failure.
3. **Scope control:** One capstone option done well beats four half-finished; document what's in/out of scope.
4. **Ops readiness:** Runbook with symptoms → checks → mitigations; alert tested with evidence screenshot.
5. **Capstone option mapping:** A = Ops assistant (Option 1), B = File automation (Option 2), C/D map to workflow engine or API platform — see `CAPSTONE_HANDBOOK.md` mapping table.
6. **Portfolio evidence:** Repo, architecture diagram, correlation ID audit query, dashboard screenshot, cost analysis.

---

*Instructor use only — do not publish answer keys to students before the quiz.*
