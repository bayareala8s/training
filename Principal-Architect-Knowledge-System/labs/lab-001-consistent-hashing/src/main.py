#!/usr/bin/env python3
"""Lab 001 CLI — serve API, run demo."""

from __future__ import annotations

import argparse
import json

from .api import create_app
from .service import RingService


def run_demo(service: RingService) -> None:
    service.seed_demo_cluster()
    print("==> Lab 001 Consistent Hashing — CLI demo")
    for key in [f"user:{i}" for i in range(5)]:
        print(f"  {service.lookup(key)}")
    print("==> Node failure simulation (node-b)")
    print(json.dumps(service.node_failure_simulation("node-b", 1000), indent=2))
    print("==> Churn comparison")
    print(json.dumps(service.compare_churn(5000), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 001: Consistent Hashing Ring")
    parser.add_argument("--serve", action="store_true", help="Start API on :8096")
    parser.add_argument("--demo", action="store_true", help="Run CLI demo")
    parser.add_argument("--inject", choices=["hot-key", "node-failure"])
    parser.add_argument("--port", type=int, default=8096)
    args = parser.parse_args()

    service = RingService()

    if args.inject == "hot-key":
        service.seed_demo_cluster()
        result = service.lookup("celebrity:1")
        print(f"Hot key always maps to: {result['node']}")
        return 0

    if args.inject == "node-failure":
        service.seed_demo_cluster()
        print(json.dumps(service.node_failure_simulation("node-b"), indent=2))
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
