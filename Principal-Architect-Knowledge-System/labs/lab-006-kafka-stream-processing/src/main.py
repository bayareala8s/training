#!/usr/bin/env python3
"""Lab 006 CLI — serve API, run demo."""

from __future__ import annotations

import argparse
import json

from .api import create_app
from .service import StreamStack


def run_demo(stack: StreamStack) -> None:
    print("==> 1. Produce orders to `orders` topic")
    for i, amount in enumerate([49.99, 75.0, 25.5], start=1):
        result = stack.create_order("cust-42", amount, "us-west", order_id=f"ord-demo-{i}")
        print(f"    {result}")

    print("==> 2. Run enricher (orders → orders-enriched)")
    print(f"    {stack.enricher.run_once()}")

    print("==> 3. Run aggregator (1-min tumbling windows)")
    print(f"    {stack.aggregator.run_once()}")

    print("==> 4. Inject poison message → DLT")
    stack.inject_poison()
    print(f"    {stack.enricher.run_once()}")

    print("==> 5. Metrics")
    print(json.dumps(stack.list_metrics(), indent=2))

    print("==> Stats:", json.dumps(stack.stats(), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 006: Kafka Stream Processing")
    parser.add_argument("--serve", action="store_true", help="Start API on :8094")
    parser.add_argument("--demo", action="store_true", help="Run end-to-end demo")
    parser.add_argument("--port", type=int, default=8094)
    args = parser.parse_args()

    stack = StreamStack()

    if args.demo:
        run_demo(stack)
        return 0

    if args.serve:
        import uvicorn

        app = create_app(stack)
        uvicorn.run(app, host="0.0.0.0", port=args.port)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
