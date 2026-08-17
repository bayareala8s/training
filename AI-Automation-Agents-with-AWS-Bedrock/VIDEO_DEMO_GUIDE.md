# Video Demo Guide — AI Automation & Agents with AWS Bedrock

Step-by-step instructions to run and record every lab for LinkedIn / Loom videos.

**Verified on AWS:** August 10, 2026 · Account `277374794397` · Region `us-east-1` · Model `amazon.nova-lite-v1:0`

**Course page:** https://baylearn.bayareala8s.com/courses/9d6c8974-eab4-45b3-aa0d-a058b9cda228/

---

## Before you record (one-time setup)

### Prerequisites

| Item | Check |
|------|-------|
| AWS CLI configured | `aws sts get-caller-identity` |
| Bedrock model access | Enable **Amazon Nova Lite** in `us-east-1` |
| Python 3.11+ | `python3 --version` |
| SAM CLI | Installed in `labs/.venv/bin/sam` after `pip install -r requirements.txt` |

### Terminal setup (run once per session)

```bash
cd labs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION=us-east-1
export PROJECT_PREFIX=ba-la8s-ai-demo          # change to your name for real use
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
```

### Deploy the full stack (Weeks 2–8)

```bash
./scripts/labs.sh start
source .stack.env    # loads API_ENDPOINT, STATE_MACHINE_ARN, etc.
```

**Expected:** Stack `ba-la8s-ai-demo-course-labs` reaches `CREATE_COMPLETE` (~2–3 min).

### When finished recording

```bash
./scripts/stop.sh    # deletes stack — stops most AWS charges
```

---

## Video structure (recommended)

| Segment | Duration | Content |
|---------|----------|---------|
| Intro | 0:30 | Course pitch + reference architecture diagram |
| Week 1 | 1:30 | Local Bedrock scripts |
| Deploy | 0:45 | `./scripts/start.sh` |
| Weeks 2–8 | 8:00 | One segment per week (commands below) |
| Teardown | 0:30 | `./scripts/stop.sh` + BayLearn CTA |
| **Total** | **~12 min** | Or split into 8 short LinkedIn clips |

**Diagrams to show on screen:** `diagrams/png/01-reference.png`, `diagrams/student/png/seq-week03.png`, etc.

---

## Week 1 — First Bedrock invocation (local, no deploy)

**What students learn:** Call Bedrock from Python, measure latency, compare prompt settings.

**Show on screen:** Terminal + `week01/invoke_bedrock.py`

### Lab 1.1 — Single invocation

```bash
cd labs
source .venv/bin/activate
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

python week01/invoke_bedrock.py --prompt "Explain AWS Step Functions in one sentence."
```

**Say on camera:** *"Week 1 is local — no AWS deploy yet. Students learn Bedrock basics: model ID, temperature, and latency before we touch serverless."*

**Expected output (verified):**
```json
{
  "latency_ms": 1104,
  "model_id": "amazon.nova-lite-v1:0",
  "usage": { "inputTokens": 8, "outputTokens": 29, "totalTokens": 37 }
}
```

### Lab 1.2 — Compare prompts / temperatures

```bash
python week01/compare_outputs.py > week01/comparison_results.json
python3 -m json.tool week01/comparison_results.json
```

> The recommendation line prints to stderr so the JSON file stays valid when redirected.

**Optional (Week 2 eval preview):**
```bash
python week02/prompt_eval.py
cat week02/prompt_eval_results.json | python3 -m json.tool
```

**Say on camera:** *"Students compare strict vs open prompts and pick defaults for automation — low temperature, structured instructions."*

---

## Week 2 — Secure Lambda + prompt evaluation

**What students learn:** Bedrock from Lambda with least-privilege IAM; prompt versioning with a golden test set.

### Lab 2.1 — Lambda invoke (requires deploy)

```bash
source .stack.env

aws lambda invoke \
  --function-name ${PROJECT_PREFIX}-week2-invoke \
  --region $AWS_REGION \
  --payload '{"prompt":"Reply with one word: ok","correlation_id":"demo-w2-1"}' \
  --cli-binary-format raw-in-base64-out /tmp/w2.json

cat /tmp/w2.json | python3 -m json.tool
```

