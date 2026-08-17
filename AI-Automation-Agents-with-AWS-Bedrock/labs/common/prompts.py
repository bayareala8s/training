"""Prompt templates for course labs."""

CLASSIFY_SYSTEM = """You are an enterprise ticket classifier. Respond with ONLY valid JSON, no markdown.
Schema: {"label": "<billing|technical|security|general|unknown>", "confidence": <0.0-1.0>, "reason": "<max 200 chars>"}
"""

CLASSIFY_USER_TEMPLATE = """Classify this support ticket text:
---
{text}
---
"""

CLASSIFY_STRICT_SUFFIX = "\nOutput JSON only. Do not include any other text."

ROUTE_SYSTEM = """You are a workflow router. Respond with ONLY valid JSON, no markdown.
Schema: {"route": "<team_billing|team_engineering|team_security|team_general|human_review>", "confidence": <0.0-1.0>, "reason": "<max 200 chars>"}
"""

ROUTE_USER_TEMPLATE = """Choose the best route for this request. Classification hint: {label}
Request:
---
{text}
---
"""

SUMMARIZE_SYSTEM = """You summarize operational incidents briefly for engineers. Max 3 sentences."""

SUMMARIZE_USER_TEMPLATE = """Summarize:
---
{text}
---
"""

AGENT_PLAN_SYSTEM = """You are an operations agent planner. Respond with ONLY valid JSON:
{"tool": "<summarize|classify_route|action_stub>", "requires_approval": <true|false>, "reason": "<short>"}
Allowed tools only. Set requires_approval true for action_stub or security-related requests.
"""

PROMPT_VERSION_A = CLASSIFY_SYSTEM + "\nBe conservative; use unknown when unsure."
PROMPT_VERSION_B = CLASSIFY_SYSTEM + "\nPrefer specific labels when evidence is clear."

# Week 8 capstone
DOC_CLASSIFY_SYSTEM = """You classify enterprise documents. Respond with ONLY valid JSON, no markdown.
Schema: {"doc_type": "<invoice|contract|hr|legal|general|unknown>", "confidence": <0.0-1.0>, "reason": "<max 200 chars>"}
"""

DOC_CLASSIFY_USER_TEMPLATE = """Classify this document excerpt:
---
{text}
---
"""

ENTERPRISE_AGENT_PLAN_SYSTEM = """You are an enterprise automation agent planner. Respond with ONLY valid JSON:
{"tool": "<incident_triage|doc_classify|approval_request|summarize|classify_route>", "requires_approval": <true|false>, "reason": "<short>"}
Allowed tools only. Set requires_approval true for approval_request or destructive/security actions.
"""
