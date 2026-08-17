#!/usr/bin/env python3
"""Lab 017 CLI — migrate, API server, worker, sweeper, demo."""

from __future__ import annotations

import argparse
import os
import sys

from .api import create_app
from .db import Database
from .queue import WebhookQueue
from .service import PaymentService
from .stripe_mock import StripeMock
from .sweeper import run_sweeper
from .webhook_worker import run_worker


def _build_stack(
    database_url: str | None,
    redis_url: str | None,
    stripe_delay: float,
) -> tuple[PaymentService, WebhookQueue, StripeMock]:
    dsn = database_url or os.getenv(
        "DATABASE_URL", "sqlite:./data/stripe_lab.db"
    )
    redis = redis_url or os.getenv("REDIS_URL")
    queue = WebhookQueue(redis_url=redis)
    db = Database(dsn)
    db.migrate()

    def on_success(event: dict) -> None:
        queue.publish(event)

    stripe = StripeMock(delay_seconds=stripe_delay, on_success=on_success)
    service = PaymentService(db, stripe, queue)
    return service, queue, stripe


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lab 017: Stripe Payment Idempotency (local)"
    )
    parser.add_argument("--migrate", action="store_true", help="Run schema migration")
    parser.add_argument("--serve", action="store_true", help="Start API on :8080")
    parser.add_argument("--worker", action="store_true", help="Run webhook worker")
    parser.add_argument("--sweeper", action="store_true", help="Run idempotency sweeper")
    parser.add_argument("--demo", action="store_true", help="Run timeout-retry demo")
    parser.add_argument("--database-url", default=None)
    parser.add_argument("--redis-url", default=None)
    parser.add_argument("--stripe-delay", type=float, default=0.0)
    args = parser.parse_args()

    service, queue, stripe = _build_stack(
        args.database_url, args.redis_url, args.stripe_delay
    )

    if args.migrate:
        print("Schema migrated.")
        return 0

    if args.serve:
        import uvicorn

        app = create_app(service)
        uvicorn.run(app, host="0.0.0.0", port=8080)
        return 0

    if args.worker:
        run_worker(service, queue)
        return 0

    if args.sweeper:
        run_sweeper(service)
        return 0

    if args.demo:
        body = {"amount_cents": 1999, "currency": "usd"}
        key = "demo-timeout-key"
        s1, r1 = service.create_charge("demo", key, body)
        s2, r2 = service.create_charge("demo", key, body)
        print(f"First: {s1} {r1}")
        print(f"Retry: {s2} {r2}")
        print(f"Orders: {service.db.count_orders()} Stripe intents: {stripe.intent_count()}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
