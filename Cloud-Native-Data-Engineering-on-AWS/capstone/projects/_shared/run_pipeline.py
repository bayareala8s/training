#!/usr/bin/env python3
"""Shared local capstone pipeline: quality → cleaned → curated → reports.

Each option calls this with its own dataset config. Runs fully offline (no AWS).
Optional --upload when BUCKET is set (uses boto3).
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SHARED = Path(__file__).resolve().parent
sys.path.insert(0, str(SHARED))
from validators import RuleEngine  # noqa: E402


def load_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    return data.get("records", [])


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def run_quality(engine: RuleEngine, records: list[dict]) -> tuple[list[dict], list[dict], dict]:
    results = engine.validate_batch(records)
    passed, quarantined = [], []
    for r in results:
        if r.has_errors:
            quarantined.append(
                {
                    **r.record,
                    "_violations": [
                        {"rule": v.rule, "field": v.field, "message": v.message, "severity": v.severity}
                        for v in r.violations
                    ],
                }
            )
        else:
            passed.append(r.record)
    total = len(records) or 1
    report = {
        "dataset": engine.dataset,
        "version": engine.version,
        "total": len(records),
        "passed": len(passed),
        "quarantined": len(quarantined),
        "pass_rate_pct": round(len(passed) / total * 100, 2),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    return passed, quarantined, report


def upload_tree(local_root: Path, bucket: str, prefix: str) -> None:
    import boto3

    s3 = boto3.client("s3")
    for path in local_root.rglob("*"):
        if path.is_file():
            key = f"{prefix.rstrip('/')}/{path.relative_to(local_root).as_posix()}"
            s3.upload_file(str(path), bucket, key)
            print(f"  uploaded s3://{bucket}/{key}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run capstone local pipeline")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--processing-date", default="2024-01-15")
    parser.add_argument("--upload", action="store_true", help="Upload output/ to S3 if BUCKET set")
    parser.add_argument("--bucket", default="")
    args = parser.parse_args()

    root = args.project_root.resolve()
    cfg_path = root / "pipeline.json"
    if not cfg_path.exists():
        print(f"Missing {cfg_path}", file=sys.stderr)
        return 1
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    out = root / "output"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    year, month, day = args.processing_date.split("-")
    partition = f"year={year}/month={month}/day={day}"

    all_reports = []
    for ds in cfg["datasets"]:
        name = ds["name"]
        raw_file = root / ds["raw_file"]
        rules_file = root / ds["rules_file"]
        if not raw_file.exists():
            print(f"Skip missing raw file: {raw_file}")
            continue

        if raw_file.suffix.lower() == ".csv":
            records = load_csv(raw_file)
        else:
            records = load_json(raw_file)

        # Raw zone copy
        raw_out = out / "raw" / name / partition / raw_file.name
        raw_out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(raw_file, raw_out)

        engine = RuleEngine(rules_file)
        passed, quarantined, report = run_quality(engine, records)
        all_reports.append(report)

        write_json(out / "cleaned" / name / partition / "passed.json", passed)
        write_json(out / "quarantine" / name / partition / "failed.json", quarantined)
        write_json(out / "metadata" / "quality-reports" / f"{name.replace('/', '_')}_report.json", report)

        # Curated transform hook
        transform_mod = ds.get("curated_transform")
        curated_rows = passed
        if transform_mod:
            sys.path.insert(0, str(root / "src" / "etl"))
            mod = __import__(transform_mod)
            curated_rows = mod.to_curated(passed, args.processing_date)

        write_csv(out / "curated" / name / partition / "data.csv", curated_rows)
        print(f"[{name}] raw={len(records)} passed={len(passed)} quarantined={len(quarantined)} curated={len(curated_rows)}")

    # Lineage / audit manifest
    manifest = {
        "project": cfg.get("project"),
        "option": cfg.get("option"),
        "processing_date": args.processing_date,
        "reports": all_reports,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(out / "metadata" / "pipeline-runs" / f"run_{args.processing_date}.json", manifest)
    print(f"\nPipeline complete → {out}")

    bucket = args.bucket or __import__("os").environ.get("BUCKET", "")
    if args.upload and bucket:
        print(f"Uploading to s3://{bucket}/capstone/{cfg.get('project', 'project')}/ ...")
        upload_tree(out, bucket, f"capstone/{cfg.get('project', 'project')}")
    elif args.upload:
        print("WARN: --upload set but no --bucket / $BUCKET", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
