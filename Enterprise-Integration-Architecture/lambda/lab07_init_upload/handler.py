"""Lab 7 — init a claim-check upload (presigned PUT)."""

from __future__ import annotations

import json
import os
import uuid
from typing import Any

import boto3

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
BUCKET = os.environ["BUCKET"]


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    headers = {str(k).lower(): v for k, v in (event.get("headers") or {}).items()}
    cid = headers.get("x-correlation-id") or str(uuid.uuid4())
    job = str(uuid.uuid4())
    key = f"inbound/{job}.bin"
    url = s3.generate_presigned_url("put_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=900)
    ddb.put_item(Item={"pk": job, "status": "PENDING_UPLOAD", "key": key, "correlationId": cid})
    return {
        "statusCode": 202,
        "headers": {"content-type": "application/json", "x-correlation-id": cid},
        "body": json.dumps({"jobId": job, "uploadUrl": url, "key": key, "correlationId": cid}),
    }
