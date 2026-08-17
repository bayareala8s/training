"""Tests for Lab 005: Eventual Consistency."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api import create_app
from src.models import Cluster, ReadRepair, Replica, SessionState, VersionVector
from src.service import ConsistencyService


def test_write_propagates_eventually():
    cluster = Cluster(replicas={f"r{i}": Replica(replica_id=f"r{i}") for i in range(1, 4)})
    cluster.replicas["r1"].put("k1", "v1")
    assert cluster.converge()
    for r in cluster.replicas.values():
        assert r.get("k1").value == "v1"


def test_stale_read_without_session():
    cluster = Cluster(replicas={f"r{i}": Replica(replica_id=f"r{i}") for i in range(1, 3)})
    cluster.replicas["r1"].put("k1", "fresh")
    assert cluster.replicas["r2"].get("k1") is None


def test_read_your_writes():
    cluster = Cluster(replicas={f"r{i}": Replica(replica_id=f"r{i}") for i in range(1, 3)})
    session = SessionState(sticky_replica="r1")
    version = cluster.replicas["r1"].put("k1", "v1")
    session.record_write(version, "k1")
    cluster.replicas["r1"].put("k1", "v2")
    session.record_write(cluster.replicas["r1"].get("k1").version, "k1")
    assert session.read_your_writes(cluster.replicas["r1"], "k1").value == "v2"


def test_read_repair():
    r1 = Replica("r1")
    r2 = Replica("r2")
    r1.put("k1", "latest")
    latest = r1.get("k1")
    repairs = ReadRepair().repair("k1", [r1, r2], latest)
    assert repairs >= 1
    assert r2.get("k1").value == "latest"


def test_concurrent_write_conflict():
    r1 = Replica("r1")
    r2 = Replica("r2")
    r1.put("k1", "a")
    r2.put("k1", "b")
    cluster = Cluster(replicas={"r1": r1, "r2": r2})
    cluster.replicate_pending()
    v1 = r1.get("k1").version
    v2 = r2.get("k1").version
    assert v1.concurrent(v2)


def test_replica_stub_get():
    r = Replica(replica_id="r1")
    assert r.get("missing") is None


def test_version_vector_increment():
    vv = VersionVector()
    vv.increment("r1")
    assert vv.values["r1"] == 1


def test_http_put_and_replicate():
    service = ConsistencyService()
    client = TestClient(create_app(service))
    resp = client.post("/v1/keys/user:1", json={"value": "alice", "replica_id": "r1"})
    assert resp.status_code == 201
    stale = client.get("/v1/keys/user:1?replica=r2")
    assert stale.json()["found"] is False
    client.post("/v1/replicate/run")
    converged = client.get("/v1/keys/user:1?replica=r2")
    assert converged.json()["value"] == "alice"


def test_http_partition():
    service = ConsistencyService()
    client = TestClient(create_app(service))
    resp = client.post("/v1/chaos/partition", json={"replicas": ["r3"], "enabled": True})
    assert resp.status_code == 200
    assert "r3" in resp.json()["partitioned"]


def test_swagger_docs():
    service = ConsistencyService()
    client = TestClient(create_app(service))
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200
