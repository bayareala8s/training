"""Lab 3.2 — Hybrid routing (rules + AI + confidence gate)."""

from __future__ import annotations

import re

from common.audit import write_audit_event
from common.bedrock_client import converse, parse_json_from_text
from common.config import CONFIDENCE_THRESHOLD
from common.prompts import ROUTE_SYSTEM, ROUTE_USER_TEMPLATE
from common.validation import apply_confidence_gate, validate_route

RULE_PATTERNS: list[tuple[re.Pattern, str, float]] = [
    (re.compile(r"\b(invoice|billing|charge|refund|payment)\b", re.I), "team_billing", 0.95),
    (re.compile(r"\b(hack|breach|soc2|security|unauthorized)\b", re.I), "team_security", 0.95),
    (re.compile(r"\b(503|500|deploy|kubernetes|api|latency)\b", re.I), "team_engineering", 0.9),
]


def rules_route(text: str) -> dict | None:
    for pattern, route, confidence in RULE_PATTERNS:
        if pattern.search(text):
            return {
                "route": route,
                "confidence": confidence,
                "reason": "rules_match",
                "valid": True,
                "source": "rules",
            }
    return None


def ai_route(text: str, label: str, *, correlation_id: str) -> dict:
    prompt = ROUTE_USER_TEMPLATE.format(label=label, text=text[:4000])
    raw = converse(prompt, system=ROUTE_SYSTEM, temperature=0.1)
    try:
        parsed = parse_json_from_text(raw["text"])
        ok, validated, errors = validate_route(parsed)
    except (ValueError, Exception):
        ok, validated, errors = False, {
            "route": "human_review",
            "confidence": 0.0,
            "reason": "parse_failed",
            "valid": False,
        }, ["parse_failed"]

    if ok:
        validated = apply_confidence_gate(validated, threshold=CONFIDENCE_THRESHOLD)

    write_audit_event(
        correlation_id=correlation_id,
        event_type="route",
        model_id=raw["model_id"],
        input_size=len(text),
        output_size=len(raw["text"]),
        validation_status="valid" if ok else "invalid",
        route_or_action=validated.get("route"),
        latency_ms=raw["latency_ms"],
        success=ok,
    )

    return {
        "correlation_id": correlation_id,
        "source": "ai",
        "valid": ok,
        "result": validated,
        "errors": errors,
        "latency_ms": raw["latency_ms"],
    }


def route_request(text: str, *, correlation_id: str, label: str = "general") -> dict:
    ruled = rules_route(text)
    if ruled:
        write_audit_event(
            correlation_id=correlation_id,
            event_type="route",
            validation_status="valid",
            route_or_action=ruled["route"],
            success=True,
            extra={"source": "rules"},
        )
        return {"correlation_id": correlation_id, **ruled}

    return ai_route(text, label, correlation_id=correlation_id)
