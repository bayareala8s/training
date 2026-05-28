#!/usr/bin/env python3
"""Lab 6.1 — Query audit events by correlation ID."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.audit import query_by_correlation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("correlation_id")
    args = parser.parse_args()
    items = query_by_correlation(args.correlation_id)
    print(json.dumps(items, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
