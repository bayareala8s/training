"""FastAPI HTTP surface for Lab 006."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from .broker import InMemoryBroker
from .schemas import CreateOrderRequest
from .service import StreamStack

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 006 — Kafka Stream Processing</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #c2410c; font-size: 1.5rem; }
    .ok { display: inline-block; background: #fff7ed; color: #c2410c; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #c2410c; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 006 — Kafka Stream Processing</h1>
  <p><span class="ok">running</span> orders → enricher → windowed metrics; poison messages → DLT</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/orders</code> — produce to <code>orders</code> topic (partition by <code>customer_id</code>)</li>
    <li><code>POST /v1/enricher/run</code> — validate + enrich → <code>orders-enriched</code></li>
    <li><code>POST /v1/aggregator/run</code> — 1-min tumbling windows → <code>order-metrics</code></li>
    <li><code>POST /v1/poison/inject</code> — bad message → DLT</li>
    <li><code>POST /v1/dlt/replay</code> — re-drive DLT messages</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_kafka.sh</pre>
</body>
</html>"""


def create_app(stack: StreamStack) -> FastAPI:
    app = FastAPI(title="Lab 006 — Kafka Stream Processing", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 006 — Kafka Stream Processing",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "produce": "POST /v1/orders",
                "topics": "GET /v1/topics/{topic}",
                "enricher": "POST /v1/enricher/run",
                "aggregator": "POST /v1/aggregator/run",
                "metrics": "GET /v1/metrics",
                "dlt": "GET /v1/dlt",
                "replay": "POST /v1/dlt/replay",
                "poison": "POST /v1/poison/inject",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", **stack.stats()}

    @app.post("/v1/orders", status_code=201)
    def create_order(body: CreateOrderRequest) -> dict[str, Any]:
        return stack.create_order(
            body.customer_id,
            body.amount,
            body.region,
            order_id=body.order_id,
        )

    @app.get("/v1/topics/{topic}")
    def get_topic(topic: str) -> dict[str, Any]:
        if topic not in InMemoryBroker.TOPICS:
            raise HTTPException(status_code=404, detail=f"unknown topic: {topic}")
        return {"topic": topic, "partitions": stack.broker.peek(topic)}

    @app.post("/v1/enricher/run")
    def run_enricher() -> dict[str, Any]:
        return stack.enricher.run_once()

    @app.post("/v1/aggregator/run")
    def run_aggregator() -> dict[str, Any]:
        return stack.aggregator.run_once()

    @app.get("/v1/metrics")
    def list_metrics() -> dict[str, Any]:
        return {"metrics": stack.list_metrics()}

    @app.get("/v1/dlt")
    def list_dlt() -> dict[str, Any]:
        return {"messages": stack.dlt.list_messages()}

    @app.post("/v1/dlt/replay")
    def replay_dlt() -> dict[str, Any]:
        return {"replayed": stack.dlt.replay()}

    @app.post("/v1/poison/inject")
    def inject_poison() -> dict[str, Any]:
        return stack.inject_poison()

    return app
