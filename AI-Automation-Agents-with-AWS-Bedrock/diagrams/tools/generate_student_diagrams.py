#!/usr/bin/env python3
"""Generate student-focused diagrams: sequences, cheat sheets, lab guides, patterns."""

from __future__ import annotations

from pathlib import Path

from drawio_builder import Box, Diagram, DrawioBuilder, Edge, Node, StepBadge, Zone

OUT = Path(__file__).resolve().parents[1] / "student" / "drawio"


def _focus(text: str, x: int = 40, y: int = 78, w: int = 1520) -> Box:
    return Box("focus", f"YOUR GOAL\n{text}", x, y, w, 60, "objective")


def _do(text: str, x: int, y: int, w: int = 280) -> Box:
    return Box(f"do_{x}_{y}", f"DO THIS\n{text}", x, y, w, 72, "success")


def _remember(text: str, x: int, y: int, w: int = 300) -> Box:
    return Box(f"rem_{x}_{y}", f"REMEMBER\n{text}", x, y, w, 72, "student")


def seq_week03() -> Diagram:
    d = Diagram(
        "seq-week03",
        "Week 3 — Request Sequence (Classify → Validate → Route)",
        subtitle="Follow one request through the decision engine — time flows left to right",
        width=1700, height=900,
    )
    d.boxes.append(_focus(
        "Trace a single ticket through classify, JSON validation, confidence gate, and routing — "
        "including what happens when validation fails.", 40, 78))
    d.zones = [Zone("z_time", "TIME →", 40, 160, 1620, 420, "#F7F8F8")]
    d.nodes = [
        Node("n1", "Request", "client", 80, 260, sublabel='{"text":"..."}'),
        Node("n2", "Classify", "lambda", 320, 260, sublabel="Bedrock invoke"),
        Node("n3", "Bedrock", "bedrock", 520, 260, fill="dark", sublabel="JSON output"),
        Node("n4", "Validator", "lambda", 720, 260, sublabel="schema check"),
        Node("n5", "Gate", "lambda", 920, 260, sublabel="confidence ≥ 0.7?"),
        Node("n6", "Route", "lambda", 1120, 260, sublabel="team assignment"),
        Node("n7", "Fallback", "user", 1120, 420, fill="gray", sublabel="human review"),
    ]
    d.edges = [
        Edge("e1", "n1", "n2", "①", bold=True),
        Edge("e2", "n2", "n3", "② invoke"),
        Edge("e3", "n3", "n4", "③ raw JSON"),
        Edge("e4", "n4", "n5", "④ if valid"),
        Edge("e5", "n5", "n6", "⑤ high conf."),
        Edge("e6", "n4", "n7", "invalid JSON", dashed=True, color="#DD3522"),
        Edge("e7", "n5", "n7", "low conf.", dashed=True, color="#DD3522"),
    ]
    d.steps = [StepBadge(i, 60 + i * 200, 200, "") for i in range(1, 6)]
    d.boxes.extend([
        Box("code", 'Expected output:\n{\n  "label": "billing",\n  "confidence": 0.91,\n  "route": "team_billing",\n  "reason": "invoice keyword"\n}', 80, 520, 340, 110, "code"),
        _do("Run: pytest tests/test_validation.py\nbefore deploying.", 460, 520, 320),
        _remember("Non-JSON or invalid schema → deterministic fallback, never crash.", 820, 520, 360),
        Box("fail", "6 FAILURE MODES TO TEST\n① Non-JSON text  ② Missing keys  ③ Wrong enum\n④ confidence out of range  ⑤ reason too long  ⑥ Low confidence", 80, 660, 720, 90, "danger"),
    ])
    return d