**Say on camera:** *"Week 2 moves Bedrock into Lambda. Notice correlation_id and latency_ms in the response — we never log full prompts."*

**Expected output (verified):**
```json
{
  "correlation_id": "demo-w2-1",
  "success": true,
  "latency_ms": 401,
  "model_id": "amazon.nova-lite-v1:0"
}
```

**Console shot (optional):** CloudWatch → Log groups → `/aws/lambda/ba-la8s-ai-demo-week2-invoke`

### Lab 2.2 — Prompt evaluation (local)

```bash
python week02/prompt_eval.py
```

**Say on camera:** *"Golden set of test cases, version A vs B, data-driven prompt selection."*

---

## Week 3 — Structured JSON + routing

**What students learn:** Force JSON output, validate schema, hybrid rules + AI routing.

**Show on screen:** `diagrams/student/png/seq-week03.png` or `cheat-week03.png`

### Lab 3.1 — Classify (structured JSON)

```bash
aws lambda invoke \
  --function-name ${PROJECT_PREFIX}-classify \
  --region $AWS_REGION \
  --payload '{"text":"Suspicious login from unknown IP address","correlation_id":"demo-w3-1"}' \
  --cli-binary-format raw-in-base64-out /tmp/w3c.json

cat /tmp/w3c.json | python3 -m json.tool
```

**Expected output (verified):**
```json
{
  "valid": true,
  "result": {
    "label": "security",
    "confidence": 0.95,
    "reason": "Mention of suspicious login from unknown IP address"
  }
}
```

### Lab 3.2 — Route (rules-first)

```bash
aws lambda invoke \
  --function-name ${PROJECT_PREFIX}-route \
  --region $AWS_REGION \
  --payload '{"text":"I was charged twice on my invoice","correlation_id":"demo-w3-2","label":"billing"}' \
  --cli-binary-format raw-in-base64-out /tmp/w3r.json

cat /tmp/w3r.json | python3 -m json.tool
```

**Expected output (verified):**
```json
{
  "route": "team_billing",
  "confidence": 0.95,
  "source": "rules",
  "reason": "rules_match"
}
```

**Say on camera:** *"Rules hit first for obvious billing keywords. AI handles ambiguity. Invalid JSON never crashes downstream — we validate everything."*

### Lab 3 — Unit tests (no AWS cost)

```bash
pytest tests/ -v
```

**Expected:** `14 passed`

---

## Week 4 — Step Functions orchestration

**What students learn:** Multi-step workflows, retries, validation branch, idempotent persist.

**Show on screen:** Step Functions console + `diagrams/student/png/seq-week04.png`

### Lab 4.1 — Happy path execution

```bash
aws stepfunctions start-execution \
  --state-machine-arn "$STATE_MACHINE_ARN" \
  --region $AWS_REGION \
  --input '{"text":"API 503 after deployment in production","correlation_id":"demo-w4-happy"}'
```

Copy the `executionArn` from output, then:

```bash
aws stepfunctions describe-execution \
  --execution-arn "<EXECUTION_ARN>" \
  --region $AWS_REGION \
  --query '{status:status,output:output}'
```

**Expected (verified):**
```json
{
  "status": "SUCCEEDED",
  "output": "{\"correlation_id\":\"demo-w4-happy\",\"status\":\"completed\",\"action\":\"ticket_stub_created\",\"stored\":true}"
}
```

**Console shot:** Step Functions → `ba-la8s-ai-demo-workflow` → Executions → Visual workflow (Classify → Validate → Persist)

### Lab 4.2 — Failure / fallback path

Demo validation failure by invoking the validate Lambda directly:

```bash
aws lambda invoke \
  --function-name ${PROJECT_PREFIX}-validate \
  --region $AWS_REGION \
  --payload '{"correlation_id":"demo-w4-fail","classification":{"result":{"label":"bad_label","confidence":2.0,"reason":"x"}},"simulate_validation_failure":true}' \
  --cli-binary-format raw-in-base64-out /tmp/w4f.json

cat /tmp/w4f.json | python3 -m json.tool
```

**Say on camera:** *"When validation fails, we take the fallback path — deterministic output, not a crash. Students document retries and catches in a reliability report."*

