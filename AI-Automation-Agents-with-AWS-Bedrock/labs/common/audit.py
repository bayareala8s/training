"""Audit event writer (metadata only — no raw prompts in logs by default)."""

from __future__ import annotations

import os
import time
from typing import Any

import boto3

from common.config import AUDIT_TABLE_NAME


def write_audit_event(
    *,
    correlation_id: str,
    event_type: str,
    model_id: str | None = None,
    input_size: int = 0,
    output_size: int = 0,
    validation_status: str = "unknown",
    route_or_action: str | None = None,
    latency_ms: int | None = None,
    success: bool = True,
    extra: dict[str, Any] | None = None,
) -> None:
    table_name = AUDIT_TABLE_NAME or os.environ.get("AUDIT_TABLE_NAME")
    if not table_name:
        return

    item: dict[str, Any] = {
        "pk": f"CORR#{correlation_id}",
        "sk": f"TS#{int(time.time() * 1000)}#{event_type}",
        "correlation_id": correlation_id,
        "event_type": event_type,
        "timestamp": int(time.time()),
        "validation_status": validation_status,
        "success": success,
    }
    if model_id:
        item["model_id"] = model_id
    if input_size:
        item["input_size"] = input_size
    if output_size:
        item["output_size"] = output_size
    if route_or_action:
        item["route_or_action"] = route_or_action
    if latency_ms is not None:
        item["latency_ms"] = latency_ms
    if extra:
        item["metadata"] = extra

    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    table = boto3.resource("dynamodb", region_name=region).Table(table_name)
    table.put_item(Item=item)


def query_by_correlation(correlation_id: str) -> list[dict[str, Any]]:
    table_name = AUDIT_TABLE_NAME or os.environ.get("AUDIT_TABLE_NAME")
    if not table_name:
        return []

    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    table = boto3.resource("dynamodb", region_name=region).Table(table_name)
    resp = table.query(
        KeyConditionExpression="pk = :pk",
        ExpressionAttributeValues={":pk": f"CORR#{correlation_id}"},
    )
    return resp.get("Items", [])
