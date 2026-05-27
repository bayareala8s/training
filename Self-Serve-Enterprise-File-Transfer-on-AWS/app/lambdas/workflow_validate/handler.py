"""Lab 4: Step Functions task — validate file metadata."""
import json
import os
from urllib.parse import unquote_plus

import boto3

s3 = boto3.client("s3")
ALLOWED = {".csv", ".json", ".xml"}
MAX_BYTES = int(os.environ.get("MAX_BYTES", str(100 * 1024 * 1024)))


def handler(event, context):
    bucket = event.get("bucket") or os.environ["LANDING_BUCKET"]
    key = unquote_plus(event.get("key", ""))
    correlation_id = event.get("correlation_id", "")

    if not key:
        return {"valid": False, "reason": "missing_key", "correlation_id": correlation_id}

    head = s3.head_object(Bucket=bucket, Key=key)
    size = head["ContentLength"]
    ext = os.path.splitext(key)[1].lower()
    valid = size > 0 and size <= MAX_BYTES and ext in ALLOWED

    result = {
        "valid": valid,
        "bucket": bucket,
        "key": key,
        "correlation_id": correlation_id,
        "reason": "ok" if valid else "validation_failed",
    }
    print(json.dumps(result))
    return result
