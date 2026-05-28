"""Lab 4 — Persist workflow result to DynamoDB."""

from __future__ import annotations

import os
import time
from decimal import Decimal

import boto3


def _to_dynamo(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    if isinstance(obj, dict):
        return {k: _to_dynamo(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_dynamo(v) for v in obj]
    return obj


def handler(event, context):
    table_name = os.environ.get("RESULTS_TABLE_NAME")
    correlation_id = event.get("correlation_id", "unknown")
    validated = event.get("validated", {})
    status = "completed" if event.get("valid") else "fallback"

    item = _to_dynamo({
        "correlation_id": correlation_id,
        "status": status,
        "label": validated.get("label") or validated.get("route", "unknown"),
        "updated_at": int(time.time()),
        "payload": validated,
    })

    if table_name:
        boto3.resource("dynamodb").Table(table_name).put_item(Item=item)

    return {
        "correlation_id": correlation_id,
        "status": status,
        "action": "ticket_stub_created",
        "stored": bool(table_name),
    }
