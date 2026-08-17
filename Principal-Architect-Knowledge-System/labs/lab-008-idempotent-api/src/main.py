#!/usr/bin/env python3
"""Lab 008 CLI — serve API, run demo."""

from __future__ import annotations

import argparse

from .api import create_app
from .service import PaymentService


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 008: Idempotent API")
    parser.add_argument("--serve", action="store_true", help="Start API on :8081")
    parser.add_argument("--demo", action="store_true", help="Run idempotency retry demo")
    parser.add_argument("--port", type=int, default=8081)
    args = parser.parse_args()

    service = PaymentService()

    if args.demo:
        body = {"amount": 49.99, "currency": "USD"}
        key = "demo-key"
        s1, r1 = service.create_payment("demo", key, body)
        s2, r2 = service.create_payment("demo", key, body)
        print(f"First:  {s1} {r1}")
        print(f"Retry:  {s2} {r2}")
        print(f"Ledger entries: {service.ledger_count()} (expect 1)")
        return 0

    if args.serve:
        import uvicorn

        app = create_app(service)
        uvicorn.run(app, host="0.0.0.0", port=args.port)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