def seq_week04() -> Diagram:
    d = Diagram(
        "seq-week04",
        "Week 4 — Step Functions Execution Timeline",
        subtitle="One workflow run: retries, catches, and idempotent persist",
        width=1700, height=950,
    )
    d.boxes.append(_focus(
        "Understand when Step Functions retries vs catches, and why persist must be idempotent.", 40, 78))
    d.zones = [
        Zone("z_happy", "HAPPY PATH", 40, 160, 780, 380, "#E9F7EF"),
        Zone("z_fail", "FAILURE PATHS", 860, 160, 800, 380, "#FADBD8"),
    ]
    d.nodes = [
        Node("start", "Start", "step_functions", 80, 240, fill="green"),
        Node("cls", "Classify", "lambda", 240, 240),
        Node("val", "Validate", "lambda", 400, 240),
        Node("per", "Persist", "lambda", 560, 240),
        Node("done", "Success", "document", 720, 240, fill="green"),
        Node("retry", "Retry", "step_functions", 900, 240, fill="green", sublabel="backoff"),
        Node("catch", "Catch", "step_functions", 900, 360, fill="green", sublabel="fallback"),
        Node("fb", "Fallback", "lambda", 1100, 360),
        Node("rev", "Needs Review", "user", 1300, 360, fill="gray"),
    ]
    d.edges = [
        Edge("e1", "start", "cls", "①"),
        Edge("e2", "cls", "val", "②"),
        Edge("e3", "val", "per", "③ valid"),
        Edge("e4", "per", "done", "④"),
        Edge("e5", "cls", "retry", "throttle/timeout", dashed=True, color="#DD3522"),
        Edge("e6", "retry", "cls", "retry", dashed=True),
        Edge("e7", "val", "catch", "schema fail", dashed=True, color="#DD3522"),
        Edge("e8", "catch", "fb", "⑤"),
        Edge("e9", "fb", "rev"),
    ]
    d.boxes.extend([
        Box("retry_rule", "RETRY when:\n• Bedrock throttling\n• Lambda timeout\n• Transient network error\n\nUse exponential backoff, max 3 attempts", 80, 580, 360, 110, "neutral"),
        Box("catch_rule", "CATCH when:\n• Validation permanent fail\n• Invalid enum / schema\n• Business rule violation\n\n→ deterministic fallback state", 480, 580, 360, 110, "neutral"),
        Box("idempotent", "IDEMPOTENCY KEY\nUse correlation_id as DynamoDB key.\nReplay safe — same input → same row, no duplicates.", 880, 580, 400, 90, "code"),
        _do("Open Step Functions console → Executions.\nInject failure in lab, screenshot run graph.", 80, 720, 400),
        _remember("Retries ≠ catches. Retries fix transient; catches handle permanent failures.", 520, 720, 420),
    ])
    return d


def seq_week05() -> Diagram:
    d = Diagram(
        "seq-week05",
        "Week 5 — API Request Flow",
        subtitle="What happens when a client calls POST /classify",
        width=1700, height=900,
    )
    d.boxes.append(_focus(
        "Follow an HTTP request from client to response — including throttling and error codes.", 40, 78))
    d.nodes = [
        Node("client", "Client", "client", 80, 280),
        Node("api", "API Gateway", "api_gateway", 280, 280, fill="purple"),
        Node("lam", "Lambda", "lambda", 480, 280, sublabel="handler"),
        Node("br", "Bedrock", "bedrock", 680, 280, fill="dark"),
        Node("aud", "Audit", "dynamodb", 880, 280, fill="blue", sublabel="async log"),
        Node("resp", "Response", "document", 1080, 280, fill="green"),
    ]
    d.edges = [
        Edge("e1", "client", "api", "POST /classify", bold=True),
        Edge("e2", "api", "lam", "② invoke"),
        Edge("e3", "lam", "br", "③ model call"),
        Edge("e4", "br", "lam", "④ JSON"),
        Edge("e5", "lam", "aud", "⑤ audit", dashed=True),
        Edge("e6", "lam", "resp", "⑥ return"),
        Edge("e7", "resp", "client", "200 / 400 / 429 / 500"),
    ]
    d.boxes.extend([
        Box("codes", "HTTP STATUS CODES\n200 — valid classified result\n400 — bad input / validation fail\n429 — throttled (retry with backoff)\n500 — unexpected server error", 80, 480, 380, 120, "code"),
        Box("req", 'Request body:\n{\n  "text": "server down in prod",\n  "correlation_id": "req-001"\n}', 500, 480, 300, 90, "code"),
        Box("resp_ex", 'Success response:\n{\n  "label": "incident",\n  "confidence": 0.88,\n  "route": "team_ops"\n}', 840, 480, 300, 90, "code"),
        _do("Test with curl against ApiEndpoint output.\nTry missing correlation_id → expect 400.", 80, 660, 400),
        _remember("Every request needs correlation_id for tracing in CloudWatch + audit.", 520, 660, 420),
    ])
    return d


