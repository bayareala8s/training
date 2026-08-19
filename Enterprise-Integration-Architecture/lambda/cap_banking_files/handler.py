"""Northbridge Bank — inbound file catalog (duplicate/quarantine)."""

from __future__ import annotations

import hashlib
import json
import os
import urllib.parse
from typing import Any

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb").Table(os.environ["CATALOG_TABLE"])


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        for rec2 in body.get("Records", []):
            bkt = rec2["s3"]["bucket"]["name"]
            key = urllib.parse.unquote_plus(rec2["s3"]["object"]["key"])
            data = s3.get_object(Bucket=bkt, Key=key)["Body"].read()
            sha = hashlib.sha256(data).hexdigest()
            existing = ddb.get_item(Key={"pk": f"HASH#{sha}"}).get("Item")
            duplicate = bool(existing)
            valid = key.lower().endswith(".csv") and b"partner" in data[:400].lower()
            status = "DUPLICATE" if duplicate else ("ACCEPTED" if valid else "QUARANTINED")
            if status == "ACCEPTED":
                try:
                    ddb.put_item(Item={"pk": f"HASH#{sha}", "key": key, "status": "ACCEPTED"}, ConditionExpression="attribute_not_exists(pk)")
                except ClientError as exc:
                    if exc.response["Error"]["Code"] != "ConditionalCheckFailedException":
                        raise
                    status = "DUPLICATE"
            dest = f"{'accepted' if status == 'ACCEPTED' else 'quarantine'}/{sha[:12]}-{key.rsplit('/', 1)[-1]}"
            s3.copy_object(Bucket=bkt, CopySource={"Bucket": bkt, "Key": key}, Key=dest)
            ddb.put_item(Item={"pk": f"FILE#{key}", "checksum": sha, "status": status, "dest": dest, "customerHint": key.split("/")[1] if "/" in key[8:] else "unknown"})
            print(json.dumps({"level": "INFO", "msg": "file", "status": status, "key": key}))
