"""Lab 7 — GET upload job status."""

from __future__ import annotations

import json
import os
from typing import Any

import boto3

ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    job = (event.get("pathParameters") or {}).get("id") or (event.get("rawPath") or "").rstrip("/").split("/")[-1]
    item = ddb.get_item(Key={"pk": job}).get("Item")
    if not item:
        return {"statusCode": 404, "headers": {"content-type": "application/json"}, "body": json.dumps({"code": "NOT_FOUND", "jobId": job})}
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"jobId": job, "status": item.get("status"), "checksum": item.get("checksum"), "key": item.get("key")}, default=str),
    }
