"""Lab 3.1 — Classification service logic (used by Lambda and tests)."""

from __future__ import annotations

from common.audit import write_audit_event
from common.bedrock_client import converse, parse_json_from_text
from common.prompts import CLASSIFY_STRICT_SUFFIX, CLASSIFY_SYSTEM, CLASSIFY_USER_TEMPLATE
from common.validation import validate_classification


def classify_text(text: str, *, correlation_id: str, use_bedrock: bool = True) -> dict:
    prompt = CLASSIFY_USER_TEMPLATE.format(text=text[:4000]) + CLASSIFY_STRICT_SUFFIX

    if not use_bedrock:
        # For unit tests without AWS
        return {
            "correlation_id": correlation_id,
            "source": "mock",
            "result": {"label": "unknown", "confidence": 0.0, "reason": "mock", "valid": True},
        }

    raw = converse(prompt, system=CLASSIFY_SYSTEM, temperature=0.1)
    try:
        parsed = parse_json_from_text(raw["text"])
        ok, validated, errors = validate_classification(parsed)
    except (ValueError, Exception):
        ok, validated, errors = False, {
            "label": "unknown",
            "confidence": 0.0,
            "reason": "parse_failed",
            "valid": False,
        }, ["parse_failed"]

    write_audit_event(
        correlation_id=correlation_id,
        event_type="classify",
        model_id=raw["model_id"],
        input_size=len(text),
        output_size=len(raw["text"]),
        validation_status="valid" if ok else "invalid",
        route_or_action=validated.get("label"),
        latency_ms=raw["latency_ms"],
        success=ok,
        extra={"errors": errors} if errors else None,
    )

    return {
        "correlation_id": correlation_id,
        "latency_ms": raw["latency_ms"],
        "valid": ok,
        "result": validated,
        "errors": errors,
    }
