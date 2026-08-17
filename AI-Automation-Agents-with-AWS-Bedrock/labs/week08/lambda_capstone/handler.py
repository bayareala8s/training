"""
Week 8 — Capstone API: /capstone/incident, /document, /approval/*, /agent
"""

from __future__ import annotations

from common.api_utils import (
    api_response,
    check_text_input,
    get_correlation_id,
    parse_body,
    resolve_route,
)
from week08.services.approval_workflow import decide_approval, request_approval
from week08.services.doc_classification import classify_document
from week08.services.enterprise_agent import run_enterprise_agent
from week08.services.incident_triage import triage_incident


def handler(event, context):
    route = resolve_route(event)
    method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod", "POST")

    if method != "POST":
        return api_response(405, {"error": "method_not_allowed"})

    body, err = parse_body(event)
    if err:
        return api_response(400, {"error": err})

    correlation_id = get_correlation_id(event, body)

    if "incident" in route:
        text = body.get("text", "")
        if size_err := check_text_input(text, correlation_id):
            return size_err
        return api_response(200, triage_incident(text, correlation_id=correlation_id), correlation_id)

    if "document" in route:
        text = body.get("document_text") or body.get("text", "")
        if size_err := check_text_input(text, correlation_id):
            return size_err
        return api_response(
            200,
            classify_document(
                text,
                correlation_id=correlation_id,
                doc_type_hint=body.get("doc_type_hint"),
                source_uri=body.get("source_uri"),
                content_type=body.get("content_type"),
            ),
            correlation_id,
        )

    if "approval" in route and "request" in route:
        action_text = body.get("action_text") or body.get("text", "")
        if size_err := check_text_input(action_text, correlation_id):
            return size_err
        result = request_approval(
            action_text,
            correlation_id=correlation_id,
            risk_level=body.get("risk_level", "auto"),
            requester_id=body.get("requester_id", "student"),
        )
        status = 202 if result.get("status") == "pending_approval" else 200
        return api_response(status, result, correlation_id)

    if "approval" in route and "decide" in route:
        approval_id = body.get("approval_id")
        decision = body.get("decision")
        if not approval_id or not decision:
            return api_response(400, {"error": "approval_id_and_decision_required"}, correlation_id)
        result = decide_approval(
            approval_id, decision, correlation_id=correlation_id, approver_id=body.get("approver_id", "approver")
        )
        code = 404 if result.get("error") == "approval_not_found" else 200
        if result.get("error") in {"invalid_state", "invalid_decision"}:
            code = 400
        return api_response(code, result, correlation_id)

    if "agent" in route:
        text = body.get("text", "")
        if size_err := check_text_input(text, correlation_id):
            return size_err
        return api_response(
            200,
            run_enterprise_agent(
                text, correlation_id=correlation_id, session_id=body.get("session_id"), tool_hint=body.get("tool_hint")
            ),
            correlation_id,
        )

    return api_response(
        404,
        {"error": "not_found", "hint": "use /capstone/incident|document|approval/request|approval/decide|agent"},
        correlation_id,
    )
