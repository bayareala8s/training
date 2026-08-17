#!/usr/bin/env python3
"""
Week 6 Lab 6.2 helper — generate API errors to exercise CloudWatch alarm.

Usage (stack must be running):
  source .stack.env
  python week06/trigger_alarm.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

LABS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LABS_ROOT))


def load_stack_env() -> None:
    env_file = LABS_ROOT / ".stack.env"
    if not env_file.exists():
        print("ERROR: Run ./scripts/start.sh first (missing .stack.env)")
        raise SystemExit(1)
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line.startswith("export "):
            key, _, val = line[7:].partition("=")
            os.environ.setdefault(key, val.strip('"'))


def post_bad(url: str) -> int:
    req = urllib.request.Request(
        url,
        data=b"not-json",
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code


def main() -> int:
    load_stack_env()
    api_base = os.environ.get("API_ENDPOINT", "").rstrip("/")
    prefix = os.environ.get("PROJECT_PREFIX", "ba-la8s-ai")
    if not api_base:
        print("ERROR: API_ENDPOINT not set")
        return 1

    print(f"Sending malformed requests to {api_base}/classify ...")
    codes = []
    for i in range(3):
        code = post_bad(f"{api_base}/classify")
        codes.append(code)
        print(f"  request {i + 1}: HTTP {code}")

    print()
    print("Next steps:")
    print(f"  1. CloudWatch → Dashboards → {prefix}-ai-ops")
    print(f"  2. CloudWatch → Alarms → {prefix}-api-errors")
    print("  3. Capture a screenshot for your Week 6 assignment")
    print(f"\nResponse codes: {codes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
