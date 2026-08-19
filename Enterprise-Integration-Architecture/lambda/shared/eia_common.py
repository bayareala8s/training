"""Shared helpers for BayLearn EIA lab and capstone Lambdas."""

from __future__ import annotations

import base64
import json
import os
import uuid
from typing import Any


def correlation_id(event: dict[str, Any]) -> str:
    headers = event.get("headers") or {}
    lowered = {str(k).lower(): v for k, v in headers.items()}
    detail = event_detail(event)
    return (
        lowered.get("x-correlation-id")
        or detail.get("correlationId")
        or str(uuid.uuid4())
    )


def response(status: int, body: dict[str, Any], correlation: str) -> dict[str, Any]:
    body = {**body, "correlationId": correlation}
    return {
        "statusCode": status,
        "headers": {
            "content-type": "application/json",
            "x-correlation-id": correlation,
        },
        "body": json.dumps(body, default=str),
    }


def log(level: str, msg: str, **fields: Any) -> None:
    rec = {"level": level, "msg": msg, **fields}
    print(json.dumps(rec, default=str))


def table_name(env: str = "TABLE_NAME") -> str:
    name = os.environ.get(env)
    if not name:
        raise RuntimeError(f"{env} is not set")
    return name


def unwrap_sqs_body(raw: Any) -> dict[str, Any]:
    """Parse an SQS body, including SNS→SQS notification envelopes and S3 event wrappers."""
    body: Any = raw
    if isinstance(raw, str):
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            return {"_raw": raw}
    if not isinstance(body, dict):
        return {}
    if "Message" in body and ("TopicArn" in body or body.get("Type") == "Notification"):
        inner = body["Message"]
        if isinstance(inner, str):
            try:
                parsed = json.loads(inner) if inner else {}
            except json.JSONDecodeError:
                return {"message": inner}
            return parsed if isinstance(parsed, dict) else {"message": parsed}
        return inner if isinstance(inner, dict) else {}
    return body


def event_detail(event: dict[str, Any]) -> dict[str, Any]:
    """EventBridge `detail` may be a dict (Lambda) or a JSON string (other transports)."""
    d = event.get("detail")
    if d is None:
        return {}
    if isinstance(d, str):
        try:
            parsed = json.loads(d) if d else {}
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return d if isinstance(d, dict) else {}


def parse_http_body(event: dict[str, Any]) -> dict[str, Any]:
    raw = event.get("body")
    if raw in (None, ""):
        return {}
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8")
    if isinstance(raw, str):
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    return raw if isinstance(raw, dict) else {}


def path_param(event: dict[str, Any], name: str) -> str:
    params = event.get("pathParameters") or {}
    if params.get(name):
        return str(params[name])
    path = event.get("rawPath") or event.get("path") or ""
    return path.rstrip("/").split("/")[-1]


def http_method(event: dict[str, Any]) -> str:
    return (
        (event.get("requestContext") or {}).get("http", {}).get("method")
        or event.get("httpMethod")
        or ""
    )


def raw_path(event: dict[str, Any]) -> str:
    return event.get("rawPath") or event.get("path") or ""
