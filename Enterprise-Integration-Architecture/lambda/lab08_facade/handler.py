"""Lab 8 strangler façade — balances leave the ESB; settlement stays on the adapter."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3

ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    cid = (event.get("headers") or {}).get("x-correlation-id") or "lab08"
    customer_id = (event.get("pathParameters") or {}).get("id") or "demo"
    item = ddb.get_item(Key={"pk": f"BAL#{customer_id}"}).get("Item")
    if not item:
        item = {"pk": f"BAL#{customer_id}", "customerId": customer_id, "balance": "100.00", "source": "new-api"}
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json", "x-correlation-id": cid},
        "body": json.dumps(
            {
                "customerId": customer_id,
                "balance": item.get("balance", "100.00"),
                "channel": "strangler-api",
                "notViaEsb": True,
            },
            default=str,
        ),
    }
