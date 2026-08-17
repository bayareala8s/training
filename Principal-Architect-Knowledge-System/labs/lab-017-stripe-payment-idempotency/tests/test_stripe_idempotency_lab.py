"""Pytest suite for Lab 017."""

from __future__ import annotations

import os
import sys
import tempfile
import threading
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

LAB_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LAB_ROOT))

from src.api import create_app  # noqa: E402
from src.db import Database  # noqa: E402
from src.queue import WebhookQueue  # noqa: E402
from src.service import PaymentService, StoreUnavailableError  # noqa: E402
from src.stripe_mock import StripeMock  # noqa: E402


@pytest.fixture()
def service() -> PaymentService:
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db = Database(f"sqlite:{path}")
    db.migrate()
    queue = WebhookQueue()
    stripe = StripeMock(on_success=queue.publish)
    yield PaymentService(db, stripe, queue)
    os.unlink(path)


def test_duplicate_retry_same_response(service: PaymentService) -> None:
    body = {"amount_cents": 5000, "currency": "usd"}
    s1, r1 = service.create_charge("t1", "key-abc", body)
    s2, r2 = service.create_charge("t1", "key-abc", body)
    assert s1 == 201 and s2 == 201
    assert r1 == r2
    assert service.db.count_orders() == 1


def test_body_mismatch_conflict(service: PaymentService) -> None:
    service.create_charge("t1", "key-1", {"amount_cents": 100, "currency": "usd"})
    status, _ = service.create_charge("t1", "key-1", {"amount_cents": 200, "currency": "usd"})
    assert status == 409


def test_concurrent_duplicates_single_order(service: PaymentService) -> None:
    body = {"amount_cents": 999, "currency": "usd"}
    results: list[tuple[int, dict]] = []

    def worker() -> None:
        results.append(service.create_charge("t1", "concurrent", body))

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert service.db.count_orders() == 1
    assert all(r[0] in (201, 409) for r in results)


def test_webhook_dedup(service: PaymentService) -> None:
    event = {"event_id": "evt_123", "type": "payment_intent.succeeded"}
    assert service.process_webhook(event) is True
    assert service.process_webhook(event) is False


def test_fail_closed_when_store_down(service: PaymentService) -> None:
    service.store_available = False
    with pytest.raises(StoreUnavailableError):
        service.create_charge("t1", "k", {"amount_cents": 1, "currency": "usd"})


def test_stripe_mock_idempotent(service: PaymentService) -> None:
    body = {"amount_cents": 100, "currency": "usd"}
    service.create_charge("t1", "stripe-key", body)
    service.create_charge("t1", "stripe-key", body)
    assert service.stripe.intent_count() == 1


def test_api_health_and_charge(service: PaymentService) -> None:
    client = TestClient(create_app(service))
    assert client.get("/health").json()["status"] == "ok"
    resp = client.post(
        "/v1/charges",
        json={"amount_cents": 2500, "currency": "usd"},
        headers={"Idempotency-Key": "api-key-1", "X-Tenant-Id": "demo"},
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "succeeded"


def test_webhook_queue_on_payment(service: PaymentService) -> None:
    body = {"amount_cents": 300, "currency": "usd"}
    service.create_charge("t1", "wh-key", body)
    assert service.webhook_queue.depth() >= 1
    event = service.webhook_queue.consume()
    assert event and event.get("event_id")


def test_api_invalid_body_returns_422(service: PaymentService) -> None:
    client = TestClient(create_app(service))
    resp = client.post(
        "/v1/charges",
        json={"additionalProp1": {}},
        headers={"Idempotency-Key": "bad-body", "X-Tenant-Id": "demo"},
    )
    assert resp.status_code == 422
