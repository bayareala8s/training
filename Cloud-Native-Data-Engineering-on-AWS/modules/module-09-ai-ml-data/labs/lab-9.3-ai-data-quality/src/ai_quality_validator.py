#!/usr/bin/env python3
"""
Lab 9.3: AI data quality validation for ML training datasets.

Validates label balance, null rates, PSI drift, leakage correlation,
duplicate entities, and feature ranges. Outputs ai_quality_report.json.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError:
    print("Install dependencies: pip install pandas pyarrow", file=sys.stderr)
    sys.exit(1)


def load_rules(path: Path) -> dict[str, Any]:
    with open(path) as f:
        return json.load(f)


def load_split(data_dir: Path, name: str) -> pd.DataFrame:
    path = data_dir / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Missing split: {path}. Run Lab 9.1 first.")
    return pd.read_parquet(path)


def check_label_balance(df: pd.DataFrame, cfg: dict[str, Any]) -> dict[str, Any]:
    col = cfg["column"]
    rate = float(df[col].mean())
    passed = cfg["min_positive_rate"] <= rate <= cfg["max_positive_rate"]
    return {
        "check": "label_balance",
        "passed": passed,
        "positive_rate": round(rate, 4),
        "severity": cfg["severity"],
        "message": f"Label rate {rate:.2%} outside [{cfg['min_positive_rate']}, {cfg['max_positive_rate']}]"
        if not passed
        else "Label balance OK",
    }


def check_null_rate(df: pd.DataFrame, cfg: dict[str, Any]) -> dict[str, Any]:
    exclude = set(cfg.get("exclude_columns", []))
    violations = []
    for col in df.columns:
        if col in exclude:
            continue
        if not pd.api.types.is_numeric_dtype(df[col]) and df[col].dtype != "object":
            continue
        rate = float(df[col].isna().mean())
        if rate > cfg["max_null_rate"]:
            violations.append({"column": col, "null_rate": round(rate, 4)})
    return {
        "check": "feature_null_rate",
        "passed": len(violations) == 0,
        "violations": violations,
        "severity": cfg["severity"],
        "message": f"{len(violations)} columns exceed null threshold" if violations else "Null rates OK",
    }


def _psi(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    """Population Stability Index for numeric feature."""
    expected = expected.dropna()
    actual = actual.dropna()
    if len(expected) < bins or len(actual) < bins:
        return 0.0
    breakpoints = pd.qcut(expected, q=bins, duplicates="drop", retbins=True)[1]
    expected_pct = pd.cut(expected, bins=breakpoints, include_lowest=True).value_counts(normalize=True)
    actual_pct = pd.cut(actual, bins=breakpoints, include_lowest=True).value_counts(normalize=True)
    aligned = pd.concat([expected_pct, actual_pct], axis=1, keys=["exp", "act"]).fillna(0.0001)
    psi = ((aligned["act"] - aligned["exp"]) * (aligned["act"] / aligned["exp"]).apply(math.log)).sum()
    return float(psi)


def check_psi(train: pd.DataFrame, test: pd.DataFrame, cfg: dict[str, Any]) -> dict[str, Any]:
    results = []
    for feat in cfg["features"]:
        if feat not in train.columns or feat not in test.columns:
            continue
        psi = _psi(train[feat], test[feat])
        level = "ok"
        if psi >= cfg["psi_error"]:
            level = "error"
        elif psi >= cfg["psi_warning"]:
            level = "warning"
        results.append({"feature": feat, "psi": round(psi, 4), "level": level})
    failed = [r for r in results if r["level"] == "error"]
    warned = [r for r in results if r["level"] == "warning"]
    return {
        "check": "feature_drift_psi",
        "passed": len(failed) == 0,
        "results": results,
        "warnings": len(warned),
        "severity": cfg["severity"],
        "message": f"PSI errors: {len(failed)}, warnings: {len(warned)}",
    }


def check_leakage(df: pd.DataFrame, cfg: dict[str, Any]) -> dict[str, Any]:
    label = cfg["label_column"]
    exclude = set(cfg.get("exclude_columns", [])) | {label}
    numeric = df.select_dtypes(include="number").columns
    suspicious = []
    for col in numeric:
        if col in exclude:
            continue
        corr = df[col].corr(df[label])
        if abs(corr) > cfg["max_abs_correlation"]:
            suspicious.append({"column": col, "correlation": round(float(corr), 4)})
    return {
        "check": "leakage_correlation",
        "passed": len(suspicious) == 0,
        "suspicious": suspicious,
        "severity": cfg["severity"],
        "message": f"{len(suspicious)} features with high label correlation" if suspicious else "No leakage detected",
    }


def check_duplicates(df: pd.DataFrame, cfg: dict[str, Any]) -> dict[str, Any]:
    dupes = df.duplicated(subset=[cfg["entity_column"], cfg["snapshot_column"]]).sum()
    return {
        "check": "duplicate_entities",
        "passed": dupes == 0,
        "duplicate_count": int(dupes),
        "severity": cfg["severity"],
        "message": f"{dupes} duplicate entity-snapshot rows" if dupes else "No duplicate entities",
    }


def check_ranges(df: pd.DataFrame, cfg: dict[str, Any]) -> dict[str, Any]:
    violations = []
    for rule in cfg["rules"]:
        col = rule["column"]
        if col not in df.columns:
            continue
        out_of_range = df[(df[col] < rule["min"]) | (df[col] > rule["max"])]
        if len(out_of_range):
            violations.append({"column": col, "count": len(out_of_range)})
    return {
        "check": "feature_range",
        "passed": len(violations) == 0,
        "violations": violations,
        "severity": cfg["severity"],
        "message": f"{len(violations)} range violations" if violations else "Feature ranges OK",
    }


def _json_safe(obj: Any) -> Any:
    """Convert numpy/pandas scalars to native Python types for json.dump."""
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]
    if hasattr(obj, "item"):
        return obj.item()
    return obj


def run_validation(data_dir: Path, rules: dict[str, Any]) -> dict[str, Any]:
    train = load_split(data_dir, "train")
    test = load_split(data_dir, "test")
    combined = pd.concat([train, test], ignore_index=True)
    checks_cfg = rules["checks"]

    results = [
        check_label_balance(combined, checks_cfg["label_balance"]),
        check_null_rate(combined, checks_cfg["feature_null_rate"]),
        check_psi(train, test, checks_cfg["feature_drift_psi"]),
        check_leakage(combined, checks_cfg["leakage_correlation"]),
        check_duplicates(combined, checks_cfg["duplicate_entities"]),
        check_ranges(combined, checks_cfg["feature_range"]),
    ]

    errors = [r for r in results if not r["passed"] and r["severity"] == "error"]
    warnings = [r for r in results if not r["passed"] and r["severity"] == "warning"]

    return _json_safe({
        "dataset": rules["dataset"],
        "version": rules["version"],
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "overall_passed": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "checks": results,
    })


def main() -> None:
    parser = argparse.ArgumentParser(description="AI data quality validation")
    parser.add_argument(
        "--rules",
        type=Path,
        default=Path(__file__).parent / "ai_quality_rules.json",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "lab-9.1-ml-dataset-prep" / "output",
        help="Directory containing train.parquet and test.parquet",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "output",
    )
    args = parser.parse_args()

    rules = load_rules(args.rules)
    report = run_validation(args.data_dir, rules)

    args.output.mkdir(parents=True, exist_ok=True)
    report_path = args.output / "ai_quality_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))
    print(f"\nReport written to {report_path}")
    print(f"Overall: {'PASSED' if report['overall_passed'] else 'FAILED'} "
          f"({report['error_count']} errors, {report['warning_count']} warnings)")

    sys.exit(0 if report["overall_passed"] else 1)


if __name__ == "__main__":
    main()