def seq_week07() -> Diagram:
    d = Diagram(
        "seq-week07",
        "Week 7 — Agent Turn Sequence",
        subtitle="One agent turn: router → tool policy → memory → response",
        width=1700, height=950,
    )
    d.boxes.append(_focus(
        "See how the agent decides which tool to call, checks policy, and updates memory.", 40, 78))
    d.nodes = [
        Node("user", "User", "user", 80, 280),
        Node("agent", "Agent", "lambda", 260, 280, sublabel="router"),
        Node("mem_r", "Memory", "dynamodb", 440, 200, fill="blue", sublabel="read TTL"),
        Node("policy", "Tool Policy", "iam", 440, 360, fill="red", sublabel="allowlist"),
        Node("tool", "Tool Lambda", "lambda", 640, 280, sublabel="classify/route"),
        Node("br", "Bedrock", "bedrock", 820, 280, fill="dark"),
        Node("mem_w", "Memory", "dynamodb", 1000, 200, fill="blue", sublabel="write"),
        Node("out", "Reply", "document", 1180, 280, fill="green"),
    ]
    d.edges = [
        Edge("e1", "user", "agent", "① message", bold=True),
        Edge("e2", "agent", "mem_r", "② context", dashed=True),
        Edge("e3", "agent", "policy", "③ check tool"),
        Edge("e4", "policy", "tool", "④ allowed"),
        Edge("e5", "tool", "br", "⑤ invoke"),
        Edge("e6", "br", "tool", "result"),
        Edge("e7", "tool", "mem_w", "⑥ store turn", dashed=True),
        Edge("e8", "agent", "out", "⑦ response"),
        Edge("e9", "out", "user"),
        Edge("e10", "policy", "agent", "denied", dashed=True, color="#DD3522"),
    ]
    d.boxes.extend([
        Box("policy_ex", "TOOL ALLOWLIST\n✓ classify  ✓ route  ✓ summarize\n✗ arbitrary HTTP  ✗ shell  ✗ delete", 80, 520, 340, 90, "success"),
        _do("POST to agent endpoint with 3-turn conversation.\nVerify memory TTL in DynamoDB.", 460, 520, 380),
        _remember("Agents are routers + policy — not unconstrained autonomy.", 880, 520, 380),
    ])
    return d


