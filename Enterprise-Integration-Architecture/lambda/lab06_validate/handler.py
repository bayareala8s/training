"""Lab 6 — inbound file validation, duplicate detection, quarantine."""

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
DEST = os.environ.get("DEST_PREFIX", "accepted/")
Q = os.environ.get("QUARANTINE_PREFIX", "quarantine/")


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        for rec2 in body.get("Records", [body] if "s3" in body else []):
            if "s3" not in rec2:
                continue
            bkt = rec2["s3"]["bucket"]["name"]
            key = urllib.parse.unquote_plus(rec2["s3"]["object"]["key"])
            if not key.startswith("inbound/"):
                continue
            obj = s3.get_object(Bucket=bkt, Key=key)
            data = obj["Body"].read()
            sha = hashlib.sha256(data).hexdigest()
            cid = (obj.get("Metadata") or {}).get("correlationid") or sha[:16]
            existing = ddb.get_item(Key={"pk": f"HASH#{sha}"}).get("Item")
            duplicate = bool(existing and existing.get("status") == "ACCEPTED")
            valid = (not duplicate) and key.lower().endswith(".csv") and b"partner" in data[:400].lower()
            base = key.rsplit("/", 1)[-1]
            if duplicate:
                status = "DUPLICATE"
                dest = f"{Q}{sha[:12]}-{base}"
            elif not valid:
                status = "QUARANTINED"
                dest = f"{Q}{sha[:12]}-{base}"
            else:
                status = "ACCEPTED"
                dest = f"{DEST}{sha[:12]}-{base}"
                try:
                    ddb.put_item(
                        Item={"pk": f"HASH#{sha}", "key": key, "status": "ACCEPTED", "correlationId": cid},
                        ConditionExpression="attribute_not_exists(pk)",
                    )
                except ClientError as exc:
                    if exc.response["Error"]["Code"] != "ConditionalCheckFailedException":
                        raise
                    status = "DUPLICATE"
                    dest = f"{Q}{sha[:12]}-{base}"
            s3.copy_object(Bucket=bkt, CopySource={"Bucket": bkt, "Key": key}, Key=dest)
            ddb.put_item(
                Item={
                    "pk": f"FILE#{key}",
                    "checksum": sha,
                    "status": status,
                    "correlationId": cid,
                    "dest": dest,
                }
            )
            print(json.dumps({"level": "INFO", "msg": "file", "status": status, "key": key, "correlationId": cid}))
