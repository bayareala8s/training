#!/usr/bin/env python3
"""Lab 014 CLI — serve API, run demo."""

from __future__ import annotations

import argparse
import json
import logging

from .api import create_app
from .service import ObservabilityService


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_demo(service: ObservabilityService) -> None:
    setup_logging()
    print("==> Lab 014 Observability — CLI demo")
    for route in ("/health", "/api", "/orders"):
        print(json.dumps(service.simulate_request(route)))
    print("==> Metrics excerpt")
    print(service.get_metrics_text())
    print("==> Recent traces")
    print(json.dumps(service.get_traces(5), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 014: Observability")
    parser.add_argument("--serve", action="store_true", help="Start API on :8104")
    parser.add_argument("--demo", action="store_true", help="Run CLI demo")
    parser.add_argument("--inject", choices=["error-spike", "latency-spike"])
    parser.add_argument("--rate", type=float, default=0.5)
    parser.add_argument("--port", type=int, default=8104)
    args = parser.parse_args()

    service = ObservabilityService()

    if args.inject:
        print(json.dumps(service.set_injection(args.inject, args.rate), indent=2))
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
