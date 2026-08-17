"""Step Functions task — evaluate approval risk for orchestrated workflow."""

from __future__ import annotations

from week08.services.approval_workflow import _evaluate_risk, request_approval


def handler(event, context):
    action_text = event.get("action_text") or event.get("text", "")
    correlation_id = event.get("correlation_id", "unknown")
    risk_level = event.get("risk_level", "auto")

    evaluation = _evaluate_risk(action_text, risk_level)
    result = request_approval(
        action_text,
        correlation_id=correlation_id,
        risk_level=risk_level,
        requester_id=event.get("requester_id", "sfn"),
    )
    return {
        "correlation_id": correlation_id,
        "evaluation": evaluation,
        "approval": result,
        "requires_approval": evaluation["requires_approval"],
    }
