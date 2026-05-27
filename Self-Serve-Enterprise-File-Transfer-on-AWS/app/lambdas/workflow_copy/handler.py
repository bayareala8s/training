"""Lab 4: copy validated object to processing/."""
import json
import os
from urllib.parse import unquote_plus

import boto3

s3 = boto3.client("s3")
INBOUND_MARKER = os.environ.get("INBOUND_PREFIX", "partners/demo/inbound/")


def handler(event, context):
    bucket = event["bucket"]
    key = unquote_plus(event["key"])
    dest = key.replace(INBOUND_MARKER, "partners/demo/processing/", 1)
    if dest == key:
        dest = f"partners/demo/processing/{os.path.basename(key)}"

    s3.copy_object(Bucket=bucket, Key=dest, CopySource={"Bucket": bucket, "Key": key})
    out = {**event, "dest_key": dest, "status": "copied"}
    print(json.dumps(out))
    return out
