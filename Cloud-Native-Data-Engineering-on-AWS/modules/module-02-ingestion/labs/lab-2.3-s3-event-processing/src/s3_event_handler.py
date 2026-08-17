"""
Lab 2.3: S3 event-driven file promotion.

Triggered by S3 ObjectCreated on an incoming/ prefix; validates file metadata,
promotes to partitioned raw/ path, or routes failures to quarantine/.
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.parse
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

DATA_LAKE_BUCKET = os.environ.get("DATA_LAKE_BUCKET", "")
INCOMING_PREFIX = os.environ.get("INCOMING_PREFIX", "incoming/")
RAW_PREFIX = os.environ.get("RAW_PREFIX", "raw/")
QUARANTINE_PREFIX = os.environ.get("QUARANTINE_PREFIX", "quarantine/")
SOURCE_SYSTEM = os.environ.get("SOURCE_SYSTEM", "file-upload")
DATASET = os.environ.get("DATASET", "transactions")
MAX_FILE_BYTES = int(os.environ.get("MAX_FILE_BYTES", str(10 * 1024 * 1024)))
ALLOWED_SUFFIXES = tuple(
    s.strip().lower()
    for s in os.environ.get("ALLOWED_SUFFIXES", ".csv,.json,.jsonl").split(",")
    if s.strip()
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _decode_s3_key(key: str) -> str:
    return urllib.parse.unquote_plus(key)


def _validate_key(key: str, size: int) -> None:
    if not key.startswith(INCOMING_PREFIX):
        raise ValueError(f"Key {key} is outside incoming prefix {INCOMING_PREFIX}")
    if size <= 0:
        raise ValueError("Empty file not allowed")
    if size > MAX_FILE_BYTES:
        raise ValueError(f"File exceeds max size {MAX_FILE_BYTES} bytes")
    if ALLOWED_SUFFIXES and not key.lower().endswith(ALLOWED_SUFFIXES):
        raise ValueError(f"File suffix not in allowed list: {ALLOWED_SUFFIXES}")


def _extract_batch_id(key: str) -> str:
    """Derive stable batch id from filename for idempotent promotion."""
    filename = key.split("/")[-1]
    base = re.sub(r"\.[^.]+$", "", filename)
    safe = re.sub(r"[^a-zA-Z0-9._=-]", "_", base)[:64]
    return safe or "unknown_batch"


def _promoted_key(source_key: str, batch_id: str, ingest_time: datetime) -> str:
    suffix = ""
    if "." in source_key:
        suffix = source_key[source_key.rfind(".") :]
    prefix = RAW_PREFIX.rstrip("/")
    return (
        f"{prefix}/{SOURCE_SYSTEM}/{DATASET}/"
        f"year={ingest_time.year}/month={ingest_time.month:02d}/day={ingest_time.day:02d}/"
        f"{batch_id}{suffix}"
    )


def _quarantine_key(source_key: str, reason: str) -> str:
    ts = _utc_now().strftime("%Y%m%dT%H%M%SZ")
    filename = source_key.split("/")[-1]
    prefix = QUARANTINE_PREFIX.rstrip("/")
    return f"{prefix}/{SOURCE_SYSTEM}/{DATASET}/{ts}_{filename}.error.json"


def _copy_object(bucket: str, source_key: str, dest_key: str, metadata: dict[str, str]) -> None:
    copy_source = {"Bucket": bucket, "Key": source_key}
    s3.copy_object(
        Bucket=bucket,
        Key=dest_key,
        CopySource=copy_source,
        Metadata=metadata,
        MetadataDirective="REPLACE",
        TaggingDirective="COPY",
    )


def _write_quarantine_manifest(bucket: str, source_key: str, reason: str) -> str:
    manifest_key = _quarantine_key(source_key, reason)
    manifest = {
        "source_bucket": bucket,
        "source_key": source_key,
        "reason": reason,
        "quarantined_at": _utc_now().isoformat(),
    }
    s3.put_object(
        Bucket=bucket,
        Key=manifest_key,
        Body=json.dumps(manifest).encode("utf-8"),
        ContentType="application/json",
    )
    return manifest_key


def process_record(record: dict[str, Any]) -> dict[str, Any]:
    """Process a single S3 event record."""
    bucket = record["s3"]["bucket"]["name"]
    key = _decode_s3_key(record["s3"]["object"]["key"])
    size = int(record["s3"]["object"].get("size", 0))

    ingest_time = _utc_now()
    try:
        _validate_key(key, size)
        batch_id = _extract_batch_id(key)
        dest_key = _promoted_key(key, batch_id, ingest_time)

        # Idempotent: copy to deterministic raw path (overwrites same batch_id+suffix)
        _copy_object(
            bucket,
            key,
            dest_key,
            metadata={
                "source-system": SOURCE_SYSTEM,
                "dataset": DATASET,
                "source-key": key[:256],
                "ingested-at": ingest_time.isoformat(),
                "batch-id": batch_id,
            },
        )

        logger.info(
            json.dumps(
                {
                    "message": "promotion_success",
                    "source_key": key,
                    "dest_key": dest_key,
                    "bytes": size,
                }
            )
        )
        return {"status": "promoted", "source_key": key, "dest_key": dest_key, "batch_id": batch_id}

    except (ValueError, ClientError) as exc:
        manifest_key = _write_quarantine_manifest(bucket, key, str(exc))
        logger.warning(
            json.dumps(
                {
                    "message": "quarantined",
                    "source_key": key,
                    "manifest_key": manifest_key,
                    "reason": str(exc),
                }
            )
        )
        return {"status": "quarantined", "source_key": key, "manifest_key": manifest_key, "reason": str(exc)}


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Lambda entry point for S3 event notifications."""
    if DATA_LAKE_BUCKET and event.get("Records"):
        # Guard: only process events for configured bucket when set
        for record in event["Records"]:
            if record.get("s3", {}).get("bucket", {}).get("name") != DATA_LAKE_BUCKET:
                logger.warning(
                    json.dumps(
                        {
                            "message": "bucket_mismatch",
                            "expected": DATA_LAKE_BUCKET,
                            "received": record.get("s3", {}).get("bucket", {}).get("name"),
                        }
                    )
                )

    results = []
    for record in event.get("Records", []):
        if record.get("eventSource") != "aws:s3":
            continue
        results.append(process_record(record))

    return {
        "statusCode": 200,
        "body": json.dumps({"processed": len(results), "results": results}),
    }
