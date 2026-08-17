"""
Lab 7 — Agent router: structured plan + tool policy + memory.
"""

from __future__ import annotations

import json
import re
import uuid

from common.audit import write_audit_event
from common.bedrock_client import converse, parse_json_from_text
from common.memory import get_memory, put_memory
from common.prompts import AGENT_PLAN_SYSTEM
from week03.classify_service import classify_text
from week03.route_service import route_request

ALLOWED_TOOLS = frozenset({"summarize", "classify_route", "action_stub"})
RISKY_KEYWORDS = re.compile(r"\b(delete|drop|production|root|credential)\b", re.I)


def handler(event, context):
    correlation_id = event.get("correlation_id") or str(uuid.uuid4())
    session_id = event.get("session_id", correlation_id)
    text = event.get("text", "")

    memory = get_memory(session_id) or {}
    memory_hint = memory.get("context_summary", "")

    plan_prompt = f"""Request:\n{text}\n\nPrior context summary: {memory_hint or 'none'}"""
    raw = converse(plan_prompt, system=AGENT_PLAN_SYSTEM, temperature=0.1)

    try:
        plan = parse_json_from_text(raw["text"])
        tool = plan.get("tool", "classify_route")
        requires_approval = bool(plan.get("requires_approval", False))
    except (ValueError, json.JSONDecodeError):
        tool = "classify_route"
        requires_approval = True
        plan = {"tool": tool, "requires_approval": True, "reason": "plan_parse_failed"}

    if tool not in ALLOWED_TOOLS:
        tool = "classify_route"
        requires_approval = True

    if RISKY_KEYWORDS.search(text):
        requires_approval = True

    policy_decision = "deny_pending_approval" if requires_approval and tool == "action_stub" else "allow"

    result: dict = {
        "correlation_id": correlation_id,
        "session_id": session_id,
        "plan": plan,
        "tool": tool,
        "policy_decision": policy_decision,
    }

    if policy_decision.startswith("deny"):
        result["output"] = {"status": "pending_approval", "message": "Action requires human approval"}
    elif tool == "summarize":
        from common.prompts import SUMMARIZE_USER_TEMPLATE, SUMMARIZE_SYSTEM

        out = converse(SUMMARIZE_USER_TEMPLATE.format(text=text), system=SUMMARIZE_SYSTEM)
        result["output"] = {"summary": out["text"]}
    elif tool == "classify_route":
        c = classify_text(text, correlation_id=correlation_id)
        label = c.get("result", {}).get("label", "general")
        r = route_request(text, correlation_id=correlation_id, label=label)
        result["output"] = {"classification": c, "routing": r}
    else:
        result["output"] = {"status": "action_stub", "ticket_id": f"STUB-{correlation_id[:8]}"}

    summary = f"tool={tool}; policy={policy_decision}"
    put_memory(session_id, context_summary=summary, last_route=tool, last_action=policy_decision)

    write_audit_event(
        correlation_id=correlation_id,
        event_type="agent_route",
        model_id=raw["model_id"],
        input_size=len(text),
        output_size=len(raw["text"]),
        validation_status="valid",
        route_or_action=tool,
        latency_ms=raw["latency_ms"],
        extra={"policy": policy_decision},
    )

    return result
