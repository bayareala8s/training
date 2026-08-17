"""Tests for Lab 012: Multi-Region AWS."""

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

LAB_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LAB_ROOT))

from src.api import create_app  # noqa: E402
from src.main import LabConfig, load_config, simulate_failover, validate_config  # noqa: E402


def test_terraform_valid():
    pytest.skip("run terraform validate in CI")


def test_config_rto_rpo():
    cfg = LabConfig("us-east-1", "us-west-2", 15, 5, 25, [])
    assert cfg.rto_minutes == 15
    assert cfg.rpo_minutes == 5


def test_health_check_spec():
    health_path = Path("config/health_check.json.example")
    if health_path.exists():
        data = json.loads(health_path.read_text())
        assert data.get("path") == "/health"


def test_cost_tags():
    from src.main import REQUIRED_TAGS

    assert REQUIRED_TAGS["lab"] == "lab-012"
    assert REQUIRED_TAGS["auto_destroy"] == "true"


def test_failover_runbook():
    runbook = Path("runbooks/failover.md")
    if runbook.exists():
        text = runbook.read_text()
        assert "RTO" in text or "failover" in text.lower()
    else:
        pytest.skip("runbooks/failover.md not yet created")


def test_validate_config_example():
    example = Path("config/lab.json.example")
    if not example.exists():
        pytest.skip("config example missing")
    cfg = load_config(example)
    errors = validate_config(cfg)
    assert errors == []


def test_simulate_failover_returns_steps():
    steps = simulate_failover(dry_run=True)
    assert len(steps) == 5
    assert steps[0]["mode"] == "DRY-RUN"


def test_api_health_and_validate():
    client = TestClient(create_app())
    health = client.get("/health").json()
    assert health["status"] == "ok"
    assert health["lab"] == "lab-012"
    resp = client.post("/v1/config/validate", json={"use_example": True})
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is True
    assert data["primary_region"] == "us-east-1"


def test_api_failover_simulate():
    client = TestClient(create_app())
    resp = client.post("/v1/failover/simulate", json={"dry_run": True})
    assert resp.status_code == 200
    data = resp.json()
    assert data["dry_run"] is True
    assert len(data["steps"]) == 5
