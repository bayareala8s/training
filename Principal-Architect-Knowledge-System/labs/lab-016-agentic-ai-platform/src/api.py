"""FastAPI HTTP surface for Lab 016."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from .schemas import (
    AgentRunRequest,
    AgentRunResponse,
    AgentRunSummary,
    AgentRunsListResponse,
    AgentStepResponse,
    ToolInvokeRequest,
    ToolInvokeResponse,
)
from .service import AgentPlatformService

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 016 — Agentic AI Platform</title>
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
  <h1>Lab 016 — Agentic AI Platform</h1>
  <p><span class="ok">running</span> Agent runtime — tool registry, policy engine, audit log</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/agents/run</code> — run agent task with tool loop</li>
    <li><code>GET /v1/agents/runs</code> — list agent run history</li>
    <li><code>POST /v1/tools/invoke</code> — invoke tool with policy check</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health</a></p>
  <pre>./scripts/demo_agent.sh</pre>
</body>
</html>"""


def create_app(service: AgentPlatformService | None = None) -> FastAPI:
    platform = service or AgentPlatformService()
    app = FastAPI(title="Lab 016 — Agentic AI Platform", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 016 — Agentic AI Platform",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "run": "POST /v1/agents/run",
                "runs": "GET /v1/agents/runs",
                "invoke": "POST /v1/tools/invoke",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "lab": "lab-016", **platform.stats()}

    @app.post("/v1/agents/run", status_code=201)
    def run_agent(body: AgentRunRequest) -> AgentRunResponse:
        record = platform.run_agent(body.agent_id, body.tenant_id, body.task)
        steps = [
            AgentStepResponse(
                step_index=s.step_index,
                thought=s.thought,
                tool_name=s.tool_call.tool_name if s.tool_call else None,
                result=s.result,
            )
            for s in record.steps
        ]
        return AgentRunResponse(
            run_id=record.run_id,
            agent_id=record.agent_id,
            tenant_id=record.tenant_id,
            task=record.task,
            status=record.status,
            steps=steps,
        )

    @app.get("/v1/agents/runs")
    def list_runs() -> AgentRunsListResponse:
        runs = [
            AgentRunSummary(
                run_id=r.run_id,
                agent_id=r.agent_id,
                tenant_id=r.tenant_id,
                task=r.task,
                status=r.status,
                step_count=len(r.steps),
            )
            for r in platform.list_runs()
        ]
        return AgentRunsListResponse(runs=runs)

    @app.post("/v1/tools/invoke")
    def invoke_tool(body: ToolInvokeRequest) -> ToolInvokeResponse:
        result = platform.invoke_tool(body.tenant_id, body.tool_name, body.arguments)
        return ToolInvokeResponse(**result)

    return app
