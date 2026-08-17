"""Tests for Lab 006: Kafka Stream Processing."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api import create_app
from src.broker import InMemoryBroker
from src.models import Order
from src.service import (
    DLTHandler,
    EnricherConsumer,
    OrderProducer,
    StreamStack,
    WindowAggregator,
)


@pytest.fixture
def stack() -> StreamStack:
    return StreamStack()


def test_producer_partition_routing(stack: StreamStack) -> None:
    stack.create_order("cust-1", 10.0, "us", order_id="o1")
    stack.create_order("cust-1", 20.0, "us", order_id="o2")
    partition = stack.broker.partition_for("cust-1")
    assert len(stack.broker.topics["orders"][partition]) == 2


def test_consumer_at_least_once(stack: StreamStack) -> None:
    stack.create_order("c1", 10.0, "eu", order_id="o1")
    assert stack.enricher.run_once()["enriched"] == 1
    assert stack.enricher.run_once()["enriched"] == 0


def test_windowed_aggregate(stack: StreamStack) -> None:
    import time

    agg = WindowAggregator(stack.broker)
    now = time.time()
    m = agg.aggregate({"event_time": now, "region": "us", "amount": 50.0})
    assert m.count == 1
    assert m.revenue == 50.0
    agg.aggregate({"event_time": now, "region": "us", "amount": 25.0})
    assert agg.windows[(m.window_start, "us")].count == 2


def test_dlt_on_poison_message(stack: StreamStack) -> None:
    stack.inject_poison()
    stack.enricher.run_once()
    assert len(stack.broker.dlt) == 1


def test_replay_dlt(stack: StreamStack) -> None:
    DLTHandler(stack.broker).send_to_dlt(
        '{"order_id":"o1","customer_id":"c1","amount":1,"region":"us","event_time":1}',
        "err",
    )
    assert stack.dlt.replay() == 1


def test_order_model() -> None:
    o = Order("o1", "c1", 10.0, "eu")
    assert o.order_id == "o1"
    assert o.amount == 10.0


def test_http_pipeline(stack: StreamStack) -> None:
    client = TestClient(create_app(stack))
    resp = client.post(
        "/v1/orders",
        json={"customer_id": "cust-99", "amount": 42.0, "region": "eu"},
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "produced"
    assert client.post("/v1/enricher/run").json()["enriched"] == 1
    assert client.post("/v1/aggregator/run").json()["metrics_emitted"] == 1
    assert client.get("/health").status_code == 200


def test_swagger_docs(stack: StreamStack) -> None:
    client = TestClient(create_app(stack))
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200
