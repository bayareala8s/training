"""Atlas Manufacturing — status APIs + HITL retry. Missing-supplier query is bounded."""

from __future__ import annotations

import json
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import boto3

ddb = boto3.resource("dynamodb")
suppliers = ddb.Table(os.environ["SUPPLIERS_TABLE"])
catalog = ddb.Table(os.environ["CATALOG_TABLE"])
approvals = ddb.Table(os.environ["APPROVAL_TABLE"])
EXPECTED = [s.strip() for s in os.environ.get("EXPECTED_SUPPLIERS", "ACME,BOLTCO,YIELD").split(",") if s.strip()]


def _body(event):
    raw = event.get("body") or "{}"
    return json.loads(raw) if isinstance(raw, str) else raw


def _ok(status, body, cid):
    body = {**body, "correlationId": cid}
    return {"statusCode": status, "headers": {"content-type": "application/json", "x-correlation-id": cid}, "body": json.dumps(body, default=str)}


def _today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    cid = {str(k).lower(): v for k, v in (event.get("headers") or {}).items()}.get("x-correlation-id") or str(uuid.uuid4())
    method = (event.get("requestContext") or {}).get("http", {}).get("method") or ""
    path = event.get("rawPath") or ""
    payload = _body(event)

    if method == "GET" and path.rstrip("/").endswith("/suppliers/missing"):
        day = payload.get("date") or _today()
        missing = []
        for name in EXPECTED:
            item = catalog.get_item(Key={"pk": f"ARRIVED#{name}#{day}"}).get("Item")
            if not item:
                missing.append(name)
        return _ok(200, {"date": day, "expected": EXPECTED, "missing": missing}, cid)

    if method == "GET" and "/shipments/" in path:
        sid = (event.get("pathParameters") or {}).get("id") or path.rstrip("/").split("/")[-1]
        item = suppliers.get_item(Key={"pk": f"SHIP#{sid}"}).get("Item")
        if not item:
            return _ok(404, {"code": "NOT_FOUND"}, cid)
        return _ok(200, {"shipment": item}, cid)

    if method == "POST" and path.rstrip("/").endswith("/tools"):
        tool = payload.get("tool")
        if tool == "ListMissingSuppliers":
            day = _today()
            missing = [n for n in EXPECTED if not catalog.get_item(Key={"pk": f"ARRIVED#{n}#{day}"}).get("Item")]
            return _ok(200, {"tool": tool, "result": {"missing": missing, "date": day}}, cid)
        if tool == "GetShipmentStatus":
            sid = payload.get("shipmentId") or "92841"
            item = suppliers.get_item(Key={"pk": f"SHIP#{sid}"}).get("Item")
            return _ok(200, {"tool": tool, "result": item}, cid)
        if tool == "RequestRetry":
            aid = str(uuid.uuid4())
            approvals.put_item(Item={"pk": aid, "status": "PENDING", "supplier": payload.get("supplier"), "ts": int(time.time())})
            return _ok(200, {"tool": tool, "approvalId": aid, "status": "PENDING_APPROVAL"}, cid)
        return _ok(400, {"code": "UNKNOWN_TOOL", "tool": tool}, cid)

    if method == "POST" and path.rstrip("/").endswith("/approve"):
        aid = payload.get("approvalId")
        item = approvals.get_item(Key={"pk": aid}).get("Item")
        if not item or item.get("status") != "PENDING":
            return _ok(409, {"code": "NOT_PENDING"}, cid)
        approvals.update_item(
            Key={"pk": aid},
            UpdateExpression="SET #s = :s, decidedAt = :t",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": "APPROVED", ":t": int(time.time())},
        )
        supplier = item.get("supplier")
        catalog.put_item(Item={"pk": f"RETRY#{supplier}", "status": "REQUESTED", "approvalId": aid})
        return _ok(200, {"approved": aid, "supplier": supplier, "status": "RETRY_REQUESTED", "audit": "SupplierRetryRequested"}, cid)

    return _ok(404, {"code": "NOT_FOUND"}, cid)
