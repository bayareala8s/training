#!/usr/bin/env python3
"""Lab 005 CLI — serve API, run demo."""

from __future__ import annotations

import argparse
import json

from .api import create_app
from .service import ConsistencyService


def run_demo(service: ConsistencyService) -> None:
    print("==> Lab 005 Eventual Consistency — CLI demo")
    print(json.dumps(service.put_key("user:1", "alice", "r1"), indent=2))
    print("==> Stale read on r2 (before replication)")
    print(json.dumps(service.get_key("user:1", "r2"), indent=2))
    print("==> Run replication")
    print(json.dumps(service.run_replication(), indent=2))
    print("==> Converged read on r2")
    print(json.dumps(service.get_key("user:1", "r2"), indent=2))
    print("==> Converge check")
    print(json.dumps(service.converge(), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 005: Eventual Consistency")
    parser.add_argument("--serve", action="store_true", help="Start API on :8099")
    parser.add_argument("--demo", action="store_true", help="Run CLI demo")
    parser.add_argument("--inject", choices=["partition", "replica-down", "delay"])
    parser.add_argument("--duration", type=int, default=30)
    parser.add_argument("--port", type=int, default=8099)
    args = parser.parse_args()

    service = ConsistencyService()

    if args.inject:
        if args.inject == "partition":
            print(json.dumps(service.set_partition(["r3"], True), indent=2))
        else:
            print(f"Injection {args.inject} for {args.duration}s — use API chaos endpoints")
        return 0

    if args.demo:
        run_demo(service)
        return 0

    if args.serve:
        import uvicorn

        app = create_app(service)
        uvicorn.run(app, host="0.0.0.0", port=args.port)
        return 0

    run_demo(service)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
