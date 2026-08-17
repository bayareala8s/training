#!/usr/bin/env python3
"""Lab 011 CLI — serve API, run demo."""

from __future__ import annotations

import argparse
import json

from .api import create_app
from .service import RateLimitService


def run_demo(service: RateLimitService) -> None:
    print("==> Lab 011 Rate Limiter — CLI demo")
    for i in range(3):
        result = service.check("tenant-1", "/api")
        print(f"  check {i + 1}: allowed={result.allowed} remaining={result.remaining}")
    print("==> Stats")
    print(json.dumps(service.stats(), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 011: Rate Limiter")
    parser.add_argument("--serve", action="store_true", help="Start API on :8101")
    parser.add_argument("--demo", action="store_true", help="Run CLI demo")
    parser.add_argument("--inject", choices=["redis-down"])
    parser.add_argument("--mode", choices=["fail-open", "fail-closed"], default="fail-closed")
    parser.add_argument("--port", type=int, default=8101)
    args = parser.parse_args()

    service = RateLimitService()

    if args.inject == "redis-down":
        print(json.dumps(service.simulate_redis_down(True, args.mode), indent=2))
        result = service.check("tenant-1", "/api")
        print(f"check during outage: allowed={result.allowed}")
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
