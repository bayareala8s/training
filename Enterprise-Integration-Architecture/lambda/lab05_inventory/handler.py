"""Lab 5 inventory — PaymentAuthorized → InventoryReserved."""

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
    ddb.put_item(Item={"pk": f"INV#{eid}", "orderId": oid, "correlationId": cid, "status": "InventoryReserved"})
    eb.put_events(
        Entries=[
            {
                "EventBusName": os.environ["BUS_NAME"],
                "Source": "eia.inventory",
                "DetailType": "InventoryReserved",
                "Detail": json.dumps({"orderId": oid, "correlationId": cid}),
            }
        ]
    )
    print(json.dumps({"level": "INFO", "msg": "inventory_reserved", "orderId": oid, "correlationId": cid}))