def cheat_week03() -> Diagram:
    d = Diagram(
        "cheat-week03",
        "Week 3 — Student Cheat Sheet",
        subtitle="Schema, validation rules, and confidence gate decision tree",
        width=1500, height=900,
    )
    d.boxes.append(_focus("Quick reference while building Lab 3.1 and 3.2.", 40, 78, 1420))
    d.boxes.extend([
        Box("schema", "REQUIRED SCHEMA\nlabel     → enum (billing|incident|general)\nconfidence → float 0.0–1.0\nroute     → enum (team_billing|team_ops|team_general)\nreason    → string, max 120 chars", 40, 160, 420, 130, "code"),
        Box("validate", "VALIDATOR CHECKS\n☐ Valid JSON (strict parse)\n☐ All required keys present\n☐ Types match (str, float)\n☐ Enums in allowed set\n☐ confidence in [0, 1]\n☐ reason length ≤ max", 500, 160, 400, 150, "neutral"),
        Box("tree", "CONFIDENCE GATE\n\n        ┌─ confidence ≥ 0.7 ─→ auto-route\noutput ─┤\n        ├─ 0.4 ≤ conf < 0.7 ─→ route + flag review\n        └─ confidence < 0.4 ─→ deterministic fallback", 940, 160, 520, 150, "success"),
        Box("fallback", "DETERMINISTIC FALLBACK\nlabel=general, route=team_general,\nconfidence=0.0, reason=validation_failed", 40, 340, 420, 80, "danger"),
        _do("Copy schema into your prompt.\nWrite tests for all 6 failure modes first.", 500, 340, 400),
        _remember("Validate AFTER Bedrock — never trust raw model output.", 940, 340, 520),
    ])
    return d


def cheat_week04() -> Diagram:
    d = Diagram(
        "cheat-week04",
        "Week 4 — Step Functions Cheat Sheet",
        subtitle="States, retry config, and catch patterns for your state machine",
        width=1500, height=900,
    )
    d.boxes.append(_focus("Use while editing workflow.asl.json and running failure injection.", 40, 78, 1420))
    d.boxes.extend([
        Box("states", "STATE ORDER\n1. ClassifyTask     (Lambda invoke)\n2. ValidateTask     (Lambda invoke)\n3. PersistTask       (Lambda invoke)\n4. Success           (Succeed)\n\nCatch branches → FallbackTask → NeedsReview", 40, 160, 440, 160, "neutral"),
        Box("retry", 'RETRY BLOCK (transient)\n"ErrorEquals": ["Lambda.TooManyRequestsException",\n                 "States.Timeout", "Sandbox.Timedout"],\n"IntervalSeconds": 2,\n"MaxAttempts": 3,\n"BackoffRate": 2.0', 520, 160, 460, 150, "code"),
        Box("catch", 'CATCH BLOCK (permanent)\n"ErrorEquals": ["ValidationError"],\n"Next": "FallbackTask"\n\nResultPath: $.error — preserve context', 1020, 160, 440, 120, "code"),
        Box("idemp", "IDEMPOTENCY\n• Key = correlation_id from input\n• PutItem with condition OR overwrite same key\n• Safe to replay failed executions", 40, 360, 440, 100, "success"),
        _do("Run execution → copy ARN → share in assignment.\nScreenshot failure injection run.", 520, 360, 460),
        _remember("Test unhappy paths — graders want failure evidence.", 1020, 360, 440),
    ])
    return d


def cheat_week06() -> Diagram:
    d = Diagram(
        "cheat-week06",
        "Week 6 — Logging & Audit Cheat Sheet",
        subtitle="What to log, what to redact, and how to query audit records",
        width=1500, height=900,
    )
    d.boxes.append(_focus("Governance reference for audit pipeline and CloudWatch queries.", 40, 78, 1420))
    d.boxes.extend([
        Box("log_yes", "ALWAYS LOG\n• correlation_id\n• timestamp (ISO 8601)\n• action / endpoint name\n• model_id\n• latency_ms\n• outcome (success|validation_fail|error)\n• route / label (non-PII)", 40, 160, 440, 150, "success"),
        Box("log_no", "NEVER LOG\n• Full prompt with PII\n• API keys / tokens\n• Passwords / SSN / account numbers\n• Raw user text (use hash or truncate)\n• Bedrock credentials", 520, 160, 440, 150, "danger"),
        Box("query", "QUERY AUDIT\npython week06/query_audit.py <correlation_id>\n\nCloudWatch Logs Insights:\nfields @timestamp, correlation_id, outcome\n| filter correlation_id = 'req-001'", 1000, 160, 460, 130, "code"),
        Box("alarm", "ALARMS TO WATCH\n• Error rate > threshold\n• Validation failure spike\n• Bedrock throttling events", 40, 360, 440, 90, "neutral"),
        _do("Find your correlation_id in verify.sh output.\nRun query_audit.py before Week 6 assignment.", 520, 360, 440),
        _remember("Audit rows enable compliance — design them like a database schema.", 1000, 360, 460),
    ])
    return d


