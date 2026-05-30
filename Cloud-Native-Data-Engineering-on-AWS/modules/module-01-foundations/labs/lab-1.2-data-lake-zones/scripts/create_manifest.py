#!/usr/bin/env python3
"""Create and upload a metadata manifest for a dataset."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import boto3


def file_checksum(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(source_file: Path, bucket: str, dataset: str) -> dict:
    stat = source_file.stat()
    return {
        "dataset": dataset,
        "version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "filename": source_file.name,
            "format": "csv",
            "size_bytes": stat.st_size,
            "checksum_sha256": file_checksum(source_file),
            "record_count_estimate": sum(1 for _ in open(source_file)) - 1,
        },
        "destination": {
            "bucket": bucket,
            "zone": "raw",
            "format": "csv",
        },
        "schema": {
            "order_id": "string",
            "customer_id": "string",
            "product_category": "string",
            "quantity": "integer",
            "unit_price": "decimal",
            "total_amount": "decimal",
            "order_status": "string",
            "order_timestamp": "timestamp",
            "region": "string",
        },
        "lineage": {
            "source_system": "lab-generator",
            "ingestion_method": "manual-upload",
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--dataset", required=True, help="e.g. retail/orders")
    parser.add_argument("--source-file", required=True)
    args = parser.parse_args()

    source = Path(args.source_file)
    manifest = build_manifest(source, args.bucket, args.dataset)
    local_manifest = source.parent / "manifest.json"
    local_manifest.write_text(json.dumps(manifest, indent=2))

    s3 = boto3.client("s3")
    key = f"metadata/{args.dataset}/manifest.json"
    s3.upload_file(str(local_manifest), args.bucket, key)
    print(f"Uploaded manifest → s3://{args.bucket}/{key}")


if __name__ == "__main__":
    main()
