"""FastAPI HTTP surface for Lab 012."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from .main import REQUIRED_TAGS, LabConfig, load_config, simulate_failover, validate_config
from .schemas import (
    ConfigValidateRequest,
    ConfigValidateResponse,
    FailoverSimulateRequest,
    FailoverSimulateResponse,
    FailoverStep,
    LabConfigSchema,
)

_LAB_ROOT = Path(__file__).resolve().parent.parent
_EXAMPLE_CONFIG = _LAB_ROOT / "config" / "lab.json.example"

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 012 — Multi-Region AWS</title>
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
  <h1>Lab 012 — Multi-Region AWS</h1>
  <p><span class="ok">running</span> Active-passive DR — config validation and failover simulation</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/config/validate</code> — validate lab config (body or example)</li>
    <li><code>POST /v1/failover/simulate</code> — dry-run regional failover steps</li>
    <li><code>GET /health</code> — service and region summary</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health</a></p>
  <pre>./scripts/demo_multiregion.sh</pre>
</body>
</html>"""


def _schema_to_lab_config(schema: LabConfigSchema) -> LabConfig:
    from .main import RegionConfig

    regions = [
        RegionConfig(r.name, r.vpc_cidr, r.is_primary) for r in schema.regions
    ]
    return LabConfig(
        primary_region=schema.primary_region,
        dr_region=schema.dr_region,
        rto_minutes=schema.rto_minutes,
        rpo_minutes=schema.rpo_minutes,
        budget_usd=schema.budget_usd,
        regions=regions,
    )


def create_app() -> FastAPI:
    app = FastAPI(title="Lab 012 — Multi-Region AWS", version="1.0.0")
    cached_cfg: LabConfig | None = None

    if _EXAMPLE_CONFIG.exists():
        cached_cfg = load_config(_EXAMPLE_CONFIG)

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 012 — Multi-Region AWS",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "validate": "POST /v1/config/validate",
                "failover": "POST /v1/failover/simulate",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "lab": "lab-012",
            "primary_region": cached_cfg.primary_region if cached_cfg else None,
            "dr_region": cached_cfg.dr_region if cached_cfg else None,
            "required_tags": REQUIRED_TAGS,
        }

    @app.post("/v1/config/validate")
    def validate(body: ConfigValidateRequest) -> ConfigValidateResponse:
        if body.use_example:
            if not _EXAMPLE_CONFIG.exists():
                raise HTTPException(status_code=404, detail="example config not found")
            cfg = load_config(_EXAMPLE_CONFIG)
        elif body.config is not None:
            cfg = _schema_to_lab_config(body.config)
        else:
            if not _EXAMPLE_CONFIG.exists():
                raise HTTPException(
                    status_code=400,
                    detail="provide config body or set use_example=true",
                )
            cfg = load_config(_EXAMPLE_CONFIG)

        errors = validate_config(cfg)
        return ConfigValidateResponse(
            valid=len(errors) == 0,
            errors=errors,
            primary_region=cfg.primary_region,
            dr_region=cfg.dr_region,
            required_tags=REQUIRED_TAGS,
        )

    @app.post("/v1/failover/simulate")
    def failover_simulate(body: FailoverSimulateRequest) -> FailoverSimulateResponse:
        raw_steps = simulate_failover(dry_run=body.dry_run)
        steps = [
            FailoverStep(step=s["step"], action=s["action"], mode=s["mode"])
            for s in raw_steps
        ]
        return FailoverSimulateResponse(dry_run=body.dry_run, steps=steps)

    return app
