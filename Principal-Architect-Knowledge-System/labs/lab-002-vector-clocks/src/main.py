#!/usr/bin/env python3
"""Lab 002 CLI — serve API, run demo."""

from __future__ import annotations

import argparse
import json

from .api import create_app
from .service import ClockService


def run_demo(service: ClockService) -> None:
    service.seed_demo_processes(2)
    print("==> Lab 002 Vector Clocks — CLI demo")
    service.send_message(0, 1, "hello", "m1")
    service.local_event(1)
    print("==> Causal mailbox delivery order:")
    for m in service.mailbox.delivered:
        print(f"  {m.msg_id} sender=P{m.sender} clock={m.clock.values}")
    print("==> Process clocks after demo:")
    print(json.dumps(service.list_processes(), indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 002: Vector Clocks")
    parser.add_argument("--serve", action="store_true", help="Start API on :8097")
    parser.add_argument("--demo", action="store_true", help="Run CLI demo")
    parser.add_argument("--inject", choices=["delayed-message", "duplicate-delivery"])
    parser.add_argument("--port", type=int, default=8097)
    args = parser.parse_args()

    service = ClockService()

    if args.inject:
        print(
            f"Injection: {args.inject} — use CausalMailbox gap detection "
            "to hold out-of-order messages"
        )
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
