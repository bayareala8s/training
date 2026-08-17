"""Tests for Lab 002: Vector Clocks."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api import create_app
from src.clocks import (
    CausalMailbox,
    Message,
    Process,
    Relation,
    VectorClock,
    VersionVector,
    compare,
)
from src.service import ClockService


def test_increment_local():
    vc = VectorClock(size=3)
    vc.increment(0)
    assert vc.values == [1, 0, 0]


def test_merge_on_receive():
    vc = VectorClock(size=2, values=[2, 1])
    other = VectorClock(size=2, values=[1, 3])
    vc.merge(other)
    vc.increment(0)
    assert vc.values[0] == 3
    assert vc.values[1] == 3


def test_compare_before():
    a = VectorClock(size=2, values=[1, 1])
    b = VectorClock(size=2, values=[2, 2])
    assert compare(a, b) == Relation.BEFORE
    assert compare(b, a) == Relation.AFTER


def test_compare_concurrent():
    a = VectorClock(size=2, values=[2, 0])
    b = VectorClock(size=2, values=[0, 2])
    assert compare(a, b) == Relation.CONCURRENT


def test_causal_delivery():
    c0 = VectorClock(size=2, values=[1, 0])
    c1 = VectorClock(size=2, values=[2, 1])
    m1 = Message("m1", 0, "hello", c0)
    m2 = Message("m2", 1, "world", c1)
    mailbox = CausalMailbox()
    mailbox.submit(m2)
    mailbox.submit(m1)
    delivered = mailbox.delivered
    assert [m.msg_id for m in delivered] == ["m1", "m2"]


def test_sibling_detection():
    VersionVector({"R1": 1})
    VersionVector({"R2": 1})
    a = VectorClock(size=2, values=[1, 0])
    b = VectorClock(size=2, values=[0, 1])
    assert compare(a, b) == Relation.CONCURRENT


def test_service_send_and_deliver():
    service = ClockService()
    service.seed_demo_processes(2)
    result = service.send_message(0, 1, "hello", "m1")
    assert result["msg_id"] == "m1"
    assert result["clock"] == [1, 0]
    delivered = service.delivered_messages()
    assert delivered["delivered"][0]["msg_id"] == "m1"


def test_http_local_event():
    service = ClockService()
    service.seed_demo_processes(2)
    client = TestClient(create_app(service))
    resp = client.post("/v1/events/local", json={"process_id": 0, "num_processes": 2})
    assert resp.status_code == 200
    assert resp.json()["clock"] == [1, 0]


def test_http_send_and_mailbox():
    service = ClockService()
    service.seed_demo_processes(2)
    client = TestClient(create_app(service))
    resp = client.post(
        "/v1/messages/send",
        json={"from": 0, "to": 1, "payload": "hello", "msg_id": "m1"},
    )
    assert resp.status_code == 200
    delivered = client.get("/v1/mailbox/delivered")
    assert delivered.status_code == 200
    assert delivered.json()["delivered"][0]["msg_id"] == "m1"


def test_http_compare():
    service = ClockService()
    client = TestClient(create_app(service))
    resp = client.post(
        "/v1/clocks/compare",
        json={"clock_a": [1, 1], "clock_b": [2, 2]},
    )
    assert resp.status_code == 200
    assert resp.json()["relation"] == "before"


def test_http_processes():
    service = ClockService()
    with TestClient(create_app(service)) as client:
        resp = client.get("/v1/processes")
        assert resp.status_code == 200
        assert resp.json()["num_processes"] == 2


def test_swagger_docs():
    service = ClockService()
    client = TestClient(create_app(service))
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200
