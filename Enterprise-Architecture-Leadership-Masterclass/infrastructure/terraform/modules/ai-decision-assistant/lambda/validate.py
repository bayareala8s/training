"""Validate decision JSON and apply deterministic HITL / routing rules."""
from __future__ import annotations

import json
import os
import time
from typing import Any

import boto3

TABLE_NAME = os.environ["DECISIONS_TABLE"]
ALLOWED_SEVERITY = {"low", "medium", "high", "critical"}
FORCE_HITL_CATEGORIES = {"security", "ai_governance", "data_integrity"}

ddb = boto3.resource("dynamodb")
table = ddb.Table(TABLE_NAME)


def _validate(decision: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "category",
        "severity",
        "business_impact",
        "routing_team",
        "next_actions",
        "hitl_required",
        "confidence",
    ]
    for key in required:
        if key not in decision:
            errors.append(f"missing:{key}")
    sev = str(decision.get("severity", "")).lower()
    if sev and sev not in ALLOWED_SEVERITY:
        errors.append("invalid:severity")
    if "next_actions" in decision and not isinstance(decision["next_actions"], list):
        errors.append("invalid:next_actions")
    conf = decision.get("confidence")
    try:
        if conf is not None and not (0.0 <= float(conf) <= 1.0):
            errors.append("invalid:confidence")
    except (TypeError, ValueError):
        errors.append("invalid:confidence")
    return errors


def _apply_rules(decision: dict[str, Any]) -> dict[str, Any]:
    out = dict(decision)
    sev = str(out.get("severity", "")).lower()
    cat = str(out.get("category", "")).lower()
    out["severity"] = sev
    out["category"] = cat
    hitl = bool(out.get("hitl_required", False))
    reasons: list[str] = []
    if sev in ("high", "critical"):
        hitl = True
        reasons.append("severity_gate")
    if cat in FORCE_HITL_CATEGORIES:
        hitl = True
        reasons.append("category_gate")
    try:
        if float(out.get("confidence", 1.0)) < 0.5:
            hitl = True
            reasons.append("confidence_gate")
    except (TypeError, ValueError):
        hitl = True
        reasons.append("confidence_unreadable")
    impact = str(out.get("business_impact", "")).lower()
    if "payment" in impact and sev in ("high", "critical"):
        if not out.get("routing_team"):
            out["routing_team"] = "payments-sre"
        reasons.append("payments_impact_rule")
    out["hitl_required"] = hitl
    out["rule_reasons"] = reasons
    return out


def handler(event, context):
    incident_id = event["incident_id"]
    metrics = event.get("metrics", {})
    decision = event.get("decision") or {}
    errors = _validate(decision)
    now = int(time.time())

    if errors:
        table.put_item(
            Item={
                "incident_id": incident_id,
                "status": "validation_failed",
                "errors": errors,
                "raw_decision": json.dumps(decision),
                "metrics": json.dumps(metrics),
                "updated_at": now,
            }
        )
        return {
            "incident_id": incident_id,
            "status": "validation_failed",
            "errors": errors,
            "hitl_required": True,
            "decision": decision,
            "metrics": metrics,
        }

    final = _apply_rules(decision)
    status = "pending_hitl" if final["hitl_required"] else "accepted"
    table.put_item(
        Item={
            "incident_id": incident_id,
            "status": status,
            "decision": json.dumps(final),
            "category": final.get("category", ""),
            "severity": final.get("severity", ""),
            "routing_team": final.get("routing_team", ""),
            "hitl_required": bool(final.get("hitl_required", False)),
            "metrics": json.dumps(metrics),
            "updated_at": now,
        }
    )
    return {
        "incident_id": incident_id,
        "status": status,
        "hitl_required": final["hitl_required"],
        "decision": final,
        "metrics": metrics,
    }
