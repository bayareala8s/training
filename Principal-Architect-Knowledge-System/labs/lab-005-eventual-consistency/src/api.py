"""FastAPI HTTP surface for Lab 005."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from .schemas import PartitionRequest, PutKeyRequest
from .service import ConsistencyService

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 005 — Eventual Consistency</title>
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
  <h1>Lab 005 — Eventual Consistency</h1>
  <p><span class="ok">running</span> Multi-replica KV — async replication, version vectors, read repair</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/keys/user:1</code> — write on replica r1</li>
    <li><code>GET /v1/keys/user:1?replica=r2</code> — stale read before replication</li>
    <li><code>POST /v1/replicate/run</code> — deliver pending events</li>
    <li><code>GET /v1/keys/user:1?replica=r2</code> — converged read</li>
    <li><code>POST /v1/chaos/partition</code> — isolate replica during partition</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_consistency.sh</pre>
</body>
</html>"""


def create_app(service: ConsistencyService) -> FastAPI:
    app = FastAPI(title="Lab 005 — Eventual Consistency", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 005 — Eventual Consistency",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "put": "POST /v1/keys/{key}",
                "get": "GET /v1/keys/{key}?replica=r1",
                "replicate": "POST /v1/replicate/run",
                "partition": "POST /v1/chaos/partition",
                "read_repair": "POST /v1/keys/{key}/repair",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", **service.stats()}

    @app.post("/v1/keys/{key}", status_code=201)
    def put_key(key: str, body: PutKeyRequest) -> dict[str, Any]:
        try:
            return service.put_key(key, body.value, body.replica_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/v1/keys/{key}")
    def get_key(
        key: str,
        replica: str = Query(default="r1", examples=["r1"]),
        session_aware: bool = Query(default=False),
    ) -> dict[str, Any]:
        try:
            return service.get_key(key, replica, session_aware=session_aware)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/v1/replicate/run")
    def run_replication() -> dict[str, Any]:
        return service.run_replication()

    @app.post("/v1/chaos/partition")
    def chaos_partition(body: PartitionRequest) -> dict[str, Any]:
        try:
            return service.set_partition(body.replicas, body.enabled)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/keys/{key}/repair")
    def repair_key(key: str) -> dict[str, Any]:
        return service.read_repair_key(key)

    return app