def cheat_week08() -> Diagram:
    d = Diagram(
        "cheat-week08",
        "Week 8 — Capstone Checklist & Demo Script",
        subtitle="Minimum bar, deliverables, and 5-minute demo flow",
        width=1500, height=950,
    )
    d.boxes.append(_focus("Use during capstone build and final presentation prep.", 40, 78, 1420))
    d.boxes.extend([
        Box("minbar", "MINIMUM BAR\n☐ Working deploy (start.sh or SAM deploy)\n☐ At least 1 API endpoint live\n☐ Structured output + validation\n☐ Step Functions OR agent routing\n☐ Audit log with correlation_id\n☐ README with architecture + run steps", 40, 160, 460, 160, "success"),
        Box("deliver", "SUBMIT\n• Git repo link\n• Architecture diagram (yours or course template)\n• 5-min demo video OR live demo\n• Reliability evidence (1 failure test)\n• Cost note (teardown confirmed)", 540, 160, 440, 140, "neutral"),
        Box("demo", "5-MIN DEMO SCRIPT\n0:00 — Problem statement (30s)\n0:30 — Architecture walkthrough (1m)\n1:30 — Happy path live call (1.5m)\n3:00 — Show validation failure + recovery (1m)\n4:00 — Audit trail + governance (1m)", 1020, 160, 440, 150, "code"),
        Box("options", "CAPSTONE OPTIONS\nA — Incident triage platform\nB — Document classification API\nC — Multi-step approval workflow\nD — Enterprise agent with tool policy", 40, 360, 460, 110, "neutral"),
        _do("Run ./scripts/cycle.sh before recording demo.\nConfirm stop.sh ran (no surprise bills).", 540, 360, 440),
        _remember("Graders score production thinking — not prompt cleverness.", 1020, 360, 440),
    ])
    return d


def lab_deploy_cycle() -> Diagram:
    d = Diagram(
        "lab-deploy-cycle",
        "Labs — Deploy Cycle (cycle.sh)",
        subtitle="One command: test → deploy → verify → teardown",
        width=1500, height=850,
    )
    d.boxes.append(_focus("Understand the full lab lifecycle before your first AWS deploy.", 40, 78, 1420))
    d.nodes = [
        Node("n1", "run-tests.sh", "document", 80, 260, fill="green", sublabel="pytest (free)"),
        Node("n2", "start.sh", "lambda", 320, 260, sublabel="sam deploy"),
        Node("n3", "verify.sh", "cloudwatch", 560, 260, fill="red", sublabel="integration"),
        Node("n4", "teardown.sh", "step_functions", 800, 260, fill="green", sublabel="delete stack"),
        Node("n5", "Done", "document", 1040, 260, fill="green", sublabel="no ongoing cost"),
    ]
    d.edges = [
        Edge("e1", "n1", "n2", "pass", bold=True),
        Edge("e2", "n2", "n3", "stack ready"),
        Edge("e3", "n3", "n4", "pass"),
        Edge("e4", "n4", "n5"),
        Edge("e5", "n1", "n5", "fail fast", dashed=True, color="#DD3522"),
        Edge("e6", "n3", "n5", "fail", dashed=True, color="#DD3522"),
    ]
    d.boxes.extend([
        Box("cmd", "ONE COMMAND\ncd labs\nPROJECT_PREFIX=ba-la8s-ai-yourname ./scripts/cycle.sh\n\nKeep stack: ./scripts/cycle.sh --keep-stack", 80, 460, 440, 100, "code"),
        Box("env", "SET BEFORE DEPLOY\nexport AWS_REGION=us-east-1\nexport PROJECT_PREFIX=ba-la8s-ai-yourname\nexport BEDROCK_MODEL_ID=amazon.nova-lite-v1:0", 560, 460, 440, 100, "code"),
        _do("Always run cycle.sh first — catches errors before you debug in console.", 80, 620, 440),
        _remember("stop.sh / teardown.sh = delete stack = stop most charges.", 560, 620, 440),
    ])
    return d


