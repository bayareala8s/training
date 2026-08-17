#!/usr/bin/env python3
"""Validate data lake zone structure."""

import argparse
import sys

import boto3
from botocore.exceptions import ClientError


def check_prefix(s3, bucket: str, prefix: str) -> bool:
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1)
    return resp.get("KeyCount", 0) > 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    args = parser.parse_args()

    s3 = boto3.client("s3")
    checks = [
        ("raw/retail/orders partition exists", "raw/retail/orders/"),
        ("metadata/retail/orders/manifest.json exists", "metadata/retail/orders/manifest.json"),
        ("cleaned/ zone accessible", "cleaned/"),
        ("curated/ zone accessible", "curated/"),
        ("quarantine/ zone accessible", "quarantine/"),
    ]

    passed = 0
    for label, prefix in checks:
        try:
            ok = check_prefix(s3, args.bucket, prefix)
            status = "✓" if ok else "✗"
            print(f"{status} {label}")
            if ok:
                passed += 1
        except ClientError as e:
            print(f"✗ {label}: {e}")

    if passed == len(checks):
        print("All zone validations passed.")
        sys.exit(0)
    else:
        print(f"{passed}/{len(checks)} checks passed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
