"""
ECS Fargate worker — large file processing (Lab 9).

Streams an S3 object, computes SHA-256, copies to processed prefix, writes manifest.
Job JSON in env TRANSFER_JOB:
  bucket, source_key, dest_prefix (optional), correlation_id, job_id (optional)
"""
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")


def _log(level: str, **fields):
    print(json.dumps({"level": level, "ts": datetime.now(timezone.utc).isoformat(), **fields}))


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    raw = os.environ.get("TRANSFER_JOB", "{}")
    job = json.loads(raw)
    bucket = job["bucket"]
    source_key = job["source_key"]
    correlation_id = job.get("correlation_id", "unknown")
    dest_prefix = job.get("dest_prefix", "partners/demo/large/processed/")

    if not dest_prefix.endswith("/"):
        dest_prefix += "/"

    basename = os.path.basename(source_key)
    dest_key = f"{dest_prefix}{basename}"
    manifest_key = f"{dest_key}.manifest.json"

    _log("INFO", status="start", correlation_id=correlation_id, source_key=source_key)

    with tempfile.TemporaryDirectory() as tmp:
        local_path = os.path.join(tmp, basename)
        _log("INFO", status="downloading", correlation_id=correlation_id)
        s3.download_file(bucket, source_key, local_path)
        size = os.path.getsize(local_path)
        digest = _sha256_file(local_path)

        _log("INFO", status="uploading", correlation_id=correlation_id, dest_key=dest_key, bytes=size)
        s3.upload_file(local_path, bucket, dest_key)

        manifest = {
            "correlation_id": correlation_id,
            "source_key": source_key,
            "dest_key": dest_key,
            "sha256": digest,
            "bytes": size,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "processor": "ecs-fargate",
        }
        s3.put_object(
            Bucket=bucket,
            Key=manifest_key,
            Body=json.dumps(manifest, indent=2).encode(),
            ContentType="application/json",
        )

    _log("INFO", status="complete", correlation_id=correlation_id, dest_key=dest_key, sha256=digest)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        _log("ERROR", status="failed", error=str(exc))
        sys.exit(1)
