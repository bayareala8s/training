#!/usr/bin/env python3
"""Generate detailed, instructor-ready AWS architecture diagrams."""

from __future__ import annotations

from pathlib import Path

from drawio_builder import Box, Diagram, DrawioBuilder, Edge, Node, StepBadge, Zone

OUT = Path(__file__).resolve().parents[1] / "drawio"


def _legend(x: int, y: int, lines: list[str]) -> Box:
    return Box("legend", "LEGEND\n" + "\n".join(f"• {ln}" for ln in lines), x, y, 280, 40 + 18 * len(lines), "legend")


def _objective(text: str, x: int, y: int, w: int = 1520) -> Box:
    return Box("obj", f"LEARNING FOCUS\n{text}", x, y, w, 70, "objective")


def _instructor(text: str, x: int, y: int, w: int = 340, h: int = 90) -> Box:
    return Box(f"inst_{x}_{y}", f"INSTRUCTOR TALKING POINT\n{text}", x, y, w, h, "instructor")


def _student(text: str, x: int, y: int, w: int = 300) -> Box:
    return Box(f"stu_{x}_{y}", f"STUDENT TAKEAWAY\n{text}", x, y, w, 80, "student")


def ref_architecture() -> Diagram:
    d = Diagram(
        "01-reference",
        "Course Reference Architecture",
        subtitle="End-to-end production AI automation on AWS — every week builds toward this pattern",
        width=1700, height=1200,
    )
    d.boxes.append(_objective(
        "Understand how events and APIs enter the system, how Bedrock is invoked inside orchestrated workflows, "
        "and where validation, persistence, audit, and human oversight fit.", 40, 78))
    d.zones = [
        Zone("z_ingress", "① INGRESS — How work enters the platform", 40, 170, 380, 520, "#EEF5FC"),
        Zone("z_orch", "② ORCHESTRATION — Reliable multi-step AI workflows", 440, 170, 420, 520, "#E9F7EF"),
        Zone("z_ai", "③ AI + GUARDRAILS — Model + deterministic validation", 880, 170, 380, 520, "#F5F0FF"),
        Zone("z_data", "④ DATA + OPS — Persist, audit, alert, govern", 1280, 170, 380, 520, "#FFF8E6"),
    ]
    d.nodes = [
        Node("user", "Users", "user", 80, 280, sublabel="Operators / apps"),
        Node("api", "API Gateway", "api_gateway", 220, 240, fill="purple", sublabel="REST / HTTP"),
        Node("eb", "EventBridge", "eventbridge", 220, 400, fill="red", sublabel="async events"),
        Node("sfn", "Step Functions", "step_functions", 500, 320, fill="green", sublabel="state machine"),
        Node("lam_val", "Lambda", "lambda", 700, 240, sublabel="validate JSON"),
        Node("bedrock", "Amazon Bedrock", "bedrock", 960, 280, fill="dark", sublabel="Nova / Claude"),
        Node("lam_act", "Lambda", "lambda", 700, 420, sublabel="actions"),
        Node("ddb", "DynamoDB", "dynamodb", 1340, 280, fill="blue", sublabel="audit + results"),
        Node("s3", "S3", "s3", 1340, 420, fill="green", sublabel="documents"),
        Node("cw", "CloudWatch", "cloudwatch", 1100, 520, fill="red", sublabel="metrics + alarms"),
        Node("hitl", "Human Review", "user", 960, 480, fill="gray", sublabel="low confidence"),
    ]
    d.edges = [
        Edge("e1", "user", "api", "① sync request", bold=True),
        Edge("e2", "user", "eb", "② async event"),
        Edge("e3", "api", "sfn", "③ start workflow"),
        Edge("e4", "eb", "sfn"),
        Edge("e5", "sfn", "bedrock", "④ invoke model"),
        Edge("e6", "sfn", "lam_val", "⑤ validate output"),
        Edge("e7", "lam_val", "lam_act", "⑥ if valid"),
        Edge("e8", "lam_val", "hitl", "invalid / low conf.", dashed=True, color="#DD3522"),
        Edge("e9", "lam_act", "ddb", "⑦ persist"),
        Edge("e10", "lam_act", "s3"),
        Edge("e11", "sfn", "cw", "logs", dashed=True),
        Edge("e12", "lam_act", "cw", dashed=True),
    ]
    d.steps = [
        StepBadge(1, 60, 200, "Ingress"),
        StepBadge(2, 460, 200, "Orchestrate"),
        StepBadge(3, 900, 200, "AI + validate"),
        StepBadge(4, 1300, 200, "Store + observe"),
    ]
    d.boxes.extend([
        Box("code_in", 'Example input:\n{ "text": "invoice charged twice",\n  "correlation_id": "abc-123" }', 60, 620, 300, 90, "code"),
        Box("code_out", 'Validated output:\n{ "label": "billing", "confidence": 0.91,\n  "route": "team_billing" }', 900, 620, 320, 90, "code"),
        _legend(40, 720, [
            "Solid arrow = happy path",
            "Dashed red = fallback / human",
            "correlation_id in every log + audit row",
        ]),
        _instructor(
            "Stress: Bedrock is probabilistic — orchestration + validation make automation safe. "
            "Never let the model call external systems without policy checks.", 1280, 720, 380, 100),
        _student("Every production path needs: structured output, validator, fallback, audit trail.", 1280, 840, 380),
    ])
    return d


