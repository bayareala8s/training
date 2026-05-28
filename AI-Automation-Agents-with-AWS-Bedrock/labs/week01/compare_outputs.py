#!/usr/bin/env python3
"""
Lab 1.2 — Compare prompts and temperatures.

Usage:
  python week01/compare_outputs.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.bedrock_client import converse
from common.config import BEDROCK_MODEL_ID

TASK = "Classify urgency of this ticket as low, medium, or high and explain in one sentence: Database replication lag alert in production."


def run_variant(name: str, prompt: str, temperature: float) -> dict:
    result = converse(prompt, temperature=temperature, model_id=BEDROCK_MODEL_ID)
    return {
        "variant": name,
        "temperature": temperature,
        "latency_ms": result["latency_ms"],
        "output_preview": result["text"][:300],
    }


def main() -> int:
    runs = [
        run_variant("open_ended_low_temp", TASK, 0.1),
        run_variant("open_ended_moderate_temp", TASK, 0.7),
        run_variant(
            "strict_json_low_temp",
            TASK + '\nRespond with JSON only: {"urgency":"low|medium|high","reason":"..."}',
            0.1,
        ),
        run_variant(
            "strict_json_moderate_temp",
            TASK + '\nRespond with JSON only: {"urgency":"low|medium|high","reason":"..."}',
            0.7,
        ),
    ]

    print(json.dumps(runs, indent=2))
    print("\nRecommendation for automation: strict JSON + low temperature (0.1–0.2).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
