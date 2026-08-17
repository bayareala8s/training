"""
Option A — AI Operations / Incident Triage Platform.

Flow: summarize → classify → route → confidence gate → severity → ticket → notify → persist → audit.
"""

from __future__ import annotations

import re

from common.audit import write_audit_event
from common.bedrock_client import converse
from common.prompts import SUMMARIZE_SYSTEM, SUMMARIZE_USER_TEMPLATE
from common.validation import apply_confidence_gate
from week03.classify_service import classify_text
from week03.route_service import route_request
from week08.services.persist import notify_stub, persist_result

# Keyword boosts for severity (deterministic, explainable in demos)
CRITICAL_PATTERN = re.compile(
    r"\b(outage|data\s*breach|ransomware|customer[- ]facing\s+down|p0|sev[- ]?1)\b",
    re.I,
)
HIGH_PATTERN = re.compile(
    r"\b(503|500|crash|failover|production|prod\b|security|credential|latency\s+spike)\b",
    re.I,
)

OWNER_BY_ROUTE = {
    "team_billing": "billing-oncall",
    "team_engineering": "platform-oncall",
    "team_security": "security-oncall",
    "team_general": "ops-triage",
    "human_review": "ops-manager",
}


def score_severity(text: str, label: str, gated_route: dict) -> dict:
    """Deterministic severity scoring with explainable reasons."""
    reasons: list[str] = []
    if gated_route.get("route") == "human_review" or gated_route.get("low_confidence"):
        return {"severity": "needs_review", "reasons": ["low_confidence_or_human_review"]}

    if CRITICAL_PATTERN.search(text):
        return {"severity": "critical", "reasons": ["critical_keyword_match"]}

    if label == "security":
        reasons.append("security_label")
        severity = "high"
    elif label == "technical" and HIGH_PATTERN.search(text):
        reasons.append("technical_plus_prod_signal")
        severity = "high"
    elif HIGH_PATTERN.search(text) or label in {"technical", "security"}:
        reasons.append("high_signal_or_label")
        severity = "high"
    elif label == "billing":
        reasons.append("billing_label")
        severity = "medium"
    else:
        reasons.append("default")
        severity = "medium"

    return {"severity": severity, "reasons": reasons}


def triage_incident(text: str, *, correlation_id: str) -> dict:
    """End-to-end incident triage for Capstone Option A."""
    summary_out = converse(
        SUMMARIZE_USER_TEMPLATE.format(text=text[:8000]),
        system=SUMMARIZE_SYSTEM,
        temperature=0.2,
    )
    classification = classify_text(text, correlation_id=correlation_id)
    label = classification.get("result", {}).get("label", "general")
    routing = route_request(text, correlation_id=correlation_id, label=label)

    route_result = routing.get("result", routing)
    gated = apply_confidence_gate(route_result) if route_result.get("valid") else route_result

    severity_info = score_severity(text, label, gated)
    severity = severity_info["severity"]
    team = gated.get("route", "human_review")
    owner = OWNER_BY_ROUTE.get(team, "ops-triage")

    ticket_stub = {
        "ticket_id": f"INC-{correlation_id[:8].upper()}",
        "team": team,
        "owner": owner,
        "severity": severity,
        "title": (summary_out["text"] or text)[:120].strip(),
        "status": "open",
    }

    notification = None
    if severity in {"critical", "high"}:
        notification = notify_stub(
            "incident_high_severity",
            f"[{severity.upper()}] {ticket_stub['ticket_id']} → {owner}: {ticket_stub['title']}",
            correlation_id=correlation_id,
        )

    package = {
        "correlation_id": correlation_id,
        "capstone_option": "incident_triage",
        "summary": summary_out["text"],
        "classification": classification,
        "routing": {**routing, "result": gated},
        "severity": severity_info,
        "ticket_stub": ticket_stub,
        "notification": notification,
        "stored": persist_result(
            correlation_id,
            status="triage_completed",
            capstone_option="incident_triage",
            payload={
                "summary": summary_out["text"][:500],
                "label": label,
                "route": team,
                "severity": severity,
                "owner": owner,
                "ticket_id": ticket_stub["ticket_id"],
            },
        ),
    }

    write_audit_event(
        correlation_id=correlation_id,
        event_type="capstone_incident_triage",
        model_id=summary_out["model_id"],
        input_size=len(text),
        output_size=len(summary_out["text"]),
        validation_status="valid" if classification.get("valid") else "fallback",
        route_or_action=team,
        latency_ms=summary_out["latency_ms"],
        extra={
            "severity": severity,
            "ticket_id": ticket_stub["ticket_id"],
            "owner": owner,
            "notify": (notification or {}).get("delivery"),
        },
    )
    return package
