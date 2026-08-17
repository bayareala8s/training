"""
Option D — Enterprise Agent with tool policy and memory.

Tools: incident_triage, doc_classify, approval_request, summarize, classify_route.
Deterministic tool_hint supported for reliable demos.
"""

from __future__ import annotations

import json
import re
import uuid

from common.audit import write_audit_event
from common.bedrock_client import converse, parse_json_from_text
from common.memory import get_memory, put_memory
from common.prompts import ENTERPRISE_AGENT_PLAN_SYSTEM, SUMMARIZE_SYSTEM, SUMMARIZE_USER_TEMPLATE
from week03.classify_service import classify_text
from week03.route_service import route_request
from week08.services.approval_workflow import request_approval
from week08.services.doc_classification import classify_document
from week08.services.incident_triage import triage_incident

ALLOWED_TOOLS = frozenset({
    "incident_triage",
    "doc_classify",
    "approval_request",
    "summarize",
    "classify_route",
})
RISKY_KEYWORDS = re.compile(r"\b(delete|drop|production|root|credential|wipe|shutdown)\b", re.I)

# Keyword hints when model plan is ambiguous (still overridden by explicit tool_hint)
TOOL_HINTS = (
    (re.compile(r"\b(incident|outage|503|crash|pod|alert)\b", re.I), "incident_triage"),
    (re.compile(r"\b(invoice|contract|document|pdf|hr form)\b", re.I), "doc_classify"),
    (re.compile(r"\b(delete|revoke|credential|approve|permission)\b", re.I), "approval_request"),
    (re.compile(r"\b(summarize|summary|tl;dr)\b", re.I), "summarize"),
)


def _infer_tool(text: str) -> str | None:
    for pattern, tool in TOOL_HINTS:
        if pattern.search(text):
            return tool
    return None


def run_enterprise_agent(
    text: str,
    *,
    correlation_id: str | None = None,
    session_id: str | None = None,
    tool_hint: str | None = None,
) -> dict:
    """Route request to the appropriate enterprise tool with policy enforcement."""
    correlation_id = correlation_id or str(uuid.uuid4())
    session_id = session_id or correlation_id

    memory = get_memory(session_id) or {}
    memory_hint = memory.get("context_summary", "")

    # Deterministic path for demos / tests
    if tool_hint and tool_hint in ALLOWED_TOOLS:
        tool = tool_hint
        requires_approval = tool == "approval_request" or bool(RISKY_KEYWORDS.search(text))
        plan = {
            "tool": tool,
            "requires_approval": requires_approval,
            "reason": "explicit_tool_hint",
        }
        raw = {"model_id": "tool-hint", "text": json.dumps(plan), "latency_ms": 0}
    else:
        plan_prompt = f"""Request:\n{text}\n\nPrior context: {memory_hint or 'none'}"""
        raw = converse(plan_prompt, system=ENTERPRISE_AGENT_PLAN_SYSTEM, temperature=0.1)
        try:
            plan = parse_json_from_text(raw["text"])
            tool = plan.get("tool", "classify_route")
            requires_approval = bool(plan.get("requires_approval", False))
        except (ValueError, json.JSONDecodeError):
            inferred = _infer_tool(text) or "classify_route"
            tool = inferred
            requires_approval = True
            plan = {"tool": tool, "requires_approval": True, "reason": "plan_parse_failed_inferred"}

    if tool not in ALLOWED_TOOLS:
        tool = _infer_tool(text) or "classify_route"
        requires_approval = True
        plan["tool"] = tool
        plan["policy_override"] = "tool_not_allowed"

    if RISKY_KEYWORDS.search(text):
        requires_approval = True
        plan["requires_approval"] = True

    policy_decision = "allow"
    if requires_approval and tool == "approval_request":
        policy_decision = "allow"
    elif requires_approval:
        policy_decision = "deny_pending_approval"

    result: dict = {
        "correlation_id": correlation_id,
        "session_id": session_id,
        "capstone_option": "enterprise_agent",
        "plan": plan,
        "tool": tool,
        "policy_decision": policy_decision,
        "memory_used": bool(memory_hint),
    }

    if policy_decision.startswith("deny"):
        result["output"] = {
            "status": "pending_approval",
            "message": "Use /capstone/approval/request for high-risk actions",
            "suggested_tool": "approval_request",
        }
    elif tool == "incident_triage":
        result["output"] = triage_incident(text, correlation_id=correlation_id)
    elif tool == "doc_classify":
        result["output"] = classify_document(text, correlation_id=correlation_id)
    elif tool == "approval_request":
        result["output"] = request_approval(text, correlation_id=correlation_id, risk_level="high")
    elif tool == "summarize":
        out = converse(SUMMARIZE_USER_TEMPLATE.format(text=text), system=SUMMARIZE_SYSTEM)
        result["output"] = {"summary": out["text"], "latency_ms": out["latency_ms"]}
    else:
        c = classify_text(text, correlation_id=correlation_id)
        label = c.get("result", {}).get("label", "general")
        r = route_request(text, correlation_id=correlation_id, label=label)
        result["output"] = {"classification": c, "routing": r}

    summary = f"tool={tool}; policy={policy_decision}"
    put_memory(session_id, context_summary=summary, last_route=tool, last_action=policy_decision)

    write_audit_event(
        correlation_id=correlation_id,
        event_type="capstone_enterprise_agent",
        model_id=raw["model_id"],
        input_size=len(text),
        output_size=len(raw["text"]),
        validation_status="valid",
        route_or_action=tool,
        latency_ms=raw["latency_ms"],
        extra={"policy": policy_decision, "session_id": session_id},
    )
    return result