def week01_landscape() -> Diagram:
    d = Diagram(
        "02-week01",
        "Week 1 — Enterprise AI Landscape",
        subtitle="When to use rules, ML, or LLMs — and what this course builds",
        width=1700, height=1150,
    )
    d.boxes.append(_objective(
        "Compare rules engines, traditional ML, and LLMs. Identify risks (hallucination, cost, data leakage) "
        "and map them to architectural controls.", 40, 78))
    d.zones = [
        Zone("zr", "RULES ENGINE", 40, 170, 500, 340, "#E9F7EF"),
        Zone("zm", "TRADITIONAL ML", 580, 170, 500, 340, "#EEF5FC"),
        Zone("zl", "LARGE LANGUAGE MODELS", 1120, 170, 540, 340, "#F5F0FF"),
        Zone("zc", "THIS COURSE — Production AI Automation Platform", 40, 540, 1620, 280, "#FFF8E6"),
    ]
    d.boxes.extend([
        Box("r1", "Best for:\n• Fixed policy logic\n• Compliance checks\n• Known patterns\n\nLimitations:\n• Breaks on free text\n• Hard to maintain huge rule sets", 60, 220, 220, 160, "neutral"),
        Box("r2", "Example:\nIF keyword IN ('invoice','billing')\n  THEN route = 'billing'", 300, 220, 220, 100, "code"),
        Box("m1", "Best for:\n• Classification with labels\n• Forecasting\n• Vision / tabular data\n\nLimitations:\n• Needs training data\n• Drift when data changes", 600, 220, 220, 160, "neutral"),
        Box("l1", "Best for:\n• Language understanding\n• Summarization\n• Flexible reasoning\n\nLimitations:\n• Non-deterministic\n• Can hallucinate\n• Token cost", 1140, 220, 240, 160, "neutral"),
        Box("risk", "ENTERPRISE RISKS\n① Hallucination → validation + human review\n② Cost spikes → throttling + limits\n③ Data leakage → redaction + IAM\n④ No audit trail → correlation ID + logging", 40, 860, 500, 120, "danger"),
    ])
    d.nodes = [
        Node("n1", "Step Functions", "step_functions", 120, 600, fill="green", sublabel="orchestration"),
        Node("n2", "Bedrock", "bedrock", 360, 600, fill="dark", sublabel="foundation model"),
        Node("n3", "Lambda Validator", "lambda", 600, 600, sublabel="JSON schema"),
        Node("n4", "API Gateway", "api_gateway", 840, 600, fill="purple", sublabel="platform APIs"),
        Node("n5", "CloudWatch", "cloudwatch", 1080, 600, fill="red", sublabel="ops"),
        Node("n6", "DynamoDB Audit", "dynamodb", 1320, 600, fill="blue", sublabel="governance"),
    ]
    d.edges = [
        Edge("w1", "n1", "n2", "invoke"),
        Edge("w2", "n2", "n3", "validate"),
        Edge("w3", "n3", "n4", "expose"),
        Edge("w4", "n3", "n5", "observe", dashed=True),
        Edge("w5", "n3", "n6", "audit", dashed=True),
    ]
    d.notes = [
        _instructor("Use the decision matrix in class: deterministic? → rules. Labeled data + stability? → ML. Language + flexibility? → LLM + guardrails.", 580, 860, 480, 90),
        _student("AI in production = workflow + model + validation + ops — not chatbot-only prompt engineering.", 1100, 860, 400),
    ]
    return d


