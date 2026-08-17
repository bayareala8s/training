"""
Option C — Multi-step Approval Workflow.

Flow: evaluate risk → pending approval OR auto-execute → decide → execute stub → notify → audit.
"""

from __future__ import annotations

import os
import re
import time
import uuid

import boto3

from common.audit import write_audit_event
from common.config import CAPSTONE_APPROVALS_TABLE
from week08.services.persist import notify_stub

HIGH_RISK_PATTERN = re.compile(
    r"\b(delete|drop|production|root|credential|wipe|shutdown|revoke|terminate)\b",
    re.I,
)


def _table():
    name = CAPSTONE_APPROVALS_TABLE or os.environ.get("CAPSTONE_APPROVALS_TABLE")
    if not name:
        return None
    return boto3.resource("dynamodb").Table(name)


def _evaluate_risk(action_text: str, risk_level: str = "auto") -> dict:
    if risk_level in {"high", "critical"}:
        return {"risk": "high", "requires_approval": True, "reason": "explicit_high_risk"}
    if risk_level == "low":
        return {"risk": "low", "requires_approval": False, "reason": "explicit_low_risk"}
    if HIGH_RISK_PATTERN.search(action_text):
        return {"risk": "high", "requires_approval": True, "reason": "keyword_match"}
    return {"risk": "medium", "requires_approval": False, "reason": "default_auto_approve"}


def _execute_stub(action_text: str, *, approval_id: str) -> dict:
    return {
        "status": "executed",
        "action_id": f"ACT-{approval_id[-8:]}",
        "message": "Action executed (stub) — replace with real change management API",
        "action_preview": action_text[:120],
    }


def request_approval(
    action_text: str,
    *,
    correlation_id: str,
    risk_level: str = "auto",
    requester_id: str = "student",
) -> dict:
    """Submit an action for approval evaluation."""
    evaluation = _evaluate_risk(action_text, risk_level)
    approval_id = f"APR-{uuid.uuid4().hex[:10].upper()}"
    now = int(time.time())

    status = "pending_approval" if evaluation["requires_approval"] else "auto_approved"
    record = {
        "approval_id": approval_id,
        "correlation_id": correlation_id,
        "status": status,
        "action_preview": action_text[:200],
        "action_size": len(action_text),
        "risk": evaluation["risk"],
        "requester_id": requester_id,
        "created_at": now,
        "updated_at": now,
    }

    output = None
    notification = None
    if not evaluation["requires_approval"]:
        output = _execute_stub(action_text, approval_id=approval_id)
        record["status"] = "executed"
        status = "executed"
    else:
        notification = notify_stub(
            "approval_pending",
            f"Approval {approval_id} pending for requester={requester_id}: {action_text[:120]}",
            correlation_id=correlation_id,
        )

    tbl = _table()
    if tbl:
        tbl.put_item(Item=record)

    write_audit_event(
        correlation_id=correlation_id,
        event_type="capstone_approval_request",
        model_id="rules-engine",
        input_size=len(action_text),
        output_size=0,
        validation_status=status,
        route_or_action=evaluation["risk"],
        latency_ms=0,
        extra={
            "approval_id": approval_id,
            "requires_approval": evaluation["requires_approval"],
            "notify": (notification or {}).get("delivery"),
        },
    )

    return {
        "correlation_id": correlation_id,
        "capstone_option": "approval_workflow",
        "approval_id": approval_id,
        "evaluation": evaluation,
        "status": status,
        "output": output,
        "notification": notification,
        "next_step": (
            "POST /capstone/approval/decide with approval_id"
            if status == "pending_approval"
            else None
        ),
    }


def decide_approval(
    approval_id: str,
    decision: str,
    *,
    correlation_id: str,
    approver_id: str = "approver",
) -> dict:
    """Approve or deny a pending approval request."""
    tbl = _table()
    if not tbl:
        return {"error": "approvals_table_not_configured", "correlation_id": correlation_id}

    resp = tbl.get_item(Key={"approval_id": approval_id})
    item = resp.get("Item")
    if not item:
        return {"error": "approval_not_found", "approval_id": approval_id, "correlation_id": correlation_id}

    if item.get("status") != "pending_approval":
        return {
            "error": "invalid_state",
            "approval_id": approval_id,
            "current_status": item.get("status"),
            "correlation_id": correlation_id,
        }

    decision = decision.lower()
    if decision not in {"approve", "deny"}:
        return {"error": "invalid_decision", "correlation_id": correlation_id}

    now = int(time.time())
    new_status = "approved" if decision == "approve" else "denied"
    output = None
    if decision == "approve":
        output = _execute_stub(item.get("action_preview", ""), approval_id=approval_id)
        new_status = "executed"

    tbl.update_item(
        Key={"approval_id": approval_id},
        UpdateExpression="SET #s = :s, approver_id = :a, updated_at = :t",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": new_status, ":a": approver_id, ":t": now},
    )

    notification = notify_stub(
        "approval_decided",
        f"Approval {approval_id} → {new_status} by {approver_id}",
        correlation_id=correlation_id,
    )

    write_audit_event(
        correlation_id=correlation_id,
        event_type="capstone_approval_decide",
        model_id="rules-engine",
        input_size=0,
        output_size=0,
        validation_status=new_status,
        route_or_action=decision,
        latency_ms=0,
        extra={
            "approval_id": approval_id,
            "approver_id": approver_id,
            "notify": notification.get("delivery"),
        },
    )

    return {
        "correlation_id": correlation_id,
        "capstone_option": "approval_workflow",
        "approval_id": approval_id,
        "decision": decision,
        "status": new_status,
        "output": output,
        "notification": notification,
    }
