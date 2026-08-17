"""
Lab 2.2: EventBridge-scheduled API ingestion.

Fetches paginated JSON from a public REST API and lands snapshots in S3 raw zone
with watermark metadata for incremental-style runs.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

DATA_LAKE_BUCKET = os.environ.get("DATA_LAKE_BUCKET", "")
RAW_PREFIX = os.environ.get("RAW_PREFIX", "raw/")
SOURCE_SYSTEM = os.environ.get("SOURCE_SYSTEM", "api-ingest")
DATASET = os.environ.get("DATASET", "posts")
API_URL = os.environ.get(
    "API_URL", "https://jsonplaceholder.typicode.com/posts"
)
WATERMARK_KEY = os.environ.get(
    "WATERMARK_KEY", "metadata/watermarks/api-ingest/posts.json"
)
HTTP_TIMEOUT_SECONDS = int(os.environ.get("HTTP_TIMEOUT_SECONDS", "30"))
MAX_PAGES = int(os.environ.get("MAX_PAGES", "1"))


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _http_get_json(url: str, params: dict[str, str] | None = None) -> Any:
    full_url = url
    if params:
        full_url = f"{url}?{urlencode(params)}"
    request = Request(
        full_url,
        headers={"Accept": "application/json", "User-Agent": "cnde-lab-2.2"},
    )
    with urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def _read_watermark() -> dict[str, Any]:
    if not DATA_LAKE_BUCKET:
        return {}
    try:
        obj = s3.get_object(Bucket=DATA_LAKE_BUCKET, Key=WATERMARK_KEY)
        return json.loads(obj["Body"].read().decode("utf-8"))
    except ClientError as exc:
        if exc.response["Error"]["Code"] in ("404", "NoSuchKey"):
            return {}
        raise


def _write_watermark(watermark: dict[str, Any]) -> None:
    s3.put_object(
        Bucket=DATA_LAKE_BUCKET,
        Key=WATERMARK_KEY,
        Body=json.dumps(watermark, indent=2).encode("utf-8"),
        ContentType="application/json",
    )


def _snapshot_key(run_time: datetime) -> str:
    prefix = RAW_PREFIX.rstrip("/")
    return (
        f"{prefix}/{SOURCE_SYSTEM}/{DATASET}/"
        f"year={run_time.year}/month={run_time.month:02d}/day={run_time.day:02d}/"
        f"posts_{run_time.strftime('%Y%m%dT%H%M%SZ')}.json"
    )


def fetch_and_land() -> dict[str, Any]:
    if not DATA_LAKE_BUCKET:
        raise RuntimeError("DATA_LAKE_BUCKET environment variable is not set")

    run_time = _utc_now()
    prior = _read_watermark()
    records: list[Any] = []

    for page in range(1, MAX_PAGES + 1):
        try:
            # JSONPlaceholder returns full list; pagination simulated via MAX_PAGES
            page_data = _http_get_json(API_URL)
            if isinstance(page_data, list):
                records.extend(page_data)
            else:
                records.append(page_data)
        except (HTTPError, URLError, TimeoutError) as exc:
            logger.error(json.dumps({"message": "api_fetch_failed", "page": page, "error": str(exc)}))
            raise

    snapshot = {
        "source_system": SOURCE_SYSTEM,
        "dataset": DATASET,
        "api_url": API_URL,
        "ingested_at": run_time.isoformat(),
        "record_count": len(records),
        "records": records,
        "prior_watermark": prior,
    }

    key = _snapshot_key(run_time)
    body = json.dumps(snapshot, default=str).encode("utf-8")
    s3.put_object(
        Bucket=DATA_LAKE_BUCKET,
        Key=key,
        Body=body,
        ContentType="application/json",
        Metadata={
            "record-count": str(len(records)),
            "source-system": SOURCE_SYSTEM,
        },
    )

    watermark = {
        "last_successful_run": run_time.isoformat(),
        "last_snapshot_key": key,
        "records_ingested": len(records),
        "api_url": API_URL,
    }
    _write_watermark(watermark)

    logger.info(
        json.dumps(
            {
                "message": "scheduled_ingestion_complete",
                "key": key,
                "record_count": len(records),
            }
        )
    )
    return {"bucket": DATA_LAKE_BUCKET, "key": key, "record_count": len(records), "watermark": watermark}


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    Invoked by EventBridge schedule. Event payload is typically empty or metadata.
    """
    try:
        result = fetch_and_land()
        return {"statusCode": 200, "body": json.dumps(result)}
    except Exception as exc:
        logger.exception("scheduled_ingestion_failed")
        return {"statusCode": 500, "body": json.dumps({"error": str(exc)})}