def week02_secure() -> Diagram:
    d = Diagram(
        "03-week02",
        "Week 2 — Secure Bedrock Integration",
        subtitle="IAM least privilege, model access, prompt versioning, and safe logging",
        width=1700, height=1150,
    )
    d.boxes.append(_objective(
        "Design IAM so only the runtime role can invoke specific foundation models. "
        "Enable model access, version prompts, and log metadata — not secrets.", 40, 78))
    d.zones = [
        Zone("z_id", "IDENTITY & ACCESS", 40, 170, 520, 400, "#FADBD8"),
        Zone("z_run", "RUNTIME (Lambda)", 580, 170, 520, 400, "#E9F7EF"),
        Zone("z_br", "BEDROCK", 1120, 170, 540, 400, "#F5F0FF"),
        Zone("z_log", "OBSERVABILITY (safe)", 580, 600, 1080, 200, "#FFF8E6"),
    ]
    d.nodes = [
        Node("dev", "Developer", "user", 80, 260),
        Node("ci", "CI/CD Pipeline", "client", 80, 380),
        Node("iam_deploy", "Deploy Role", "iam", 300, 260, fill="red", sublabel="CloudFormation"),
        Node("iam_run", "Lambda Role", "iam", 700, 260, fill="red", sublabel="execution only"),
        Node("lam", "Lambda", "lambda", 700, 380),
        Node("br", "Bedrock", "bedrock", 1280, 300, fill="dark"),
        Node("cw", "CloudWatch", "cloudwatch", 640, 660, fill="red"),
        Node("ddb", "Audit Table", "dynamodb", 960, 660, fill="blue"),
        Node("sm", "Secrets Mgr", "secrets", 300, 480, fill="red", sublabel="optional"),
    ]
    d.edges = [
        Edge("s1", "dev", "iam_deploy", "deploy stack"),
        Edge("s2", "ci", "iam_deploy"),
        Edge("s3", "iam_run", "lam", "attached"),
        Edge("s4", "lam", "br", "bedrock:Converse\non specific model ARN", bold=True),
        Edge("s5", "lam", "cw", "latency, status", dashed=True),
        Edge("s6", "lam", "ddb", "audit event", dashed=True),
        Edge("s7", "sm", "lam", "API keys only\nif needed", dashed=True, color="#879196"),
    ]
    d.steps = [
        StepBadge(1, 60, 180, "Who deploys?"),
        StepBadge(2, 600, 180, "Who invokes AI?"),
        StepBadge(3, 1120, 180, "Model gate"),
        StepBadge(4, 600, 580, "What we log"),
    ]
    d.boxes.extend([
        Box("pol", "IAM POLICY (example)\nAllow: bedrock:Converse\nResource: arn:aws:bedrock:*::foundation-model/amazon.nova-lite-v1:0\nDeny: * on all other models", 1120, 480, 500, 100, "code"),
        Box("nog", "NEVER LOG\n• Full prompts with PII\n• API keys / tokens\n• Credit card numbers", 40, 620, 480, 80, "danger"),
        Box("oklog", "SAFE TO LOG\n• correlation_id\n• model_id\n• input/output SIZE\n• latency_ms\n• validation_status", 580, 820, 500, 90, "success"),
        _instructor("Walk through Bedrock model access in console. Show one denied call when model not enabled — students remember IAM + access gate.", 40, 820, 480, 100),
    ])
    return d