def lab_console_checkpoints() -> Diagram:
    d = Diagram(
        "lab-console-checkpoints",
        "Labs — After Deploy: 3 Console Checkpoints",
        subtitle="Where to look when verify.sh passes but you want to explore",
        width=1500, height=850,
    )
    d.boxes.append(_focus("Navigate AWS console confidently after start.sh deploys your stack.", 40, 78, 1420))
    d.nodes = [
        Node("cf", "CloudFormation", "generic", 80, 280, fill="gray", sublabel="stack status"),
        Node("lam", "Lambda", "lambda", 380, 280, sublabel="functions"),
        Node("sfn", "Step Functions", "step_functions", 680, 280, fill="green", sublabel="executions"),
        Node("api", "API Gateway", "api_gateway", 980, 280, fill="purple", sublabel="invoke URL"),
    ]
    d.edges = [
        Edge("e1", "cf", "lam", "① outputs"),
        Edge("e2", "lam", "sfn", "② test invoke"),
        Edge("e3", "sfn", "api", "③ live HTTP"),
    ]
    d.boxes.extend([
        Box("c1", "CHECKPOINT 1 — CloudFormation\nStack: {PROJECT_PREFIX}-labs\nStatus: CREATE_COMPLETE\nCopy outputs: ApiEndpoint, StateMachineArn", 40, 460, 440, 110, "neutral"),
        Box("c2", "CHECKPOINT 2 — Step Functions\nStart execution with sample input\nView graph: classify → validate → persist\nFind correlation_id in execution input", 520, 460, 440, 110, "neutral"),
        Box("c3", "CHECKPOINT 3 — API Gateway\ncurl -X POST $ApiEndpoint/classify \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"text\":\"...\",\"correlation_id\":\"demo-1\"}'", 1000, 460, 460, 110, "code"),
        _do("Use status.sh to see if stack is up before opening console.", 40, 620, 440),
        _remember("Console exploration is optional — verify.sh is your source of truth.", 520, 620, 440),
    ])
    return d


def pattern_week03() -> Diagram:
    d = Diagram(
        "pattern-week03",
        "Week 3 — Anti-Pattern vs Production Pattern",
        subtitle="Raw LLM output vs validated structured automation",
        width=1500, height=800,
    )
    d.boxes.append(_focus("See why validation is non-optional in enterprise automation.", 40, 78, 1420))
    d.zones = [
        Zone("z_bad", "ANTI-PATTERN", 40, 160, 680, 420, "#FADBD8"),
        Zone("z_good", "PRODUCTION PATTERN", 780, 160, 680, 420, "#E9F7EF"),
    ]
    d.boxes.extend([
        Box("bad1", "User text → Bedrock → parse with regex → hope it works\n\nRisks:\n• Model returns prose, not JSON\n• Hallucinated enum values\n• No confidence gate\n• Downstream crashes", 60, 220, 640, 130, "danger"),
        Box("bad2", 'Example bad output:\n"I think this is probably billing related..."', 60, 380, 640, 70, "code"),
        Box("good1", "User text → Bedrock → strict JSON → validator → confidence gate → route\n\nControls:\n• Schema enforced\n• Fallback on failure\n• correlation_id traced\n• Tests cover 6 failure modes", 800, 220, 640, 130, "success"),
        Box("good2", 'Example good output:\n{"label":"billing","confidence":0.91,\n "route":"team_billing","reason":"invoice keyword"}', 800, 380, 640, 80, "code"),
        _remember("If you cannot validate it, you cannot automate it.", 60, 620, 640),
        _do("Implement validator before tuning prompts.", 800, 620, 640),
    ])
    return d