---

## Week 5 — AI automation APIs

**What students learn:** HTTP platform with `/classify`, `/summarize`, `/route`; cost controls.

**Show on screen:** Terminal `curl` + `diagrams/student/png/seq-week05.png`

```bash
API="$API_ENDPOINT"   # from .stack.env
```

### Lab 5.1 — Three endpoints

**Classify:**
```bash
curl -sS -X POST "$API/classify" \
  -H "Content-Type: application/json" \
  -d '{"text":"Database replication lag in production","correlation_id":"demo-w5-1"}' | python3 -m json.tool
```

**Summarize:**
```bash
curl -sS -X POST "$API/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text":"Pod crash loop after node upgrade. Errors in kubelet logs.","correlation_id":"demo-w5-2"}' | python3 -m json.tool
```

**Route:**
```bash
curl -sS -X POST "$API/route" \
  -H "Content-Type: application/json" \
  -d '{"text":"Refund for cancelled subscription","label":"billing","correlation_id":"demo-w5-3"}' | python3 -m json.tool
```

**Expected highlights (verified):**
- `/classify` → `label: technical`, `valid: true`
- `/summarize` → one-paragraph summary
- `/route` → `route: team_billing`, `source: rules`

### Lab 5.2 — Input size limit (cost control)

```bash
python3 -c 'print("{\"text\":\"" + "x"*9000 + "\",\"correlation_id\":\"demo-w5-big\"}")' > /tmp/big.json

curl -sS -w "\nHTTP: %{http_code}\n" -X POST "$API/classify" \
  -H "Content-Type: application/json" -d @/tmp/big.json
```

**Expected (verified):** HTTP `400` + `{"error":"input_too_large","max_chars":8000}`

**Say on camera:** *"Production APIs need limits — oversized input is rejected before it hits Bedrock."*

---

## Week 6 — Observability & governance

**What students learn:** Audit trail, safe logging, CloudWatch dashboard.

**Show on screen:** `diagrams/student/png/cheat-week06.png` + DynamoDB / CloudWatch console

### Lab 6.1 — Query audit by correlation ID

```bash
export AUDIT_TABLE_NAME=${PROJECT_PREFIX}-audit

python week06/query_audit.py demo-w5-1
```

**Expected (verified):** JSON array with `event_type`, `model_id`, `latency_ms`, `validation_status` — **no raw user text**.

### Lab 6.2 — Dashboard & alarm (console)

1. **CloudWatch** → **Dashboards** → `ba-la8s-ai-demo-ai-ops`
2. **CloudWatch** → **Alarms** → `ba-la8s-ai-demo-api-errors`

**Say on camera:** *"We log events, not content. Every API call is traceable by correlation_id for compliance and debugging."*

---

## Week 7 — Governed agent + memory

**What students learn:** Agent as router with tool policy, approval gates, session memory.

**Show on screen:** `diagrams/student/png/seq-week07.png` + `pattern-week07.png`

### Lab 7.1 — Safe request (allowed)

```bash
aws lambda invoke \
  --function-name ${PROJECT_PREFIX}-agent \
  --region $AWS_REGION \
  --payload '{"text":"Summarize incident: DB failover in prod","session_id":"demo-sess-1","correlation_id":"demo-w7-1"}' \
  --cli-binary-format raw-in-base64-out /tmp/w7.json

cat /tmp/w7.json | python3 -m json.tool
```

**Expected (verified):**
```json
{
  "tool": "summarize",
  "policy_decision": "allow",
  "output": { "summary": "..." }
}
```

### Lab 7.2 — Risky request (approval required)

```bash
aws lambda invoke \
  --function-name ${PROJECT_PREFIX}-agent \
  --region $AWS_REGION \
  --payload '{"text":"Delete production database root credentials","session_id":"demo-sess-1","correlation_id":"demo-w7-2"}' \
  --cli-binary-format raw-in-base64-out /tmp/w7b.json

cat /tmp/w7b.json | python3 -m json.tool
```

**Expected (verified):**
```json
{
  "tool": "action_stub",
  "policy_decision": "deny_pending_approval",
  "output": { "status": "pending_approval", "message": "Action requires human approval" }
}
```

