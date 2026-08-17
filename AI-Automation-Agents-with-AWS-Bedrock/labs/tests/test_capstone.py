"""Week 8 capstone unit tests (no AWS / Bedrock required)."""

from __future__ import annotations

from week08.services.approval_workflow import _evaluate_risk, _execute_stub
from week08.services.enterprise_agent import ALLOWED_TOOLS, _infer_tool
from week08.services.incident_triage import score_severity


def test_high_risk_keywords():
    ev = _evaluate_risk("Delete production database")
    assert ev["requires_approval"] is True
    assert ev["risk"] == "high"


def test_low_risk_explicit():
    ev = _evaluate_risk("Generate weekly report", risk_level="low")
    assert ev["requires_approval"] is False


def test_medium_auto_approve():
    ev = _evaluate_risk("Send status update to Slack channel")
    assert ev["requires_approval"] is False
    assert ev["risk"] == "medium"


def test_execute_stub_shape():
    out = _execute_stub("do the thing", approval_id="APR-ABCDEF1234")
    assert out["status"] == "executed"
    assert out["action_id"].startswith("ACT-")


def test_validate_document_valid():
    from common.validation import validate_document

    ok, validated, errors = validate_document({
        "doc_type": "invoice",
        "confidence": 0.9,
        "reason": "invoice keywords",
    })
    assert ok
    assert validated["queue"] == "queue_invoices"
    assert not errors


def test_validate_document_invalid_type():
    from common.validation import validate_document

    ok, validated, errors = validate_document({
        "doc_type": "spam",
        "confidence": 0.9,
        "reason": "x",
    })
    assert not ok
    assert "invalid_doc_type" in errors


def test_severity_critical():
    info = score_severity(
        "P0 customer-facing outage and data breach",
        "security",
        {"route": "team_security", "valid": True},
    )
    assert info["severity"] == "critical"


def test_severity_needs_review():
    info = score_severity(
        "something odd",
        "general",
        {"route": "human_review", "low_confidence": True},
    )
    assert info["severity"] == "needs_review"


def test_severity_high_prod_signal():
    info = score_severity(
        "API 503 crash in production",
        "technical",
        {"route": "team_engineering", "valid": True},
    )
    assert info["severity"] == "high"


def test_infer_tool_incident():
    assert _infer_tool("API 503 outage alert") == "incident_triage"


def test_infer_tool_document():
    assert _infer_tool("Please classify this invoice PDF") == "doc_classify"


def test_allowed_tools_complete():
    assert {"incident_triage", "doc_classify", "approval_request", "summarize", "classify_route"} <= ALLOWED_TOOLS
