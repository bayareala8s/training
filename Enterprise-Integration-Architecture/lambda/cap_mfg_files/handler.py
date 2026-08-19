"""Atlas Manufacturing — partner file ingest (SFTP/API landing share the same catalog)."""

from __future__ import annotations

import json
import os
import urllib.parse
from datetime import datetime, timezone
from typing import Any

import boto3

s3 = boto3.client("s3")
catalog = boto3.resource("dynamodb").Table(os.environ["CATALOG_TABLE"])


def lambda_handler(event: dict[str, Any], _ctx: Any) -> None:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for rec in event.get("Records", []):
        body = json.loads(rec["body"])
        for rec2 in body.get("Records", []):
            bkt = rec2["s3"]["bucket"]["name"]
            key = urllib.parse.unquote_plus(rec2["s3"]["object"]["key"])
            # inbound/{SUPPLIER}/file.csv
            parts = key.split("/")
            supplier = parts[1] if len(parts) > 2 else "UNKNOWN"
            obj = s3.get_object(Bucket=bkt, Key=key)
            data = obj["Body"].read()
            valid = key.lower().endswith(".csv") and len(data) > 0
            status = "ACCEPTED" if valid else "QUARANTINED"
            catalog.put_item(Item={"pk": f"FILE#{key}", "supplier": supplier, "status": status, "bytes": len(data)})
            if status == "ACCEPTED":
                catalog.put_item(Item={"pk": f"ARRIVED#{supplier}#{day}", "supplier": supplier, "key": key, "status": "ACCEPTED"})
            print(json.dumps({"level": "INFO", "msg": "mfg_file", "supplier": supplier, "status": status, "key": key}))
