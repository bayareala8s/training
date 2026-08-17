"""Tests for Lab 008: Idempotent API."""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

LAB_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LAB_ROOT))

from src.api import create_app  # noqa: E402
from src.service import (  # noqa: E402
    IdempotencyRecord,
    IdempotencyStatus,
    IdempotencyStore,
    PaymentService,
    request_hash,
)


@pytest.fixture()
def service() -> PaymentService:
    return PaymentService(IdempotencyStore())


def test_duplicate_post_same_response(service: PaymentService) -> None:
    body = {"amount": 10, "currency": "USD"}
    s1, r1 = service.create_payment("t1", "key-1", body)
    s2, r2 = service.create_payment("t1", "key-1", body)
    assert s1 == 201 and s2 == 201
    assert r1 == r2
    assert service.ledger_count() == 1


def test_concurrent_duplicate(service: PaymentService) -> None:
    body = {"amount": 5, "currency": "USD"}
    results: list[tuple[int, dict]] = []

    def worker() -> None:
        results.append(service.create_payment("t1", "concurrent-key", body))

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert service.ledger_count() == 1
    assert all(r[0] in (201, 409) for r in results)


def test_different_body_same_key(service: PaymentService) -> None:
    service.create_payment("t1", "key-1", {"amount": 10, "currency": "USD"})
    status, _ = service.create_payment("t1", "key-1", {"amount": 20, "currency": "USD"})
    assert status == 409


def test_webhook_dedup(service: PaymentService) -> None:
    assert service.handle_webhook("evt-1", {"type": "paid"}) is True
    assert service.handle_webhook("evt-1", {"type": "paid"}) is False


def test_expired_key_retry() -> None:
    store = IdempotencyStore(ttl_seconds=0.001)
    record = IdempotencyRecord("t1", "k1", "hash", IdempotencyStatus.COMPLETED, 201, b"{}")
    record.expires_at = 0
    store.save(record)
    time.sleep(0.01)
    assert store.lookup("t1", "k1") is None


def test_request_hash_stable() -> None:
    h1 = request_hash({"amount": 10, "currency": "USD"})
    h2 = request_hash({"currency": "USD", "amount": 10})
    assert h1 == h2


def test_store_lookup() -> None:
    store = IdempotencyStore()
    assert store.lookup("t1", "k1") is None


def test_missing_idempotency_key(service: PaymentService) -> None:
    status, body = service.create_payment("t1", "", {"amount": 10, "currency": "USD"})
    assert status == 400
    assert "Idempotency-Key" in body["error"]


def test_api_health_and_payment(service: PaymentService) -> None:
    client = TestClient(create_app(service))
    health = client.get("/health").json()
    assert health["status"] == "ok"
    assert health["ledger_entries"] == 0
    resp = client.post(
        "/v1/payments",
        json={"amount": 25.0, "currency": "USD"},
        headers={"Idempotency-Key": "api-1", "X-Tenant-Id": "demo"},
    )
    assert resp.status_code == 201
    assert resp.json()["payment_id"].startswith("pay-")
    assert client.get("/health").json()["ledger_entries"] == 1


def test_api_idempotent_replay(service: PaymentService) -> None:
    client = TestClient(create_app(service))
    headers = {"Idempotency-Key": "replay-1", "X-Tenant-Id": "demo"}
    body = {"amount": 10.0, "currency": "USD"}
    r1 = client.post("/v1/payments", json=body, headers=headers)
    r2 = client.post("/v1/payments", json=body, headers=headers)
    assert r1.status_code == 201 and r2.status_code == 201
    assert r1.json()["payment_id"] == r2.json()["payment_id"]
    assert service.ledger_count() == 1


def test_api_invalid_body_returns_422(service: PaymentService) -> None:
    client = TestClient(create_app(service))
    resp = client.post(
        "/v1/payments",
        json={"additionalProp1": {}},
        headers={"Idempotency-Key": "bad", "X-Tenant-Id": "demo"},
    )
    assert resp.status_code == 422


def test_api_webhook_endpoint(service: PaymentService) -> None:
    client = TestClient(create_app(service))
    event = {"event_id": "evt-99", "type": "payment.completed"}
    assert client.post("/v1/webhooks", json=event).json()["processed"] is True
    assert client.post("/v1/webhooks", json=event).json()["duplicate"] is True
