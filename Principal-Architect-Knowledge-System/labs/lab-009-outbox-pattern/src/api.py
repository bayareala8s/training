"""FastAPI HTTP surface for Lab 009."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .schemas import CreateOrderRequest
from .service import OutboxStack

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 009 — Transactional Outbox</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #1a5f7a; font-size: 1.5rem; }
    .ok { display: inline-block; background: #e6f4ea; color: #137333; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #1a5f7a; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 009 — Transactional Outbox Pattern</h1>
  <p><span class="ok">running</span> Order + outbox commit atomically; relay publishes to in-memory broker (Kafka stand-in)</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/orders</code> — order row + outbox row in one transaction</li>
    <li><code>GET /v1/outbox?pending=true</code> — see unpublished events</li>
    <li><code>POST /v1/relay/run</code> — relay publishes to broker</li>
    <li><code>POST /v1/consumer/run</code> — idempotent inventory update</li>
    <li><code>POST /v1/consumer/run</code> again — duplicates deduped</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_outbox.sh</pre>
</body>
</html>"""


def create_app(stack: OutboxStack) -> FastAPI:
    app = FastAPI(title="Lab 009 — Transactional Outbox", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 009 — Transactional Outbox",
            "status": "running",
            "endpoints": {
                "health": "GET /health",
                "create_order": "POST /v1/orders",
                "outbox": "GET /v1/outbox",
                "relay": "POST /v1/relay/run",
                "broker": "GET /v1/broker",
                "consumer": "POST /v1/consumer/run",
                "docs": "GET /docs",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", **stack.stats()}

    @app.post("/v1/orders", status_code=201)
    def create_order(body: CreateOrderRequest) -> dict[str, Any]:
        try:
            order, event = stack.orders.create_order(body.sku, body.quantity)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            "order": order.to_dict(),
            "outbox_event": event.to_dict(),
            "message": "Order and outbox row committed atomically",
        }

    @app.get("/v1/orders")
    def list_orders() -> dict[str, Any]:
        return {"orders": [o.to_dict() for o in stack.orders.list_orders()]}

    @app.get("/v1/outbox")
    def list_outbox(pending: bool = False) -> dict[str, Any]:
        events = stack.orders.list_outbox(pending_only=pending)
        return {"events": [e.to_dict() for e in events], "pending": pending}

    @app.post("/v1/relay/run")
    def run_relay() -> dict[str, Any]:
        published = stack.relay.run_once()
        return {
            "published": published,
            "broker_messages": len(stack.broker),
            "outbox_pending": stack.db.pending_outbox_count(),
        }

    @app.get("/v1/broker")
    def list_broker() -> dict[str, Any]:
        return {"events": [e.to_dict() for e in stack.broker]}

    @app.post("/v1/consumer/run")
    def run_consumer() -> dict[str, Any]:
        result = stack.consumer.process_broker(stack.broker)
        return result

    return app
