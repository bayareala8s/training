"""Harbor Retail — payment step of the choreography."""

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
    ddb.update_item(
        Key={"pk": f"ORDER#{oid}"},
        UpdateExpression="SET paymentStatus = :p",
        ExpressionAttributeValues={":p": "AUTHORIZED"},
    )
    eb.put_events(
        Entries=[
            {
                "EventBusName": BUS,
                "Source": "eia.payments",
                "DetailType": "PaymentAuthorized",
                "Detail": json.dumps({"orderId": oid, "correlationId": cid, "failInventory": d.get("failInventory", False), "amount": d.get("amount")}),
            }
        ]
    )
    print(json.dumps({"level": "INFO", "msg": "payment_authorized", "orderId": oid, "correlationId": cid}))
