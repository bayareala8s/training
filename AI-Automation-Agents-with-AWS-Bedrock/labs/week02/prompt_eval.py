#!/usr/bin/env python3
"""
Lab 2.2 — Prompt evaluation harness (runs locally against Bedrock).

Usage:
  python week02/prompt_eval.py --output week02/prompt_eval_results.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.bedrock_client import converse, parse_json_from_text
from common.prompts import CLASSIFY_STRICT_SUFFIX, CLASSIFY_USER_TEMPLATE, PROMPT_VERSION_A, PROMPT_VERSION_B
from common.validation import validate_classification

GOLDEN = Path(__file__).parent / "golden_set.json"


def score_case(expected: str, predicted: str) -> int:
    return 1 if expected == predicted else 0


def run_version(version_name: str, system: str, cases: list[dict]) -> dict:
    results = []
    total = 0
    for case in cases:
        prompt = CLASSIFY_USER_TEMPLATE.format(text=case["text"]) + CLASSIFY_STRICT_SUFFIX
        out = converse(prompt, system=system, temperature=0.1)
        try:
            parsed = parse_json_from_text(out["text"])
            ok, validated, _ = validate_classification(parsed)
            label = validated.get("label", "unknown") if ok else "unknown"
        except (ValueError, json.JSONDecodeError):
            label = "unknown"
            ok = False
        pts = score_case(case["expected_label"], label)
        total += pts
        results.append({
            "id": case["id"],
            "expected": case["expected_label"],
            "predicted": label,
            "valid_json": ok,
            "score": pts,
        })
    return {
        "version": version_name,
        "total_score": total,
        "max_score": len(cases),
        "accuracy": round(total / len(cases), 3) if cases else 0,
        "cases": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="week02/prompt_eval_results.json")
    args = parser.parse_args()

    cases = json.loads(GOLDEN.read_text())
    report = {
        "version_a": run_version("A", PROMPT_VERSION_A, cases),
        "version_b": run_version("B", PROMPT_VERSION_B, cases),
    }
    a, b = report["version_a"]["accuracy"], report["version_b"]["accuracy"]
    report["winner"] = "A" if a >= b else "B"
    report["recommendation"] = (
        f"Use prompt version {report['winner']} (accuracy A={a}, B={b})."
    )

    out_path = Path(args.output)
    out_path.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
