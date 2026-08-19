"""Harbor Retail — saga completion or compensating transaction."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3

ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def _detail(event):
    d = event.get("detail") or {}
    return json.loads(d) if isinstance(d, str) else d


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    d = _detail(event)
    oid = d["orderId"]
    cid = d.get("correlationId")
    dtype = event.get("detail-type") or event.get("detailType")
    if dtype == "InventoryFailed":
        ddb.update_item(
            Key={"pk": f"ORDER#{oid}"},
            UpdateExpression="SET #s = :s, paymentStatus = :p, compensation = :c",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": "COMPENSATED", ":p": "VOIDED", ":c": "PaymentVoided"},
        )
        print(json.dumps({"level": "INFO", "msg": "compensated", "orderId": oid, "correlationId": cid}))
        return
    ddb.update_item(
        Key={"pk": f"ORDER#{oid}"},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "COMPLETED"},
    )
    print(json.dumps({"level": "INFO", "msg": "completed", "orderId": oid, "correlationId": cid}))
