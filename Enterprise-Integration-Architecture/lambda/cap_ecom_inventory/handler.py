"""Harbor Retail — inventory step. Fails when failInventory is true (payment already ok)."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3

eb = boto3.client("events")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
BUS = os.environ["BUS_NAME"]


def _detail(event):
    d = event.get("detail") or {}
    return json.loads(d) if isinstance(d, str) else d


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    d = _detail(event)
    oid = d["orderId"]
    cid = d.get("correlationId")
    fail = bool(d.get("failInventory")) or d.get("amount") == 13.13
    if fail:
        ddb.update_item(
            Key={"pk": f"ORDER#{oid}"},
            UpdateExpression="SET inventoryStatus = :s",
            ExpressionAttributeValues={":s": "FAILED"},
        )
        eb.put_events(
            Entries=[
                {
                    "EventBusName": BUS,
                    "Source": "eia.inventory",
                    "DetailType": "InventoryFailed",
                    "Detail": json.dumps({"orderId": oid, "correlationId": cid, "reason": "SKU_UNAVAILABLE"}),
                }
            ]
        )
        print(json.dumps({"level": "WARN", "msg": "inventory_failed", "orderId": oid, "correlationId": cid}))
        return
    ddb.update_item(
        Key={"pk": f"ORDER#{oid}"},
        UpdateExpression="SET inventoryStatus = :s",
        ExpressionAttributeValues={":s": "RESERVED"},
    )
    eb.put_events(
        Entries=[
            {
                "EventBusName": BUS,
                "Source": "eia.inventory",
                "DetailType": "InventoryReserved",
                "Detail": json.dumps({"orderId": oid, "correlationId": cid}),
            }
        ]
    )
    print(json.dumps({"level": "INFO", "msg": "inventory_reserved", "orderId": oid, "correlationId": cid}))
