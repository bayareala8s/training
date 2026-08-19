"""Harbor Retail — order API (acceptance) + customer-service tools (status APIs only)."""

from __future__ import annotations

import json
import os
import uuid
from decimal import Decimal
from typing import Any

import boto3

ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
eb = boto3.client("events")
BUS = os.environ["BUS_NAME"]


def _body(event):
    raw = event.get("body") or "{}"
    return json.loads(raw) if isinstance(raw, str) else raw


def _ok(status, body, cid):
    body = {**body, "correlationId": cid}
    return {"statusCode": status, "headers": {"content-type": "application/json", "x-correlation-id": cid}, "body": json.dumps(body, default=str)}


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    cid = {str(k).lower(): v for k, v in (event.get("headers") or {}).items()}.get("x-correlation-id") or str(uuid.uuid4())
    method = (event.get("requestContext") or {}).get("http", {}).get("method") or ""
    path = event.get("rawPath") or ""
    payload = _body(event)

    if method == "POST" and path.rstrip("/").endswith("/orders"):
        oid = str(uuid.uuid4())
        fail_inv = bool(payload.get("failInventory")) or payload.get("amount") == 13.13
        item = {
            "pk": f"ORDER#{oid}",
            "orderId": oid,
            "status": "ACCEPTED",
            "amount": Decimal(str(payload.get("amount", 20))),
            "sku": payload.get("sku", "SKU-1"),
            "failInventory": fail_inv,
            "correlationId": cid,
        }
        ddb.put_item(Item=item)
        eb.put_events(
            Entries=[
                {
                    "EventBusName": BUS,
                    "Source": "eia.orders",
                    "DetailType": "OrderCreated",
                    "Detail": json.dumps({"orderId": oid, "correlationId": cid, "amount": float(item["amount"]), "failInventory": fail_inv}),
                }
            ]
        )
        return _ok(202, {"code": "ACCEPTED", "orderId": oid, "status": "ACCEPTED"}, cid)

    if method == "GET" and "/orders/" in path:
        oid = (event.get("pathParameters") or {}).get("id") or path.rstrip("/").split("/")[-1]
        item = ddb.get_item(Key={"pk": f"ORDER#{oid}"}).get("Item")
        if not item:
            return _ok(404, {"code": "NOT_FOUND"}, cid)
        return _ok(200, {"order": item}, cid)

    if method == "POST" and path.rstrip("/").endswith("/tools"):
        tool = payload.get("tool")
        oid = payload.get("orderId")
        if tool != "GetOrderStatus" or not oid:
            return _ok(400, {"code": "UNKNOWN_TOOL"}, cid)
        item = ddb.get_item(Key={"pk": f"ORDER#{oid}"}).get("Item")
        return _ok(200, {"tool": tool, "result": item}, cid)

    return _ok(404, {"code": "NOT_FOUND"}, cid)