def week03_decision() -> Diagram:
    d = Diagram(
        "04-week03",
        "Week 3 — AI Decision Engine",
        subtitle="Structured JSON outputs, schema validation, confidence gates, hybrid rules + AI",
        width=1700, height=1200,
    )
    d.boxes.append(_objective(
        "Treat the LLM as a probabilistic component. Enforce JSON schema, reject bad outputs, "
        "and route low-confidence results to human review.", 40, 78))
    d.nodes = [
        Node("in", "Ticket Text", "client", 60, 280, sublabel="input"),
        Node("rules", "Rules Engine", "lambda", 280, 180, fill="green", sublabel="keywords"),
        Node("br", "Bedrock", "bedrock", 280, 380, fill="dark", sublabel="JSON-only prompt"),
        Node("parse", "JSON Parser", "lambda", 500, 280, sublabel="strict parse"),
        Node("val", "Schema Validator", "lambda", 700, 280, fill="green", sublabel="enums + bounds"),
        Node("conf", "Confidence Gate", "lambda", 900, 280, fill="purple", sublabel="threshold 0.65"),
        Node("auto", "Auto Route", "api_gateway", 1120, 200, fill="purple"),
        Node("human", "Human Review", "user", 1120, 380, fill="gray"),
        Node("unk", "Fallback: unknown", "document", 900, 480, fill="gray"),
    ]
    d.edges = [
        Edge("d1", "in", "rules", "① obvious?", bold=True),
        Edge("d2", "in", "br", "② else LLM"),
        Edge("d3", "rules", "auto", "high conf.", color="#248814"),
        Edge("d4", "br", "parse"),
        Edge("d5", "parse", "val", "③ valid JSON?"),
        Edge("d6", "val", "conf", "④ schema OK"),
        Edge("d7", "conf", "auto", "⑤ conf >= 0.65"),
        Edge("d8", "conf", "human", "⑥ conf < 0.65", dashed=True, color="#DD3522"),
        Edge("d9", "parse", "unk", "invalid JSON", dashed=True, color="#DD3522"),
        Edge("d10", "val", "unk", "bad enum", dashed=True, color="#DD3522"),
    ]
    d.steps = [
        StepBadge(1, 60, 200), StepBadge(2, 260, 200), StepBadge(3, 480, 200),
        StepBadge(4, 680, 200), StepBadge(5, 880, 200), StepBadge(6, 1100, 200),
    ]
    d.boxes.extend([
        Box("schema", 'REQUIRED JSON SCHEMA\n{\n  "label": "billing|technical|security|general|unknown",\n  "confidence": 0.0-1.0,\n  "reason": "max 200 chars"\n}', 60, 520, 340, 120, "code"),
        Box("fail", "FAILURE MODES (discuss in class)\n• Non-JSON text\n• Missing keys\n• Invalid enum value\n• confidence out of range\n• reason too long", 440, 520, 320, 130, "danger"),
        Box("hybrid", "HYBRID PATTERN\nRules handle 30-40% obvious cases → cheaper, faster, auditable.\nLLM handles ambiguous language only.", 800, 520, 380, 90, "success"),
        _instructor("Demo: show valid JSON pass, then malformed output hitting fallback. Students must explain WHY validation is not optional.", 60, 680, 520, 90),
        _student("Downstream automation only consumes validated objects — never raw model text.", 600, 680, 400),
    ])
    return d


def week04_sfn() -> Diagram:
    d = Diagram(
        "05-week04",
        "Week 4 — Step Functions Orchestration",
        subtitle="Classify → validate → act with retries, catch, idempotency, and failure simulation",
        width=1700, height=1150,
    )
    d.boxes.append(_objective(
        "Model multi-step AI workflows as state machines. Use retries for transient errors, "
        "Catch for validation failures, and idempotency keys for safe replays.", 40, 78))
    d.zones = [
        Zone("z_sm", "STATE MACHINE (Week 4 Lab)", 40, 170, 1200, 380, "#E9F7EF"),
        Zone("z_rel", "RELIABILITY PATTERNS", 40, 580, 700, 280, "#EEF5FC"),
        Zone("z_fail", "FAILURE INJECTION (Lab 4.2)", 760, 580, 820, 280, "#FADBD8"),
    ]
    d.nodes = [
        Node("start", "Start", "client", 80, 300, w=56, h=56),
        Node("c", "Task: Classify", "lambda", 200, 280, sublabel="Bedrock invoke"),
        Node("v", "Task: Validate", "lambda", 400, 280, fill="green"),
        Node("choice", "Choice", "generic", 600, 280, fill="gray", sublabel="valid?"),
        Node("p", "Task: Persist", "lambda", 800, 200, sublabel="DynamoDB"),
        Node("f", "Task: Fallback", "lambda", 800, 380, fill="purple", sublabel="unknown label"),
        Node("end", "End", "client", 1000, 280, w=56, h=56),
        Node("retry", "Retry", "generic", 200, 450, fill="gray", sublabel="backoff 2s"),
        Node("dlq", "DLQ / Alert", "sns", 1000, 450, fill="red"),
    ]
    d.edges = [
        Edge("f1", "start", "c"),
        Edge("f2", "c", "v"),
        Edge("f3", "v", "choice"),
        Edge("f4", "choice", "p", "valid=true", color="#248814", bold=True),
        Edge("f5", "choice", "f", "valid=false", color="#DD3522", dashed=True),
        Edge("f6", "p", "end"),
        Edge("f7", "f", "end"),
        Edge("f8", "c", "retry", "throttle", dashed=True),
        Edge("f9", "retry", "c"),
        Edge("f10", "f", "dlq", "permanent fail", dashed=True, color="#DD3522"),
    ]
    d.boxes.extend([
        Box("retry_box", "RETRY CONFIG\n• IntervalSeconds: 2\n• MaxAttempts: 3\n• BackoffRate: 2.0\n• On: Lambda.ServiceException, Throttling", 60, 620, 320, 110, "code"),
        Box("idem", "IDEMPOTENCY\nKey: correlation_id\nStore: DynamoDB\nReplay safe: yes — no duplicate tickets", 400, 620, 320, 100, "success"),
        Box("sim", "LAB 4.2 — Simulate:\n1) Bedrock throttling → retry\n2) Invalid JSON → fallback path\n3) Downstream timeout → Catch → DLQ", 780, 620, 480, 110, "danger"),
        _instructor("Draw the execution graph in Step Functions console during demo. Show one failed execution and read the Cause field together.", 60, 860, 700, 90),
    ])
    return d


