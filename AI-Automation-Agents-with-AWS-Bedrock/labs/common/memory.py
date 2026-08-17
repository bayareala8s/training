"""Session memory store (summaries only — no secrets)."""

from __future__ import annotations

import os
import time
from typing import Any

import boto3

from common.config import MEMORY_TABLE_NAME

TTL_SECONDS = 7 * 24 * 3600  # 7 days


def get_memory(session_id: str) -> dict[str, Any] | None:
    table_name = MEMORY_TABLE_NAME or os.environ.get("MEMORY_TABLE_NAME")
    if not table_name:
        return None

    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    table = boto3.resource("dynamodb", region_name=region).Table(table_name)
    resp = table.get_item(Key={"session_id": session_id})
    return resp.get("Item")


def put_memory(
    session_id: str,
    *,
    context_summary: str,
    last_route: str | None = None,
    last_action: str | None = None,
) -> None:
    table_name = MEMORY_TABLE_NAME or os.environ.get("MEMORY_TABLE_NAME")
    if not table_name:
        return

    # Never store full user payloads — summary only, bounded length
    summary = (context_summary or "")[:500]
    now = int(time.time())
    item = {
        "session_id": session_id,
        "context_summary": summary,
        "updated_at": now,
        "ttl": now + TTL_SECONDS,
    }
    if last_route:
        item["last_route"] = last_route
    if last_action:
        item["last_action"] = last_action

    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    table = boto3.resource("dynamodb", region_name=region).Table(table_name)
    table.put_item(Item=item)
