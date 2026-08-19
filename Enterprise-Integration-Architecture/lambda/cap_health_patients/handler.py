"""CareMesh — authorized patient API. This is the only data-plane reader."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3

ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def _headers(event):
    return {str(k).lower(): v for k, v in (event.get("headers") or {}).items()}


def _ok(status, body, cid):
    return {"statusCode": status, "headers": {"content-type": "application/json", "x-correlation-id": cid}, "body": json.dumps(body, default=str)}


def _view(item: dict, role: str) -> dict:
    base = {"patientId": item.get("patientId"), "name": item.get("name")}
    if role == "billing":
        return {**base, "accountStatus": item.get("accountStatus")}
    if role in {"clinician", "patient"}:
        return {**base, "status": item.get("status")}
    return base


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    h = _headers(event)
    cid = h.get("x-correlation-id") or "health"
    role = (h.get("x-actor-role") or "").lower()
    actor = h.get("x-actor-id") or ""
    pid = (event.get("pathParameters") or {}).get("id") or (event.get("rawPath") or "").rstrip("/").split("/")[-1]
    if role not in {"clinician", "patient", "billing"}:
        return _ok(401, {"code": "UNAUTHENTICATED", "message": "x-actor-role required"}, cid)
    if role == "patient" and actor != pid:
        return _ok(403, {"code": "FORBIDDEN", "message": "patients may only read self"}, cid)
    item = ddb.get_item(Key={"pk": f"PT#{pid}"}).get("Item")
    if not item:
        return _ok(404, {"code": "NOT_FOUND"}, cid)
    return _ok(200, {"patient": _view(item, role), "minimized": True}, cid)
