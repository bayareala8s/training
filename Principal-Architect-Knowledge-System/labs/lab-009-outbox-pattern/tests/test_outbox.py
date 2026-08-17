"""Tests for Lab 009: Transactional Outbox."""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

LAB_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LAB_ROOT))

from src.api import create_app  # noqa: E402
from src.models import Order, OutboxEvent  # noqa: E402
from src.service import (  # noqa: E402
    InventoryConsumer,
    OrderService,
    OutboxRelay,
    OutboxStack,
)
from src.store import InMemoryDB  # noqa: E402


@pytest.fixture()
def stack() -> OutboxStack:
    return OutboxStack()


def test_atomic_order_outbox() -> None:
    db = InMemoryDB()
    svc = OrderService(db)
    order, event = svc.create_order("SKU-1", 2)
    assert order.order_id in db.orders
    assert event.id in db.outbox


def test_relay_publishes() -> None:
    db = InMemoryDB()
    broker: list[OutboxEvent] = []
    relay = OutboxRelay(db, broker)
    event = OutboxEvent("e1", "ord-1", "OrderCreated", {})
    db.outbox["e1"] = event
    assert relay.run_once() == 1
    assert len(broker) == 1
    assert db.outbox["e1"].published_at is not None


def test_relay_crash_safe() -> None:
    db = InMemoryDB()
    broker: list[OutboxEvent] = []
    relay = OutboxRelay(db, broker)
    db.outbox["e1"] = OutboxEvent("e1", "ord-1", "OrderCreated", {})
    relay.publish(db.outbox["e1"])
    relay2 = OutboxRelay(db, broker)
    assert relay2.run_once() == 1


def test_duplicate_publish_safe() -> None:
    consumer = InventoryConsumer()
    event = OutboxEvent("e1", "ord-1", "OrderCreated", {"sku": "X", "quantity": 1})
    assert consumer.handle(event) is True
    assert consumer.handle(event) is False


def test_ordering_per_aggregate() -> None:
    db = InMemoryDB()
    broker: list[OutboxEvent] = []
    relay = OutboxRelay(db, broker)
    e1 = OutboxEvent("e1", "ord-1", "OrderCreated", {})
    e2 = OutboxEvent("e2", "ord-1", "OrderShipped", {})
    db.outbox["e2"] = e2
    db.outbox["e1"] = e1
    batch = relay.poll_batch()
    assert [e.event_type for e in batch] == ["OrderCreated", "OrderShipped"]


def test_outbox_event_model() -> None:
    evt = OutboxEvent("e1", "ord-1", "OrderCreated", {"sku": "X"})
    assert evt.published_at is None
    assert evt.aggregate_id == "ord-1"


def test_api_create_and_relay_flow(stack: OutboxStack) -> None:
    client = TestClient(create_app(stack))
    assert client.get("/health").json()["status"] == "ok"
    resp = client.post("/v1/orders", json={"sku": "API-SKU", "quantity": 1})
    assert resp.status_code == 201
    assert client.get("/health").json()["outbox_pending"] == 1
    relay = client.post("/v1/relay/run")
    assert relay.json()["published"] == 1
    assert client.get("/health").json()["outbox_pending"] == 0
    c1 = client.post("/v1/consumer/run").json()
    c2 = client.post("/v1/consumer/run").json()
    assert c1["processed"] >= 1
    assert c2["duplicates"] >= 1


def test_demo_end_to_end(stack: OutboxStack) -> None:
    order, event = stack.orders.create_order("DEMO", 5)
    assert stack.db.pending_outbox_count() == 1
    assert stack.relay.run_once() == 1
    assert stack.db.pending_outbox_count() == 0
    r = stack.consumer.process_broker(stack.broker)
    assert r["inventory"]["DEMO"] == 5
    assert stack.consumer.process_broker(stack.broker)["duplicates"] == 1
