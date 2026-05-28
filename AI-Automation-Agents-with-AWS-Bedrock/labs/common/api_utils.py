"""API Gateway Lambda proxy helpers."""

from __future__ import annotations

import json
import uuid
from typing import Any


def api_response(status: int, body: dict[str, Any], correlation_id: str | None = None) -> dict[str, Any]:
    cid = correlation_id or str(uuid.uuid4())
    payload = {"correlation_id": cid, **body}
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "X-Correlation-Id": cid,
        },
        "body": json.dumps(payload),
    }


def parse_body(event: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    """Returns (body_dict, error_message)."""
    raw = event.get("body")
    if raw is None:
        return {}, "missing_body"
    if event.get("isBase64Encoded"):
        import base64

        raw = base64.b64decode(raw).decode("utf-8")
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except json.JSONDecodeError:
        return {}, "invalid_json"
    if not isinstance(data, dict):
        return {}, "body_must_be_object"
    return data, None


def get_correlation_id(event: dict[str, Any], body: dict[str, Any]) -> str:
    headers = event.get("headers") or {}
    # API Gateway may lowercase header names
    for key, val in headers.items():
        if key.lower() == "x-correlation-id" and val:
            return str(val)
    if body.get("correlation_id"):
        return str(body["correlation_id"])
    return str(uuid.uuid4())
