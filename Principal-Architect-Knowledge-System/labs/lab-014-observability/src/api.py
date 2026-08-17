"""FastAPI HTTP surface for Lab 014."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from .schemas import InjectRequest, SimulateRequest
from .service import ObservabilityService

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 014 — Observability</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #7c3aed; font-size: 1.5rem; }
    .ok { display: inline-block; background: #ede9fe; color: #7c3aed; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #7c3aed; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 014 — Observability</h1>
  <p><span class="ok">running</span> RED metrics, structured logs, trace correlation</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/requests/simulate</code> — generate instrumented request</li>
    <li><code>GET /metrics</code> — Prometheus text exposition</li>
    <li><code>GET /v1/traces</code> — recent correlated log entries</li>
    <li><code>GET /health</code> — service stats</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health</a> · <a href="/metrics">Metrics</a></p>
  <pre>./scripts/demo_observability.sh</pre>
</body>
</html>"""


def create_app(service: ObservabilityService) -> FastAPI:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    app = FastAPI(title="Lab 014 — Observability", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 014 — Observability",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "metrics": "GET /metrics",
                "simulate": "POST /v1/requests/simulate",
                "traces": "GET /v1/traces",
                "inject": "POST /v1/chaos/inject",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", **service.stats()}

    @app.get("/metrics", response_class=PlainTextResponse)
    def metrics() -> str:
        return service.get_metrics_text()

    @app.post("/v1/requests/simulate")
    def simulate_request(body: SimulateRequest) -> dict[str, Any]:
        return service.simulate_request(body.route)

    @app.get("/v1/traces")
    def list_traces(limit: int = Query(default=20, ge=1, le=100)) -> dict[str, Any]:
        traces = service.get_traces(limit)
        return {"count": len(traces), "traces": traces}

    @app.post("/v1/chaos/inject")
    def chaos_inject(body: InjectRequest) -> dict[str, Any]:
        try:
            return service.set_injection(body.inject, body.rate)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return app
