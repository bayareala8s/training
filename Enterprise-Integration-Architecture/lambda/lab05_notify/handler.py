"""Lab 5 notify — InventoryReserved → OrderCompleted projection."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3

ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def _detail(event: dict[str, Any]) -> dict[str, Any]:
    d = event.get("detail") or {}
    if isinstance(d, str):
        d = json.loads(d) if d else {}
    return d if isinstance(d, dict) else {}


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    d = _detail(event)
    oid = d.get("orderId")
    cid = d.get("correlationId")
    ddb.put_item(
        Item={
            "pk": f"DONE#{oid}",
            "orderId": oid,
            "status": "OrderCompleted",
            "correlationId": cid,
        }
    )
    print(json.dumps({"level": "INFO", "msg": "completed", "orderId": oid, "correlationId": cid}))
