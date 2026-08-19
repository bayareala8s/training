"""Lab 11 chaos consumer — same contract as Lab 3 with faster visibility for drills."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    for rec in event.get("Records", []):
        try:
            body = json.loads(rec["body"])
        except json.JSONDecodeError as exc:
            print(json.dumps({"level": "ERROR", "msg": "invalid_json", "messageId": rec.get("messageId")}))
            raise RuntimeError("invalid json") from exc
        mid = rec["messageId"]
        cid = (body or {}).get("correlationId") if isinstance(body, dict) else mid
        if not isinstance(body, dict) or body.get("fail") or body.get("amount") == "POISON":
            print(json.dumps({"level": "ERROR", "msg": "poison", "correlationId": cid, "messageId": mid}))
            raise RuntimeError("poison message")
        try:
            table.put_item(
                Item={"pk": f"MSG#{mid}", "paymentId": body.get("paymentId"), "correlationId": cid, "status": "POSTED"},
                ConditionExpression="attribute_not_exists(pk)",
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ConditionalCheckFailedException":
                raise
        print(json.dumps({"level": "INFO", "msg": "posted", "correlationId": cid, "messageId": mid}))
