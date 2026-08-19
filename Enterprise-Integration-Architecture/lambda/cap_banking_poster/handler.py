"""Northbridge Bank — async ledger posting consumer (command/queue). Idempotent on paymentId."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

table = boto3.resource("dynamodb").Table(os.environ["PAYMENTS_TABLE"])


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        pid = body["paymentId"]
        cid = body.get("correlationId")
        if body.get("amount") == "POISON":
            raise RuntimeError("poison payment")
        try:
            table.update_item(
                Key={"pk": f"PAY#{pid}"},
                UpdateExpression="SET #s = :s",
                ConditionExpression="attribute_exists(pk)",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":s": "POSTED"},
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                table.put_item(Item={"pk": f"PAY#{pid}", "paymentId": pid, "status": "POSTED", "correlationId": cid})
            else:
                raise
        print(json.dumps({"level": "INFO", "msg": "posted", "paymentId": pid, "correlationId": cid}))
