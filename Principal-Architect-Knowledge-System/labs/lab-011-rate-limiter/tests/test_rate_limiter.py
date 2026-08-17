"""Tests for Lab 011: Distributed Rate Limiter."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api import create_app
from src.models import REDIS, RateLimitMiddleware, SlidingWindowLog, TokenBucket
from src.service import RateLimitService


def setup_function() -> None:
    REDIS.zsets.clear()
    REDIS.available = True


def test_token_bucket_burst():
    bucket = TokenBucket(rate=10.0, burst=5.0)
    assert sum(1 for _ in range(10) if bucket.allow()) == 5


def test_sliding_window_accuracy():
    limiter = SlidingWindowLog("redis://localhost", window_seconds=60.0, limit=3)
    results = [limiter.check("user:1", limit=3).allowed for _ in range(5)]
    assert results == [True, True, True, False, False]


def test_distributed_consistency():
    limiter = SlidingWindowLog("redis://localhost", 60.0, limit=2)
    limiter.check("shared", 2)
    limiter2 = SlidingWindowLog("redis://localhost", 60.0, limit=2)
    result = limiter2.check("shared", 2)
    assert result.remaining == 0


def test_retry_after_header():
    limiter = SlidingWindowLog("redis://localhost", 60.0, limit=2)
    for _ in range(3):
        limiter.check("k", 2)
    result = limiter.check("k", 2)
    assert result.allowed is False
    assert result.retry_after == 60.0


def test_per_tenant_isolation():
    limiter = SlidingWindowLog("redis://localhost", 60.0, limit=1)
    limiter.check("tenant-a", 1)
    result = limiter.check("tenant-b", 1)
    assert result.allowed is True


def test_token_bucket_stub():
    bucket = TokenBucket(rate=10.0, burst=20.0)
    assert bucket.rate == 10.0


def test_middleware_local_deny():
    bucket = TokenBucket(rate=0.1, burst=1.0)
    limiter = SlidingWindowLog("redis://localhost", 60.0, limit=100)
    mw = RateLimitMiddleware(bucket, limiter)
    assert mw.check("t1", "/api").allowed is True
    assert mw.check("t1", "/api").allowed is False


def test_http_check():
    service = RateLimitService()
    client = TestClient(create_app(service))
    resp = client.post("/v1/check", json={"tenant_id": "tenant-1", "route": "/api"})
    assert resp.status_code == 200
    assert resp.json()["allowed"] is True
    assert "X-RateLimit-Limit" in resp.headers


def test_http_redis_down_fail_closed():
    service = RateLimitService()
    client = TestClient(create_app(service))
    client.post("/v1/chaos/redis-down", json={"enabled": True, "mode": "fail-closed"})
    resp = client.post("/v1/check", json={"tenant_id": "tenant-1", "route": "/api"})
    assert resp.status_code == 429
    assert resp.json()["allowed"] is False


def test_swagger_docs():
    service = RateLimitService()
    client = TestClient(create_app(service))
    assert client.get("/docs").status_code == 200
    assert client.get("/health").json()["status"] == "ok"
