"""Observability service — API/CLI orchestration."""

from __future__ import annotations

import random
from collections import deque
from typing import Any

from .models import MetricsRegistry, RequestContext, TelemetryMiddleware


class ObservabilityService:
    """Instrumented service with metrics, logs, and trace buffer."""

    def __init__(self, trace_buffer_size: int = 100) -> None:
        self.metrics = MetricsRegistry()
        self.traces: deque[dict[str, Any]] = deque(maxlen=trace_buffer_size)
        self.middleware = TelemetryMiddleware(self.metrics, trace_sink=self._record_trace)
        self.error_spike_rate = 0.0
        self.latency_spike_ms = 0.0
        self.simulations_total = 0

    def _record_trace(self, entry: dict[str, Any]) -> None:
        self.traces.appendleft(entry)

    def simulate_request(self, route: str) -> dict[str, Any]:
        import time

        self.simulations_total += 1
        ctx = RequestContext()
        status = "200"
        if self.error_spike_rate > 0 and random.random() < self.error_spike_rate:
            status = "500"
        if self.latency_spike_ms > 0:
            time.sleep(self.latency_spike_ms / 1000.0)
        result = self.middleware.handle(route, ctx, status=status)
        return {
            **result,
            "status": status,
            "trace_id": ctx.trace_id,
            "request_id": ctx.request_id,
        }

    def get_traces(self, limit: int = 20) -> list[dict[str, Any]]:
        return list(self.traces)[:limit]

    def get_metrics_text(self) -> str:
        return self.metrics.prometheus_text()

    def set_injection(self, inject_type: str, rate: float = 0.5) -> dict[str, Any]:
        if inject_type == "error-spike":
            self.error_spike_rate = rate
            self.latency_spike_ms = 0.0
        elif inject_type == "latency-spike":
            self.latency_spike_ms = rate * 1000
            self.error_spike_rate = 0.0
        else:
            raise ValueError(f"unknown injection: {inject_type}")
        return {
            "inject": inject_type,
            "error_spike_rate": self.error_spike_rate,
            "latency_spike_ms": self.latency_spike_ms,
        }

    def stats(self) -> dict[str, Any]:
        return {
            "simulations_total": self.simulations_total,
            "trace_buffer_size": len(self.traces),
            "metric_series": len(self.metrics.requests_total),
            "error_spike_rate": self.error_spike_rate,
            "latency_spike_ms": self.latency_spike_ms,
        }
