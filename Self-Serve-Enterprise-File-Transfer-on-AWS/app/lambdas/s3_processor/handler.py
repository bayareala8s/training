"""Lab 3: validate S3 uploads and route to processing/ or quarantine/."""
import json
import os
from datetime import datetime, timezone
from urllib.parse import unquote_plus

import boto3

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb")

ALLOWED = {".csv", ".json", ".xml"}
MAX_BYTES = int(os.environ.get("MAX_BYTES", str(100 * 1024 * 1024)))
TABLE_NAME = os.environ["IDEMPOTENCY_TABLE"]
INBOUND_MARKER = os.environ.get("INBOUND_PREFIX", "partners/demo/inbound/")


def _log(level, **fields):
    print(json.dumps({"level": level, "ts": datetime.now(timezone.utc).isoformat(), **fields}))


def _try_claim(event_key: str) -> bool:
    table = ddb.Table(TABLE_NAME)
    try:
        table.put_item(
            Item={
                "event_key": event_key,
                "processed_at": datetime.now(timezone.utc).isoformat(),
            },
            ConditionExpression="attribute_not_exists(event_key)",
        )
        return True
    except ddb.meta.client.exceptions.ConditionalCheckFailedException:
        return False


def _route(bucket: str, key: str, zone: str) -> str:
    if INBOUND_MARKER not in key:
        dest = f"partners/demo/{zone}/{os.path.basename(key)}"
    else:
        dest = key.replace(INBOUND_MARKER, f"partners/demo/{zone}/", 1)
    s3.copy_object(
        Bucket=bucket,
        Key=dest,
        CopySource={"Bucket": bucket, "Key": key},
    )
    return dest


def handler(event, context):
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        size = int(record["s3"]["object"].get("size", 0))
        event_key = record.get("responseElements", {}).get("x-amz-request-id") or f"{bucket}:{key}"

        if not _try_claim(event_key):
            _log("INFO", status="skip_duplicate", key=key, event_key=event_key)
            continue

        ext = os.path.splitext(key)[1].lower()
        valid = size > 0 and size <= MAX_BYTES and ext in ALLOWED

        if valid:
            dest = _route(bucket, key, "processing")
            _log("INFO", status="ok", key=key, dest=dest, correlation_id=os.environ.get("CORRELATION_ID", ""))
        else:
            dest = _route(bucket, key, "quarantine")
            _log(
                "WARN",
                status="quarantine",
                key=key,
                dest=dest,
                reason="validation_failed",
                size=size,
                ext=ext,
            )

    return {"statusCode": 200}
