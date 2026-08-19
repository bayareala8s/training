"""Lab 7 — process inbound object and mark the job COMPLETED."""

from __future__ import annotations

import hashlib
import json
import os
import urllib.parse
from typing import Any

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    for rec in event.get("Records", []):
        bkt = rec["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(rec["s3"]["object"]["key"])
        job = key.split("/")[-1].replace(".bin", "")
        data = s3.get_object(Bucket=bkt, Key=key)["Body"].read()
        sha = hashlib.sha256(data).hexdigest()
        try:
            ddb.update_item(
                Key={"pk": job},
                UpdateExpression="SET #s = :s, checksum = :c, #k = :k",
                ExpressionAttributeNames={"#s": "status", "#k": "key"},
                ExpressionAttributeValues={":s": "COMPLETED", ":c": sha, ":k": key},
            )
        except ClientError:
            ddb.put_item(Item={"pk": job, "status": "COMPLETED", "checksum": sha, "key": key})
        print(json.dumps({"level": "INFO", "msg": "processed", "jobId": job, "bytes": len(data)}))
