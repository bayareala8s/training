"""Lab 5 payment — OrderCreated → PaymentAuthorized."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3

eb = boto3.client("events")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def _detail(event: dict[str, Any]) -> dict[str, Any]:
    d = event.get("detail") or {}
    if isinstance(d, str):
        d = json.loads(d) if d else {}
    return d if isinstance(d, dict) else {}


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    d = _detail(event)
    eid = event.get("id") or d.get("orderId")
    oid = d.get("orderId")
    cid = d.get("correlationId")
    ddb.put_item(Item={"pk": f"PAY#{eid}", "orderId": oid, "correlationId": cid, "status": "PaymentAuthorized"})
    eb.put_events(
        Entries=[
            {
                "EventBusName": os.environ["BUS_NAME"],
                "Source": "eia.payments",
                "DetailType": "PaymentAuthorized",
                "Detail": json.dumps({"orderId": oid, "correlationId": cid, "eventId": eid}),
            }
        ]
    )
    print(json.dumps({"level": "INFO", "msg": "payment_authorized", "orderId": oid, "correlationId": cid}))
