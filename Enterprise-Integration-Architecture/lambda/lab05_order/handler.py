"""Lab 5 — emit OrderCreated. Works as a direct invoke or HTTP API POST /orders."""

from __future__ import annotations

import json
import os
import uuid
from typing import Any

import boto3

eb = boto3.client("events")


def lambda_handler(event: dict[str, Any], _ctx: Any) -> Any:
    payload = event or {}
    if isinstance(payload.get("body"), str):
        payload = json.loads(payload["body"] or "{}")
    cid = payload.get("correlationId") or str(uuid.uuid4())
    oid = payload.get("orderId") or str(uuid.uuid4())
    amount = payload.get("amount", 20)
    eb.put_events(
        Entries=[
            {
                "EventBusName": os.environ["BUS_NAME"],
                "Source": "eia.orders",
                "DetailType": "OrderCreated",
                "Detail": json.dumps({"orderId": oid, "correlationId": cid, "amount": amount}),
            }
        ]
    )
    result = {"orderId": oid, "correlationId": cid, "status": "OrderCreated"}
    if event.get("requestContext"):
        return {
            "statusCode": 202,
            "headers": {"content-type": "application/json", "x-correlation-id": cid},
            "body": json.dumps(result),
        }
    return result