def pattern_week06() -> Diagram:
    d = Diagram(
        "pattern-week06",
        "Week 6 — Anti-Pattern vs Production Pattern",
        subtitle="Log everything vs redacted audit trail",
        width=1500, height=800,
    )
    d.boxes.append(_focus("Logging choices affect compliance, cost, and incident response.", 40, 78, 1420))
    d.zones = [
        Zone("z_bad", "ANTI-PATTERN — Log Everything", 40, 160, 680, 420, "#FADBD8"),
        Zone("z_good", "PRODUCTION — Structured Audit", 780, 160, 680, 420, "#E9F7EF"),
    ]
    d.boxes.extend([
        Box("bad1", "print(full_prompt)\nprint(user_message)\nprint(api_key)\n\nProblems:\n• PII in CloudWatch\n• Credential leakage risk\n• Unqueryable blob logs\n• Compliance violation", 60, 220, 640, 130, "danger"),
        Box("good1", "log structured audit row:\n{correlation_id, action, model_id,\n latency_ms, outcome, label, route}\n\nBenefits:\n• Searchable\n• Redaction-safe\n• Retention policies\n• Dashboard-ready", 800, 220, 640, 130, "success"),
        Box("good2", "Use week06/query_audit.py — not raw log grep", 800, 380, 640, 50, "code"),
        _remember("Log events, not content. Hash or truncate user text.", 60, 620, 640),
        _do("Review audit.py — mirror its fields in your capstone.", 800, 620, 640),
    ])
    return d


def pattern_week07() -> Diagram:
    d = Diagram(
        "pattern-week07",
        "Week 7 — Anti-Pattern vs Production Pattern",
        subtitle="Unlimited agent vs tool policy + memory bounds",
        width=1500, height=800,
    )
    d.boxes.append(_focus("Agents need boundaries — same as any production API.", 40, 78, 1420))
    d.zones = [
        Zone("z_bad", "ANTI-PATTERN — Autonomous Agent", 40, 160, 680, 420, "#FADBD8"),
        Zone("z_good", "PRODUCTION — Governed Agent", 780, 160, 680, 420, "#E9F7EF"),
    ]
    d.boxes.extend([
        Box("bad1", "Agent can call any URL, run any code, no memory limit\n\nRisks:\n• Prompt injection → data exfil\n• Runaway tool loops\n• Unbounded DynamoDB growth\n• No audit of tool calls", 60, 220, 640, 130, "danger"),
        Box("good1", "Router + allowlisted tools + TTL memory + audit per turn\n\nControls:\n• classify / route / summarize only\n• Deny unknown tools\n• Memory expires (TTL)\n• correlation_id per turn", 800, 220, 640, 130, "success"),
        Box("good2", "Tool policy = IAM mindset for agents", 800, 380, 640, 50, "code"),
        _remember("An agent is a router, not magic. Policy first.", 60, 620, 640),
        _do("List allowed tools in README. Test denied tool request.", 800, 620, 640),
    ])
    return d


STUDENT_DIAGRAMS = [
    seq_week03, seq_week04, seq_week05, seq_week07,
    cheat_week03, cheat_week04, cheat_week06, cheat_week08,
    lab_deploy_cycle, lab_console_checkpoints,
    pattern_week03, pattern_week06, pattern_week07,
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for factory in STUDENT_DIAGRAMS:
        diagram = factory()
        xml = DrawioBuilder(diagram).build()
        path = OUT / f"{diagram.name}.drawio"
        path.write_text(xml, encoding="utf-8")
        print(f"Wrote {path.name} ({diagram.width}x{diagram.height})")
    print(f"\nGenerated {len(STUDENT_DIAGRAMS)} student diagrams.")


if __name__ == "__main__":
    main()
