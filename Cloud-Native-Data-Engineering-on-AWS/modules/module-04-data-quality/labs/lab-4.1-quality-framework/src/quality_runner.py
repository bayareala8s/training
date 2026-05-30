#!/usr/bin/env python3
"""Batch quality runner: validate records and route to pass/quarantine."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from validators import RuleEngine, ValidationResult


def load_records(input_path: Path) -> list[dict]:
    with input_path.open(encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "records" in data:
        return data["records"]
    raise ValueError("Input must be a JSON array or object with 'records' key")


def serialize_violations(result: ValidationResult) -> list[dict]:
    return [
        {
            "rule": v.rule,
            "field": v.field,
            "message": v.message,
            "severity": v.severity,
            "actual_value": v.actual_value,
        }
        for v in result.violations
    ]


def route_records(
    results: list[ValidationResult],
    strict: bool = False,
) -> tuple[list[dict], list[dict]]:
    """Split records into passed and quarantined based on severity."""
    passed: list[dict] = []
    quarantined: list[dict] = []

    for result in results:
        should_quarantine = result.has_errors or (strict and result.has_warnings)

        if should_quarantine:
            quarantined.append(
                {
                    **result.record,
                    "_violations": serialize_violations(result),
                    "_quarantine_reason": "validation_failed",
                }
            )
        else:
            record = dict(result.record)
            warnings = [v for v in result.violations if v.severity == "warning"]
            if warnings:
                record["_quality_flags"] = serialize_violations(result)
            passed.append(record)

    return passed, quarantined


def build_report(
    engine: RuleEngine,
    results: list[ValidationResult],
    passed: list[dict],
    quarantined: list[dict],
    batch_id: str,
) -> dict:
    violation_counts: Counter[str] = Counter()
    for result in results:
        for v in result.violations:
            if v.severity == "error":
                violation_counts[v.rule] += 1

    total = len(results)
    pass_count = len(passed)
    fail_count = len(quarantined)
    pass_rate = (pass_count / total * 100) if total else 100.0

    top_violations = [
        {"rule": rule, "count": count}
        for rule, count in violation_counts.most_common(10)
    ]

    return {
        "report_timestamp": datetime.now(timezone.utc).isoformat(),
        "dataset": engine.dataset,
        "rules_version": engine.version,
        "batch_id": batch_id,
        "summary": {
            "total_records": total,
            "passed": pass_count,
            "quarantined": fail_count,
            "pass_rate_pct": round(pass_rate, 2),
        },
        "top_violations": top_violations,
        "slo_status": {
            "completeness_target_pct": 99.9,
            "completeness_actual_pct": round(pass_rate, 2),
            "within_slo": pass_rate >= 99.9,
        },
    }


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
        f.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate records against JSON rules and route to quarantine."
    )
    parser.add_argument("--rules", required=True, help="Path to rules JSON file")
    parser.add_argument("--input", required=True, help="Path to input records JSON")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for passed, quarantined, and report files",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warning-severity violations as quarantine triggers",
    )
    parser.add_argument(
        "--batch-id",
        default=None,
        help="Optional batch identifier (defaults to UUID)",
    )
    args = parser.parse_args()

    rules_path = Path(args.rules)
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    batch_id = args.batch_id or str(uuid.uuid4())

    if not rules_path.exists():
        print(f"Error: rules file not found: {rules_path}", file=sys.stderr)
        return 1
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    engine = RuleEngine(rules_path)
    records = load_records(input_path)
    results = engine.validate_batch(records)
    passed, quarantined = route_records(results, strict=args.strict)

    write_json(output_dir / "passed_records.json", passed)
    write_json(output_dir / "quarantined_records.json", quarantined)
    report = build_report(engine, results, passed, quarantined, batch_id)
    write_json(output_dir / "quality_report.json", report)

    summary = report["summary"]
    print(f"Processed {summary['total_records']} records")
    print(f"  Passed:      {summary['passed']}")
    print(f"  Quarantined: {summary['quarantined']}")
    print(f"  Pass rate:   {summary['pass_rate_pct']:.2f}%")
    print(f"Report written to {output_dir / 'quality_report.json'}")

    if not report["slo_status"]["within_slo"]:
        print("WARNING: Pass rate below 99.9% SLO target")

    return 0


if __name__ == "__main__":
    sys.exit(main())