def week05_api() -> Diagram:
    d = Diagram(
        "06-week05",
        "Week 5 — AI Automation API Platform",
        subtitle="API Gateway + Lambda + Bedrock — contracts, auth, throttling, cost controls",
        width=1700, height=1200,
    )
    d.boxes.append(_objective(
        "Build three governed endpoints (/classify, /summarize, /route) with request validation, "
        "structured errors, correlation IDs, and rate limits.", 40, 78))
    d.nodes = [
        Node("clients", "Internal Apps", "client", 60, 320),
        Node("apigw", "API Gateway", "api_gateway", 280, 320, fill="purple", sublabel="HTTP API"),
        Node("waf", "Usage Plan", "waf", 280, 500, fill="red", sublabel="10 rps limit"),
        Node("lam", "Lambda", "lambda", 520, 320),
        Node("br", "Bedrock", "bedrock", 760, 240, fill="dark"),
        Node("val", "Validator", "lambda", 760, 400, fill="green"),
        Node("cw", "CloudWatch", "cloudwatch", 1000, 320, fill="red"),
        Node("ddb", "Audit", "dynamodb", 1000, 480, fill="blue"),
    ]
    d.edges = [
        Edge("a1", "clients", "apigw", "HTTPS"),
        Edge("a2", "apigw", "waf", "throttle"),
        Edge("a3", "apigw", "lam", "route"),
        Edge("a4", "lam", "br"),
        Edge("a5", "lam", "val"),
        Edge("a6", "lam", "cw", dashed=True),
        Edge("a7", "lam", "ddb", dashed=True),
    ]
    d.boxes.extend([
        Box("ep", "ENDPOINTS (Lab 5)\nPOST /classify — JSON label + confidence\nPOST /summarize — short summary\nPOST /route — team routing", 60, 520, 360, 100, "neutral"),
        Box("req", 'REQUEST (example)\nHeaders: X-Correlation-Id\nBody: { "text": "...", "label": "billing" }\nMax size: 8000 chars', 440, 520, 340, 110, "code"),
        Box("err", 'ERROR RESPONSE\n{ "correlation_id": "...",\n  "error": "input_too_large",\n  "max_chars": 8000 }', 800, 520, 340, 100, "danger"),
        Box("cost", "COST CONTROLS\n• max input/output length\n• temperature default 0.2\n• usage plan / burst limits\n• fail fast on abuse", 1160, 520, 300, 110, "success"),
        _instructor("Live demo: call each endpoint with curl. Show 400 on oversized payload and X-Correlation-Id in response.", 60, 680, 600, 90),
    ])
    return d


