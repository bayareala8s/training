"""FastAPI HTTP surface for Lab 001."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from .ring import RingEmptyError
from .schemas import AddNodeRequest, LookupRequest, NodeFailureRequest, SimulationRequest
from .service import RingService

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 001 — Consistent Hashing Ring</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #1d4ed8; font-size: 1.5rem; }
    .ok { display: inline-block; background: #dbeafe; color: #1d4ed8; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #1d4ed8; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 001 — Consistent Hashing Ring</h1>
  <p><span class="ok">running</span> Virtual-node hash ring — minimal key churn on node add/remove</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/nodes</code> — add nodes with vnodes (128 each)</li>
    <li><code>GET /v1/lookup/user:42</code> — resolve key → owning node</li>
    <li><code>POST /v1/simulate/balance</code> — load distribution across nodes</li>
    <li><code>POST /v1/simulate/churn</code> — consistent vs modulo hashing</li>
    <li><code>POST /v1/simulate/node-failure</code> — keys redistributed on remove</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_ring.sh</pre>
</body>
</html>"""


def create_app(service: RingService) -> FastAPI:
    app = FastAPI(title="Lab 001 — Consistent Hashing Ring", version="1.0.0")

    @app.on_event("startup")
    def _seed() -> None:
        service.seed_demo_cluster()

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 001 — Consistent Hashing Ring",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "nodes": "GET/POST /v1/nodes",
                "lookup": "GET /v1/lookup/{key}",
                "balance": "POST /v1/simulate/balance",
                "churn": "POST /v1/simulate/churn",
                "node_failure": "POST /v1/simulate/node-failure",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", **service.stats()}

    @app.get("/v1/nodes")
    def list_nodes() -> dict[str, Any]:
        return service.stats()

    @app.post("/v1/nodes", status_code=201)
    def add_node(body: AddNodeRequest) -> dict[str, Any]:
        return service.add_node(body.node_id, body.vnode_count)

    @app.delete("/v1/nodes/{node_id}")
    def remove_node(node_id: str) -> dict[str, Any]:
        try:
            return service.remove_node(node_id)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/v1/lookup/{key}")
    def lookup_key(key: str) -> dict[str, Any]:
        try:
            return service.lookup(key)
        except RingEmptyError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.post("/v1/lookup")
    def lookup_body(body: LookupRequest) -> dict[str, Any]:
        try:
            return service.lookup(body.key)
        except RingEmptyError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.post("/v1/simulate/balance")
    def simulate_balance(body: SimulationRequest) -> dict[str, Any]:
        try:
            return service.balance_stats(body.key_count)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/simulate/churn")
    def simulate_churn(body: SimulationRequest) -> dict[str, Any]:
        try:
            return service.compare_churn(body.key_count)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/simulate/node-failure")
    def simulate_node_failure(body: NodeFailureRequest) -> dict[str, Any]:
        try:
            return service.node_failure_simulation(body.node_id, body.key_count)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app
