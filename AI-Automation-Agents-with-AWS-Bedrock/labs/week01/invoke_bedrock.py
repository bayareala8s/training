#!/usr/bin/env python3
"""
Lab 1.1 — First Bedrock invocation with latency measurement.

Usage (from labs/ directory):
  export AWS_PROFILE=your-profile
  export AWS_REGION=us-east-1
  export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
  python week01/invoke_bedrock.py --prompt "Explain idempotency in one sentence."
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow imports from labs/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.bedrock_client import converse
from common.config import BEDROCK_MODEL_ID, DEFAULT_TEMPERATURE


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 1.1 — Invoke Bedrock")
    parser.add_argument("--prompt", default="What is AWS Step Functions in one sentence?")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--model-id", default=BEDROCK_MODEL_ID)
    args = parser.parse_args()

    print(f"Model: {args.model_id}")
    print(f"Temperature: {args.temperature}")
    print("Invoking Bedrock...\n")

    result = converse(args.prompt, model_id=args.model_id, temperature=args.temperature)

    print("--- Response ---")
    print(result["text"])
    print("\n--- Metrics ---")
    print(json.dumps({
        "latency_ms": result["latency_ms"],
        "model_id": result["model_id"],
        "usage": result.get("usage", {}),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
