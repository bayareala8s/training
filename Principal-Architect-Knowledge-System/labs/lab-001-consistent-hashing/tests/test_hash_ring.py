"""Tests for Lab 001: Consistent Hashing Ring."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api import create_app
from src.ring import HashRing, RingEmptyError, hash_position, modulo_node, redistribution_ratio
from src.service import RingService


def test_hash_position_stable():
    assert hash_position("user:42") == hash_position("user:42")
    assert hash_position("a") != hash_position("b")


def test_empty_ring_raises():
    ring = HashRing()
    with pytest.raises(RingEmptyError):
        ring.get_node("any-key")


def test_single_node_all_keys_same_owner():
    ring = HashRing()
    ring.add_node("only-node", vnode_count=32)
    keys = [f"k:{i}" for i in range(100)]
    owners = {ring.get_node(k) for k in keys}
    assert owners == {"only-node"}


def test_add_remove_idempotent():
    ring = HashRing()
    ring.add_node("node-a", vnode_count=16)
    size_after_first = len(ring._ring)
    ring.add_node("node-a", vnode_count=16)
    assert len(ring._ring) == size_after_first


def test_removal_redistributes_minimally():
    ring = HashRing()
    for n in ("a", "b", "c", "d", "e"):
        ring.add_node(n, vnode_count=128)
    keys = [f"key:{i}" for i in range(10_000)]
    before = {k: ring.get_node(k) for k in keys}
    ring.remove_node("c")
    after = {k: ring.get_node(k) for k in keys}
    moved = sum(1 for k in keys if before[k] != after[k])
    assert moved / len(keys) < 0.30


def test_vnode_load_balance():
    ring = HashRing()
    for i in range(10):
        ring.add_node(f"node-{i}", vnode_count=128)
    counts: dict[str, int] = {}
    for i in range(100_000):
        node = ring.get_node(f"item:{i}")
        counts[node] = counts.get(node, 0) + 1
    mean = 100_000 / 10
    variance = sum((c - mean) ** 2 for c in counts.values()) / 10
    cv = (variance**0.5) / mean
    assert cv < 0.15


def test_modulo_vs_consistent_churn():
    keys = [f"k:{i}" for i in range(5_000)]
    ring_before = HashRing()
    for n in range(5):
        ring_before.add_node(f"n{n}", vnode_count=64)
    ring_after = HashRing()
    for n in range(6):
        ring_after.add_node(f"n{n}", vnode_count=64)
    consistent_churn = redistribution_ratio(keys, ring_before, ring_after)
    modulo_before = {k: modulo_node(k, 5) for k in keys}
    modulo_after = {k: modulo_node(k, 6) for k in keys}
    modulo_churn = sum(1 for k in keys if modulo_before[k] != modulo_after[k]) / len(keys)
    assert consistent_churn < modulo_churn


def test_http_lookup():
    service = RingService()
    service.seed_demo_cluster()
    client = TestClient(create_app(service))
    resp = client.get("/v1/lookup/user:42")
    assert resp.status_code == 200
    assert "node" in resp.json()


def test_http_churn_simulation():
    service = RingService()
    service.seed_demo_cluster()
    client = TestClient(create_app(service))
    resp = client.post("/v1/simulate/churn", json={"key_count": 5000})
    assert resp.status_code == 200
    assert resp.json()["consistent_wins"] is True


def test_swagger_docs():
    service = RingService()
    client = TestClient(create_app(service))
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200