**Say on camera:** *"Agents aren't magic — they're routers with an allowlist. Risky actions require human approval."*

### Memory check (console)

**DynamoDB** → Tables → `ba-la8s-ai-demo-memory` → Explore items → filter by `session_id`

---

## Week 8 — Capstone (student projects)

**Runnable labs:** [`labs/week08/README.md`](labs/week08/README.md)

Deploy includes all 4 capstone tracks:

| Option | Endpoint |
|--------|----------|
| A — Incident triage | `POST /capstone/incident` |
| B — Doc classification | `POST /capstone/document` |
| C — Approval workflow | `POST /capstone/approval/request` + `/decide` |
| D — Enterprise agent | `POST /capstone/agent` |

```bash
cd labs && ./scripts/start.sh && source .stack.env
./scripts/verify-capstone.sh
```

**Say on camera:** *"Week 8 ships four portfolio-ready capstone tracks — incident triage, document classification, approval workflows, and a governed enterprise agent. Students pick one to extend."*

See option READMEs under `labs/week08/option_*` for demo scripts per track.

---

## Full automated verification (all labs at once)

```bash
./scripts/verify.sh
```

**Expected (verified Aug 10, 2026):**
```
OK: Week2 Lambda invoke
OK: API /classify label=billing
OK: API /route rules path route=team_billing source=rules
OK: API /classify rejects oversized input (400)
OK: Step Functions workflow SUCCEEDED
OK: Agent Lambda tool=summarize policy=allow
OK: Audit table has 1 event(s)
=== All integration checks passed ===
```

**Or full cycle (test + deploy + verify + auto-teardown):**
```bash
./scripts/cycle.sh
```

---

## Stack outputs reference

After `./scripts/start.sh`, your `.stack.env` will contain:

| Variable | Example value |
|----------|----------------|
| `API_ENDPOINT` | `https://ao0w0h27o2.execute-api.us-east-1.amazonaws.com/prod` |
| `STATE_MACHINE_ARN` | `arn:aws:states:us-east-1:277374794397:stateMachine:ba-la8s-ai-demo-workflow` |
| `AUDIT_TABLE_NAME` | `ba-la8s-ai-demo-audit` |
| `WEEK2_FUNCTION` | `ba-la8s-ai-demo-week2-invoke` |
| `AGENT_FUNCTION` | `ba-la8s-ai-demo-agent` |

> Your URLs will differ per deploy — always `source .stack.env` before recording.

---

## LinkedIn clip ideas (one per week)

| Clip | Hook | Command to show |
|------|------|-----------------|
| Week 1 | "First Bedrock call in 30 seconds" | `invoke_bedrock.py` |
| Week 2 | "Bedrock in Lambda — production IAM" | Lambda invoke |
| Week 3 | "Never trust raw LLM output" | classify + route |
| Week 4 | "AI workflows need orchestration" | Step Functions console |
| Week 5 | "Three AI APIs in one stack" | curl /classify /summarize /route |
| Week 6 | "What to log vs never log" | `query_audit.py` |
| Week 7 | "Governed agents, not chatbots" | safe vs risky agent invoke |
| Week 8 | "Portfolio-ready capstone" | capstone diagram |

**CTA for every post:** https://baylearn.bayareala8s.com/courses/9d6c8974-eab4-45b3-aa0d-a058b9cda228/

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `AccessDeniedException` on Bedrock | Enable Nova Lite in Bedrock console → Model access |
| `sam: command not found` | `source .venv/bin/activate` (SAM is in venv) |
| Empty audit query | Run an API call first; wait 2s; use correct `correlation_id` |
| API 403/429 | Throttling — retry with backoff |
| Stack already exists | `./scripts/status.sh` or use different `PROJECT_PREFIX` |

---

## Cost reminder

- **While stack is up:** small DynamoDB + API Gateway charges; Bedrock charges per invoke
- **After `./scripts/stop.sh`:** stack deleted — no ongoing resource cost
- **Free:** `pytest`, Week 1 local scripts (Bedrock invoke only)

---

*BayAreaLa8s — AI Automation & Agents with AWS Bedrock*
