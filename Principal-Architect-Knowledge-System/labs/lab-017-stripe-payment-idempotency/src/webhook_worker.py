"""Webhook worker — consumes queue like SQS → Lambda."""

from __future__ import annotations

import time

from .queue import WebhookQueue
from .service import PaymentService


def run_worker(service: PaymentService, queue: WebhookQueue, poll_seconds: int = 30) -> None:
    print("Webhook worker started — polling queue")
    end = time.time() + poll_seconds
    while time.time() < end:
        event = queue.consume(timeout_seconds=1)
        if event:
            ok = service.process_webhook(event)
            print(f"Processed webhook {event.get('event_id')}: duplicate={not ok}")
        time.sleep(0.1)
    print("Webhook worker stopped")
