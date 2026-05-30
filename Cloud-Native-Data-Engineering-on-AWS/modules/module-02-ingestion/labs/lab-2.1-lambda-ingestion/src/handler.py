"""
Lab 2.1: Lambda file ingestion to S3 raw zone.

Accepts JSON payloads (direct invoke or API Gateway proxy) and writes
idempotent, partitioned objects to the data lake raw zone.
"""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

# Environment variables (set in Lambda console or Terraform)
DATA_LAKE_BUCKET = os.environ.get("DATA_LAKE_BUCKET", "")
RAW_PREFIX = os.environ.get("RAW_PREFIX", "raw/")
SOURCE_SYSTEM = os.environ.get("SOURCE_SYSTEM", "lambda-ingest")
DATASET = os.environ.get("DATASET", "transactions")

# Deterministic key safe characters
SAFE_KEY_PATTERN = re.compile(r"[^a-zA-Z0-9._=-]+")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_record_id(record_id: str) -> str:
    """Sanitize record id for use in S3 object keys."""
    return SAFE_KEY_PATTERN.sub("_", record_id.strip())[:128]


def _build_raw_key(record_id: str, ingest_time: datetime) -> str:
    """
    Deterministic, idempotent S3 key.
    Re-processing the same record_id overwrites the same object with identical content.
    """
    prefix = RAW_PREFIX.rstrip("/")
    return (
        f"{prefix}/{SOURCE_SYSTEM}/{DATASET}/"
        f"year={ingest_time.year}/month={ingest_time.month:02d}/day={ingest_time.day:02d}/"
        f"{_normalize_record_id(record_id)}.json"
    )


def _validate_payload(body: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Validate required fields; return (record_id, normalized record)."""
    record_id = body.get("record_id") or body.get("id")
    if not record_id:
        raise ValueError("Payload must include 'record_id' or 'id'")

    record = {
        "record_id": str(record_id),
        "payload": body.get("data", body),
        "source_system": SOURCE_SYSTEM,
        "dataset": DATASET,
        "ingested_at": _utc_now().isoformat(),
    }
    return str(record_id), record


def ingest_record(body: dict[str, Any]) -> dict[str, Any]:
    """Write a single record to S3 raw zone."""
    if not DATA_LAKE_BUCKET:
        raise RuntimeError("DATA_LAKE_BUCKET environment variable is not set")

    record_id, record = _validate_payload(body)
    ingest_time = _utc_now()
    key = _build_raw_key(record_id, ingest_time)
    content = json.dumps(record, default=str, separators=(",", ":"))

    s3.put_object(
        Bucket=DATA_LAKE_BUCKET,
        Key=key,
        Body=content.encode("utf-8"),
        ContentType="application/json",
        Metadata={
            "source-system": SOURCE_SYSTEM,
            "dataset": DATASET,
            "record-id": _normalize_record_id(record_id),
        },
        Tagging=f"source={SOURCE_SYSTEM}&dataset={DATASET}",
    )

    logger.info(
        json.dumps(
            {
                "message": "ingestion_success",
                "bucket": DATA_LAKE_BUCKET,
                "key": key,
                "record_id": record_id,
                "bytes": len(content),
            }
        )
    )
    return {"bucket": DATA_LAKE_BUCKET, "key": key, "record_id": record_id}


def _parse_event(event: dict[str, Any]) -> list[dict[str, Any]]:
    """Support direct invoke, batch, and API Gateway proxy events."""
    if "Records" in event and isinstance(event["Records"], list):
        # Optional: SQS batch wrapper
        bodies = []
        for rec in event["Records"]:
            raw = rec.get("body", rec)
            if isinstance(raw, str):
                bodies.append(json.loads(raw))
            else:
                bodies.append(raw)
        return bodies

    if "body" in event:
        body = event["body"]
        if event.get("isBase64Encoded"):
            import base64

            body = base64.b64decode(body).decode("utf-8")
        if isinstance(body, str):
            body = json.loads(body) if body else {}
        return [body] if body else []

    if "records" in event:
        return event["records"]

    return [event]


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    Lambda entry point.

    Example test event:
    {
      "record_id": "TXN-1001",
      "data": {"amount": 250.00, "currency": "USD", "account": "****1234"}
    }
    """
    request_id = getattr(context, "aws_request_id", str(uuid4()))
    results: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    try:
        payloads = _parse_event(event)
        if not payloads:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "empty_payload", "request_id": request_id}),
            }

        for item in payloads:
            try:
                results.append(ingest_record(item))
            except (ValueError, ClientError) as exc:
                logger.exception("record_failed")
                errors.append({"error": str(exc), "record": item})

        status_code = 207 if errors and results else (400 if errors else 200)
        response_body = {
            "request_id": request_id,
            "ingested": len(results),
            "failed": len(errors),
            "results": results,
            "errors": errors,
        }
        return {"statusCode": status_code, "body": json.dumps(response_body)}

    except Exception as exc:
        logger.exception("handler_failed")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(exc), "request_id": request_id}),
        }
