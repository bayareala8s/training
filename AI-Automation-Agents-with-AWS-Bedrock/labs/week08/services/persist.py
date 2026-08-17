"""Shared DynamoDB helpers for Week 8 capstone options."""

from __future__ import annotations

import os
import time
from decimal import Decimal
from typing import Any

import boto3


def _to_dynamo(obj: Any) -> Any:
    if isinstance(obj, float):
        return Decimal(str(obj))
    if isinstance(obj, dict):
        return {k: _to_dynamo(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_dynamo(v) for v in obj]
    return obj


def persist_result(
    correlation_id: str,
    *,
    status: str,
    capstone_option: str,
    payload: dict[str, Any],
) -> bool:
    """Write a capstone result row. Returns False if RESULTS_TABLE_NAME unset."""
    table_name = os.environ.get("RESULTS_TABLE_NAME")
    if not table_name:
        return False
    item = _to_dynamo({
        "correlation_id": correlation_id,
        "status": status,
        "capstone_option": capstone_option,
        "updated_at": int(time.time()),
        "payload": payload,
    })
    boto3.resource("dynamodb").Table(table_name).put_item(Item=item)
    return True


def notify_stub(channel: str, message: str, *, correlation_id: str) -> dict[str, str]:
    """
    Portfolio stretch hook for SNS/PagerDuty.

    Does not call AWS unless CAPSTONE_NOTIFY_TOPIC_ARN is set.
    Always returns a structured stub suitable for demos and audit extras.
    """
    topic = os.environ.get("CAPSTONE_NOTIFY_TOPIC_ARN", "")
    record = {
        "channel": channel,
        "message": message[:500],
        "correlation_id": correlation_id,
        "delivery": "skipped_no_topic" if not topic else "sns_attempted",
    }
    if topic:
        try:
            boto3.client("sns").publish(
                TopicArn=topic,
                Subject=f"Capstone {channel}",
                Message=message[:2000],
            )
            record["delivery"] = "sns_published"
        except Exception as exc:  # noqa: BLE001 — demo-friendly; never fail triage on notify
            record["delivery"] = f"sns_failed:{type(exc).__name__}"
    return record
