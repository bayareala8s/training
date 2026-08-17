"""Step Functions task — enrich triage record after classify/validate."""

from __future__ import annotations

from common.bedrock_client import converse
from common.prompts import SUMMARIZE_SYSTEM, SUMMARIZE_USER_TEMPLATE
from week08.services.incident_triage import OWNER_BY_ROUTE, score_severity


def handler(event, context):
    text = event.get("text", "")
    correlation_id = event.get("correlation_id", "unknown")
    classification = event.get("classification", {})
    validation = event.get("validation", {})

    summary_out = converse(
        SUMMARIZE_USER_TEMPLATE.format(text=text[:8000]),
        system=SUMMARIZE_SYSTEM,
        temperature=0.2,
    )

    validated = validation.get("validated", {})
    label = validated.get("label") or classification.get("result", {}).get("label", "general")
    gated = {
        "route": validated.get("route", "human_review") if validation.get("valid") else "human_review",
        "low_confidence": not validation.get("valid", False),
        "valid": validation.get("valid", False),
    }
    severity_info = score_severity(text, label, gated)
    team = gated["route"]
    owner = OWNER_BY_ROUTE.get(team, "ops-triage")

    return {
        "correlation_id": correlation_id,
        "summary": summary_out["text"],
        "severity": severity_info["severity"],
        "severity_reasons": severity_info["reasons"],
        "owner": owner,
        "team": team,
        "ticket_stub": {
            "ticket_id": f"INC-{correlation_id[:8].upper()}",
            "team": team,
            "owner": owner,
            "severity": severity_info["severity"],
            "status": "open",
        },
        "classification": classification,
        "validation": validation,
        "triage_ready": True,
    }
