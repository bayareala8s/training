#!/usr/bin/env python3
"""Lab 009 CLI — serve API, run demo."""

from __future__ import annotations

import argparse
import json

from .api import create_app
from .service import OutboxStack


def run_demo(stack: OutboxStack) -> None:
    print("==> 1. Create order (atomic order + outbox)")
    order, event = stack.orders.create_order("DEMO-SKU", 3)
    print(f"    order={order.order_id} event={event.id} pending={stack.db.pending_outbox_count()}")

    print("==> 2. Run relay (publish to broker)")
    published = stack.relay.run_once()
    print(f"    published={published} broker={len(stack.broker)}")

    print("==> 3. Run consumer (idempotent inventory)")
    r1 = stack.consumer.process_broker(stack.broker)
    print(f"    {r1}")

    print("==> 4. Run consumer again (duplicates deduped)")
    r2 = stack.consumer.process_broker(stack.broker)
    print(f"    {r2}")

    print("==> Stats:", json.dumps(stack.stats(), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 009: Transactional Outbox")
    parser.add_argument("--serve", action="store_true", help="Start API on :8092")
    parser.add_argument("--demo", action="store_true", help="Run end-to-end demo")
    parser.add_argument("--port", type=int, default=8092)
    args = parser.parse_args()

    stack = OutboxStack()

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
