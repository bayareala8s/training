"""Tests for Lab 016: Agentic AI Platform."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

LAB_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LAB_ROOT))

from src.api import create_app  # noqa: E402
from src.main import (  # noqa: E402
    AgentRuntime,
    AuditLogger,
    PolicyDecision,
    PolicyEngine,
    ToolCall,
    ToolRegistry,
    ToolSpec,
)
from src.service import AgentPlatformService  # noqa: E402


def test_tool_schema_validation():
    reg = ToolRegistry()
    reg.register(
        ToolSpec(
            "search_kb",
            "Search KB",
            {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            "low",
        )
    )
    assert reg.validate(ToolCall("search_kb", {"query": "raft"})) is True
    assert reg.validate(ToolCall("search_kb", {})) is False


def test_policy_blocks_tool():
    class BlockHigh(PolicyEngine):
        def evaluate(self, tenant_id: str, tool_name: str, risk_level: str) -> PolicyDecision:
            return PolicyDecision.DENY if risk_level == "blocked" else PolicyDecision.ALLOW

    reg = ToolRegistry()
    reg.register(ToolSpec("danger", "Danger", {}, "blocked"))
    runtime = AgentRuntime(reg, BlockHigh(), AuditLogger(), max_steps=5)
    steps = runtime.run("t1", "run danger tool")
    assert any("denied" in s.thought for s in steps)


def test_approval_required():
    reg = ToolRegistry()
    reg.register(
        ToolSpec(
            "delete_data",
            "Delete",
            {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            "high",
        )
    )
    runtime = AgentRuntime(reg, PolicyEngine(), AuditLogger())
    steps = runtime.run("t1", "search delete_data")
    assert any("approval" in s.thought for s in steps)


def test_agent_loop_terminates():
    reg = ToolRegistry()
    reg.register(
        ToolSpec(
            "echo",
            "Echo",
            {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            "low",
            handler=lambda query: query,
        )
    )
    runtime = AgentRuntime(reg, PolicyEngine(), AuditLogger(), max_steps=2, token_budget=50)
    steps = runtime.run("t1", "short")
    assert len(steps) <= 2


def test_audit_log_complete():
    reg = ToolRegistry()
    reg.register(
        ToolSpec(
            "search_kb",
            "Search KB",
            {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            "low",
            handler=lambda query: "ok",
        )
    )
    audit = AuditLogger()
    runtime = AgentRuntime(reg, PolicyEngine(), audit)
    runtime.run("t1", "search docs")
    assert len(audit.events) >= 1
    assert audit.events[0]["tool"] == "search_kb"


def test_tool_registry_register():
    reg = ToolRegistry()
    reg.register(ToolSpec("search_kb", "Search KB", {}, "low"))
    assert reg.get("search_kb") is not None


def test_policy_engine_stub():
    class AllowAll(PolicyEngine):
        def evaluate(self, tenant_id: str, tool_name: str, risk_level: str) -> PolicyDecision:
            return PolicyDecision.ALLOW

    pe = AllowAll()
    assert pe.evaluate("t1", "search_kb", "low") == PolicyDecision.ALLOW


def test_platform_invoke_tool():
    platform = AgentPlatformService()
    result = platform.invoke_tool("t1", "search_kb", {"query": "raft"})
    assert result["allowed"] is True
    assert "raft" in str(result["result"])


def test_api_run_and_list_runs():
    client = TestClient(create_app())
    assert client.get("/health").json()["status"] == "ok"
    run = client.post(
        "/v1/agents/run",
        json={"agent_id": "support-agent", "task": "search docs", "tenant_id": "default"},
    )
    assert run.status_code == 201
    data = run.json()
    assert data["status"] in ("completed", "pending_approval", "denied")
    runs = client.get("/v1/agents/runs").json()
    assert len(runs["runs"]) >= 1


def test_api_tool_invoke_policy():
    client = TestClient(create_app())
    ok = client.post(
        "/v1/tools/invoke",
        json={"tool_name": "search_kb", "tenant_id": "default", "arguments": {"query": "test"}},
    )
    assert ok.json()["allowed"] is True
    blocked = client.post(
        "/v1/tools/invoke",
        json={"tool_name": "send_email", "tenant_id": "default", "arguments": {"query": "hi"}},
    )
    assert blocked.json()["allowed"] is False
    assert blocked.json()["policy"] == "require_approval"
