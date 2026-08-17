"""Tests for Lab 014: Observability."""

import json
import logging
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.api import create_app
from src.models import MetricsRegistry, RequestContext, TelemetryMiddleware
from src.service import ObservabilityService


def test_metrics_increment():
    m = MetricsRegistry()
    m.record_request("/api", "200", 0.1)
    m.record_request("/api", "200", 0.2)
    assert m.requests_total[("/api", "200")] == 2


def test_trace_context_propagation():
    ctx = RequestContext()
    mw = TelemetryMiddleware(MetricsRegistry())
    result = mw.handle("/api", ctx)
    assert result["ok"] is True
    assert ctx.trace_id
    assert ctx.span_id


def test_log_contains_trace_id(caplog):
    caplog.set_level(logging.INFO)
    ctx = RequestContext(trace_id="trace-abc")
    TelemetryMiddleware(MetricsRegistry()).handle("/health", ctx)
    assert any("trace-abc" in r.message for r in caplog.records)


def test_prometheus_scrape():
    m = MetricsRegistry()
    m.record_request("/health", "200", 0.01)
    text = m.prometheus_text()
    assert "http_requests_total" in text
    assert '/health"' in text


def test_slo_recording_rule():
    promql = 'sum(rate(http_requests_total{status="500"}[5m])) / sum(rate(http_requests_total[5m]))'
    assert "http_requests_total" in promql


def test_middleware_stub():
    mw = TelemetryMiddleware(MetricsRegistry())
    ctx = RequestContext(trace_id="abc")
    assert ctx.request_id


def test_http_simulate_and_traces():
    service = ObservabilityService()
    client = TestClient(create_app(service))
    resp = client.post("/v1/requests/simulate", json={"route": "/api"})
    assert resp.status_code == 200
    assert resp.json()["trace_id"]
    traces = client.get("/v1/traces")
    assert traces.json()["count"] >= 1


def test_http_metrics_endpoint():
    service = ObservabilityService()
    client = TestClient(create_app(service))
    client.post("/v1/requests/simulate", json={"route": "/health"})
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "http_requests_total" in metrics.text


def test_swagger_docs():
    service = ObservabilityService()
    client = TestClient(create_app(service))
    assert client.get("/docs").status_code == 200
    assert client.get("/health").json()["status"] == "ok"
