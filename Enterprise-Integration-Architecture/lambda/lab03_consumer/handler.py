"""Lab 3 consumer — idempotent; poison when amount==POISON or fail flag."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    for rec in event.get("Records", []):
        try:
            body = json.loads(rec["body"])
        except json.JSONDecodeError as exc:
            print(json.dumps({"level": "ERROR", "msg": "invalid_json", "messageId": rec.get("messageId")}))
            raise RuntimeError("invalid json") from exc
        if not isinstance(body, dict):
            raise RuntimeError("invalid payload")
        mid = rec["messageId"]
        cid = body.get("correlationId") or rec.get("attributes", {}).get("MessageDeduplicationId") or mid
        if body.get("fail") or body.get("amount") == "POISON":
            print(json.dumps({"level": "ERROR", "msg": "poison", "correlationId": cid, "messageId": mid}))
            raise RuntimeError("poison message")
        try:
            table.put_item(
                Item={
                    "pk": f"MSG#{mid}",
                    "paymentId": body.get("paymentId"),
                    "correlationId": cid,
                    "status": "POSTED",
                },
                ConditionExpression="attribute_not_exists(pk)",
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ConditionalCheckFailedException":
                raise
            print(json.dumps({"level": "INFO", "msg": "duplicate", "correlationId": cid, "messageId": mid}))
            continue
        print(json.dumps({"level": "INFO", "msg": "posted", "correlationId": cid, "messageId": mid}))