def week06_observability() -> Diagram:
    d = Diagram(
        "07-week06",
        "Week 6 — Observability, Governance & AI Safety",
        subtitle="Audit trails, dashboards, alerts, redaction policy, human-in-the-loop",
        width=1700, height=1200,
    )
    d.boxes.append(_objective(
        "Implement metadata-only audit logging, CloudWatch dashboards, cost alarms, "
        "and human approval branches for high-risk decisions.", 40, 78))
    d.nodes = [
        Node("wf", "AI Workflow", "step_functions", 80, 300, fill="green"),
        Node("api", "API Lambda", "lambda", 80, 440),
        Node("emit", "Audit Emitter", "lambda", 360, 360),
        Node("ddb", "DynamoDB\nAudit Store", "dynamodb", 600, 360, fill="blue"),
        Node("cw_dash", "Dashboard", "cloudwatch", 860, 300, fill="red"),
        Node("alarm", "SNS Alarm", "sns", 1100, 300, fill="red"),
        Node("hitl", "Human Approval", "user", 600, 560),
        Node("gov", "Governance\nChecklist", "document", 80, 600),
    ]
    d.edges = [
        Edge("o1", "wf", "emit", "AI event"),
        Edge("o2", "api", "emit"),
        Edge("o3", "emit", "ddb", "pk=CORR#id"),
        Edge("o4", "emit", "cw_dash", "metrics"),
        Edge("o5", "cw_dash", "alarm", "error rate"),
        Edge("o6", "wf", "hitl", "high risk", dashed=True, color="#DD3522"),
    ]
    d.boxes.extend([
        Box("audit_rec", "AUDIT RECORD (metadata only)\ncorrelation_id | timestamp | model_id\ninput_size | output_size | validation_status\nroute_or_action | latency_ms", 360, 520, 420, 110, "code"),
        Box("dash_m", "DASHBOARD WIDGETS\n• Request count\n• Error rate\n• p95 latency\n• Validation failures\n• Retry count", 860, 480, 380, 110, "neutral"),
        Box("gov_l", "GOVERNANCE CHECKLIST\n☐ Prompt version controlled\n☐ Model access reviewed\n☐ Log redaction policy\n☐ Budget alert configured\n☐ HITL for risky actions", 80, 720, 400, 130, "legend"),
        Box("nog", "NEVER STORE IN LOGS\nRaw customer PII, passwords, full card numbers, unredacted prompts in regulated industries", 520, 720, 400, 80, "danger"),
        _instructor("Query audit by correlation_id live. Trigger alarm with bad requests. Connect governance to real incident response.", 960, 720, 400, 100),
    ])
    return d


def week07_agent() -> Diagram:
    d = Diagram(
        "08-week07",
        "Week 7 — Enterprise AI Agent System",
        subtitle="Router, tool policy, memory with TTL, event-driven chaining",
        width=1700, height=1200,
    )
    d.boxes.append(_objective(
        "Build an agent-like router that outputs a structured plan, enforces tool allow-lists, "
        "stores session memory safely, and chains workflows via events.", 40, 78))
    d.nodes = [
        Node("evt", "EventBridge", "eventbridge", 60, 320, fill="red"),
        Node("agent", "Agent Router", "lambda", 300, 320, fill="purple", sublabel="plan JSON"),
        Node("pol", "Tool Policy", "iam", 300, 520, fill="red"),
        Node("sum", "Summarize WF", "lambda", 600, 200),
        Node("cls", "Classify+Route", "lambda", 600, 320),
        Node("act", "Action Stub", "lambda", 600, 440, fill="orange"),
        Node("mem", "Memory", "dynamodb", 900, 320, fill="blue", sublabel="TTL 7d"),
        Node("audit", "Audit", "cloudwatch", 900, 480, fill="red"),
        Node("appr", "Approval", "user", 600, 600),
    ]
    d.edges = [
        Edge("g1", "evt", "agent", "trigger"),
        Edge("g2", "agent", "pol", "check allow-list"),
        Edge("g3", "agent", "sum", "tool=summarize"),
        Edge("g4", "agent", "cls", "tool=classify_route"),
        Edge("g5", "agent", "act", "requires_approval", dashed=True, color="#DD3522"),
        Edge("g6", "act", "appr"),
        Edge("g7", "agent", "mem", "session summary"),
        Edge("g8", "agent", "audit"),
    ]
    d.boxes.extend([
        Box("plan", 'PLAN JSON (example)\n{\n  "tool": "classify_route",\n  "requires_approval": false,\n  "reason": "billing keywords"\n}', 60, 520, 360, 110, "code"),
        Box("pol_t", "TOOL POLICY\nALLOWED: summarize, classify_route, action_stub\nDENY: delete_prod, exfiltrate_data\nAPPROVAL: action_stub, security keywords", 440, 520, 400, 110, "danger"),
        Box("mem_r", "MEMORY RULES\nSTORE: short context summary, last route\nNEVER: secrets, full ticket bodies, PCI data\nTTL: 7 days (DynamoDB)", 900, 600, 380, 100, "success"),
        _instructor("Contrast 'autonomous agent' hype vs enterprise agent = router + policy + audit. Demo risky prompt requiring approval.", 60, 680, 550, 100),
    ])
    return d


