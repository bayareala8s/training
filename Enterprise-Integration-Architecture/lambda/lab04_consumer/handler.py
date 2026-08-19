"""Lab 4 — SNS→SQS consumer. Unwraps the SNS notification envelope before projecting."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
PREFIX = os.environ.get("PROJECTION_PREFIX", "INV")


def unwrap_sqs_body(raw: Any) -> dict[str, Any]:
    body: Any = json.loads(raw) if isinstance(raw, str) else (raw or {})
    if isinstance(body, dict) and "Message" in body and (
        "TopicArn" in body or body.get("Type") == "Notification"
    ):
        inner = body["Message"]
        if isinstance(inner, str):
            try:
                parsed = json.loads(inner)
            except json.JSONDecodeError:
                return {"message": inner}
            return parsed if isinstance(parsed, dict) else {"message": parsed}
        return inner if isinstance(inner, dict) else {}
    return body if isinstance(body, dict) else {}


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    for rec in event.get("Records", []):
        body = unwrap_sqs_body(rec.get("body") or "{}")
        oid = body.get("orderId") or rec["messageId"]
        cid = body.get("correlationId") or rec["messageId"]
        table.put_item(
            Item={
                "pk": f"{PREFIX}#{oid}",
                "orderId": oid,
                "projection": PREFIX,
                "correlationId": cid,
            }
        )
        print(json.dumps({"level": "INFO", "msg": "projected", "projection": PREFIX, "orderId": oid, "correlationId": cid}))
