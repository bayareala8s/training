"""Observability models — metrics, tracing, middleware."""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class RequestContext:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    span_id: str = ""

    def ensure_trace(self) -> None:
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())
        if not self.span_id:
            self.span_id = str(uuid.uuid4())[:16]


class MetricsRegistry:
    def __init__(self) -> None:
        self.requests_total: dict[tuple[str, str], int] = {}
        self.duration_histogram: dict[str, list[float]] = {}

    def record_request(self, route: str, status: str, duration_s: float) -> None:
        key = (route, status)
        self.requests_total[key] = self.requests_total.get(key, 0) + 1
        self.duration_histogram.setdefault(route, []).append(duration_s)

    def prometheus_text(self) -> str:
        lines = [
            "# HELP http_requests_total Total HTTP requests",
            "# TYPE http_requests_total counter",
        ]
        for (route, status), count in sorted(self.requests_total.items()):
            lines.append(f'http_requests_total{{route="{route}",status="{status}"}} {count}')
        lines.extend([
            "# HELP http_request_duration_seconds Request duration histogram samples",
            "# TYPE http_request_duration_seconds gauge",
        ])
        for route, durations in sorted(self.duration_histogram.items()):
            if durations:
                lines.append(
                    f'http_request_duration_seconds{{route="{route}"}} {durations[-1]:.6f}'
                )
        return "\n".join(lines) + "\n"


class TelemetryMiddleware:
    def __init__(
        self,
        metrics: MetricsRegistry,
        trace_sink: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        self.metrics = metrics
        self.logger = logging.getLogger("lab-014")
        self.trace_sink = trace_sink

    def handle(self, route: str, ctx: RequestContext, status: str = "200") -> dict[str, Any]:
        ctx.ensure_trace()
        start = time.monotonic()
        try:
            result: dict[str, Any] = {"route": route, "ok": status == "200"}
        finally:
            duration = time.monotonic() - start
            self.metrics.record_request(route, status, duration)
            entry = {
                "trace_id": ctx.trace_id,
                "span_id": ctx.span_id,
                "request_id": ctx.request_id,
                "route": route,
                "status": status,
                "duration_ms": round(duration * 1000, 2),
            }
            self.logger.info(json.dumps(entry))
            if self.trace_sink:
                self.trace_sink(entry)
        return result