def week08_capstone() -> Diagram:
    d = Diagram(
        "09-week08",
        "Week 8 — Capstone Architecture Options",
        subtitle="Four portfolio-ready systems — all must meet the production minimum bar",
        width=1700, height=1250,
    )
    d.boxes.append(_objective(
        "Deliver one capstone with orchestration, Bedrock, validation, audit, dashboard, and cost analysis. "
        "Choose the option closest to your target role.", 40, 78))
    d.zones = [
        Zone("o1", "OPTION 1 — AI Operations Assistant", 40, 170, 380, 320, "#EEF5FC"),
        Zone("o2", "OPTION 2 — File Automation Platform", 440, 170, 380, 320, "#E9F7EF"),
        Zone("o3", "OPTION 3 — Workflow Engine", 840, 170, 380, 320, "#F5F0FF"),
        Zone("o4", "OPTION 4 — Internal AI API Platform", 1240, 170, 400, 320, "#FFF8E6"),
        Zone("bar", "MINIMUM BAR (all options)", 40, 520, 1600, 120, "#FADBD8"),
    ]
    d.boxes.extend([
        Box("c1", "Flow:\nIncident → classify severity\n→ route to team → ticket stub\n→ human approval if critical", 60, 220, 340, 120, "neutral"),
        Box("c2", "Flow:\nS3 upload → extract metadata\n→ classify doc → route queue\n→ needs-review if low confidence", 460, 220, 340, 120, "neutral"),
        Box("c3", "Flow:\nAPI defines workflow type\n→ Step Functions template\n→ validate + branch + persist", 860, 220, 340, 120, "neutral"),
        Box("c4", "Flow:\n/classify /summarize /route\n→ shared governance layer\n→ per-team usage limits", 1260, 220, 360, 120, "neutral"),
        Box("min", "REQUIRED: Step Functions or equivalent | Bedrock | JSON validation | DynamoDB/S3 audit | CloudWatch dashboard + alarm | Cost/risk write-up | 12-min demo", 60, 560, 1560, 60, "danger"),
        Box("demo", "DEMO SCRIPT (12 min)\n① Problem + metrics (3m) ② Happy path (5m) ③ Failure + recovery (2m) ④ Cost/governance (2m)", 40, 680, 500, 100, "code"),
        _instructor("Use capstone reviews to test architecture thinking — not just 'does it run'. Ask about failure modes and cost drivers.", 580, 680, 500, 100),
    ])
    d.nodes = [
        Node("br", "Bedrock", "bedrock", 720, 860, fill="dark"),
        Node("gov", "Governance", "cloudwatch", 1000, 860, fill="red"),
        Node("sfn", "Orchestration", "step_functions", 480, 860, fill="green"),
    ]
    d.edges = [
        Edge("x1", "sfn", "br"),
        Edge("x2", "br", "gov", dashed=True),
    ]
    return d


def iam_model() -> Diagram:
    d = Diagram(
        "10-iam",
        "IAM & Security Boundaries",
        subtitle="Separate deploy roles, runtime roles, and API caller identity",
        width=1600, height=1000,
    )
    d.boxes.append(_objective("Understand who can deploy infrastructure vs who can invoke AI vs who can call APIs.", 40, 78))
    d.zones = [
        Zone("humans", "HUMAN & MACHINE IDENTITIES", 40, 170, 480, 450, "#EEF5FC"),
        Zone("roles", "IAM ROLES", 540, 170, 500, 450, "#FADBD8"),
        Zone("resources", "PROTECTED RESOURCES", 1060, 170, 500, 450, "#E9F7EF"),
    ]
    d.nodes = [
        Node("admin", "Admin / Instructor", "user", 80, 260),
        Node("dev", "Developer", "user", 80, 380),
        Node("caller", "API Client", "cognito", 80, 500),
        Node("deploy", "Deploy Role", "iam", 600, 260, fill="red"),
        Node("runtime", "Lambda Role", "iam", 600, 380, fill="red"),
        Node("br", "Bedrock Models", "bedrock", 1120, 280, fill="dark"),
        Node("data", "DynamoDB / S3", "dynamodb", 1120, 420, fill="blue"),
        Node("logs", "CloudWatch Logs", "cloudwatch", 1320, 350, fill="red"),
    ]
    d.edges = [
        Edge("i1", "admin", "deploy", "CloudFormation/SAM"),
        Edge("i2", "dev", "deploy", "scoped"),
        Edge("i3", "deploy", "runtime", "creates"),
        Edge("i4", "runtime", "br", "Converse only"),
        Edge("i5", "runtime", "data", "table ARNs"),
        Edge("i6", "runtime", "logs", "PutLogEvents"),
        Edge("i7", "caller", "runtime", "invoke via API", dashed=True),
    ]
    d.boxes.append(_instructor("Blast radius: compromise of runtime role ≠ full admin. Use separate accounts per student.", 40, 660, 700, 80))
    return d


