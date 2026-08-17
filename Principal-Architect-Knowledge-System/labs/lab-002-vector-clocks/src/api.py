"""FastAPI HTTP surface for Lab 002."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from .schemas import CompareRequest, LocalEventRequest, SendMessageRequest
from .service import ClockService, ProcessNotFoundError

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 002 — Vector Clocks</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #047857; font-size: 1.5rem; }
    .ok { display: inline-block; background: #d1fae5; color: #047857; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #047857; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 002 — Vector Clocks &amp; Causal Ordering</h1>
  <p><span class="ok">running</span> Simulated processes with vector clocks and causal delivery</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>GET /v1/processes</code> — view process clocks (P0, P1 seeded)</li>
    <li><code>POST /v1/events/local</code> — local event increments V[i]</li>
    <li><code>POST /v1/messages/send</code> — send with clock snapshot attached</li>
    <li><code>GET /v1/mailbox/delivered</code> — causally ordered delivery</li>
    <li><code>POST /v1/clocks/compare</code> — before / after / concurrent / equal</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_clocks.sh</pre>
</body>
</html>"""


def create_app(service: ClockService) -> FastAPI:
    app = FastAPI(title="Lab 002 — Vector Clocks", version="1.0.0")

    @app.on_event("startup")
    def _seed() -> None:
        service.seed_demo_processes(2)

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 002 — Vector Clocks",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "processes": "GET /v1/processes",
                "local_event": "POST /v1/events/local",
                "send": "POST /v1/messages/send",
                "delivered": "GET /v1/mailbox/delivered",
                "compare": "POST /v1/clocks/compare",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", **service.stats()}

    @app.get("/v1/processes")
    def list_processes() -> dict[str, Any]:
        return service.list_processes()

    @app.post("/v1/events/local")
    def local_event(body: LocalEventRequest) -> dict[str, Any]:
        try:
            return service.local_event(body.process_id, body.num_processes)
        except ProcessNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/messages/send")
    def send_message(body: SendMessageRequest) -> dict[str, Any]:
        try:
            return service.send_message(
                body.from_process, body.to, body.payload, body.msg_id
            )
        except ProcessNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/v1/mailbox/delivered")
    def delivered() -> dict[str, Any]:
        return service.delivered_messages()

    @app.post("/v1/clocks/compare")
    def compare_clocks(body: CompareRequest) -> dict[str, Any]:
        return service.compare_clocks(body.clock_a, body.clock_b)

    return app