def labs_deployed() -> Diagram:
    d = Diagram(
        "11-labs",
        "Course Labs — Deployed SAM Stack",
        subtitle="What ./scripts/cycle.sh deploys and verifies on AWS",
        width=1700, height=1200,
    )
    d.boxes.append(_objective(
        "Map each weekly lab to a live AWS resource. Use correlation_id to trace API → Lambda → audit → dashboard.", 40, 78))
    d.zones = [
        Zone("z_api", "WEEK 5 — HTTP API", 40, 170, 500, 350, "#F5F0FF"),
        Zone("z_sfn", "WEEK 4 — STEP FUNCTIONS", 560, 170, 500, 350, "#E9F7EF"),
        Zone("z_data", "WEEKS 6-7 — DATA", 1080, 170, 560, 350, "#EEF5FC"),
        Zone("z_ops", "WEEK 6 — OBSERVABILITY", 40, 560, 1600, 200, "#FFF8E6"),
    ]
    d.nodes = [
        Node("api", "API Gateway", "api_gateway", 80, 280, fill="purple"),
        Node("lapi", "ApiFunction", "lambda", 280, 280),
        Node("l2", "Week2Invoke", "lambda", 280, 400, sublabel="Week 2"),
        Node("sfn", "State Machine", "step_functions", 620, 280, fill="green"),
        Node("lcl", "Classify", "lambda", 620, 400),
        Node("lv", "Validate", "lambda", 780, 400, fill="green"),
        Node("lag", "Agent", "lambda", 280, 520, fill="purple"),
        Node("br", "Bedrock Nova Lite", "bedrock", 900, 260, fill="dark"),
        Node("aud", "Audit Table", "dynamodb", 1140, 280, fill="blue"),
        Node("mem", "Memory Table", "dynamodb", 1140, 400, fill="blue"),
        Node("res", "Results Table", "dynamodb", 1140, 520, fill="blue"),
        Node("dash", "Dashboard", "cloudwatch", 700, 620, fill="red"),
        Node("alm", "Error Alarm", "sns", 1000, 620, fill="red"),
    ]
    d.edges = [
        Edge("l0", "api", "lapi"),
        Edge("l1", "lapi", "br"),
        Edge("l2", "lcl", "br"),
        Edge("l3", "lag", "br"),
        Edge("l4", "sfn", "lcl"),
        Edge("l5", "sfn", "lv"),
        Edge("l6", "lapi", "aud", dashed=True),
        Edge("l7", "lag", "mem"),
        Edge("l8", "lv", "res"),
        Edge("l9", "lapi", "dash", dashed=True),
        Edge("l10", "dash", "alm"),
    ]
    d.boxes.extend([
        Box("verify", "VERIFY: ./scripts/cycle.sh\nUnit tests → deploy → integration tests → teardown", 40, 800, 400, 70, "code"),
        Box("endpoints", "LIVE ENDPOINTS\nPOST /classify\nPOST /summarize\nPOST /route", 460, 800, 300, 80, "success"),
        _student("After deploy, query audit: python week06/query_audit.py <correlation_id>", 800, 800, 400),
    ])
    return d


DIAGRAMS = [
    ref_architecture, week01_landscape, week02_secure, week03_decision,
    week04_sfn, week05_api, week06_observability, week07_agent,
    week08_capstone, iam_model, labs_deployed,
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for factory in DIAGRAMS:
        diagram = factory()
        xml = DrawioBuilder(diagram).build()
        path = OUT / f"{diagram.name}.drawio"
        path.write_text(xml, encoding="utf-8")
        print(f"Wrote {path.name} ({diagram.width}x{diagram.height})")
    print(f"\nGenerated {len(DIAGRAMS)} detailed diagrams.")


if __name__ == "__main__":
    main()
