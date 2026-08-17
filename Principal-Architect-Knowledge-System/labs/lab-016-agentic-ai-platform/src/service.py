"""Agent platform service layer."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from .main import (
    AgentRuntime,
    AgentStep,
    AuditLogger,
    PolicyDecision,
    PolicyEngine,
    ToolCall,
    ToolRegistry,
    ToolSpec,
)


def _default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            "search_kb",
            "Search KB",
            {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            "low",
            handler=lambda query: f"results for {query}",
        )
    )
    registry.register(
        ToolSpec(
            "create_ticket",
            "Create ticket",
            {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
            "medium",
            handler=lambda query: f"ticket created for {query}",
        )
    )
    registry.register(
        ToolSpec(
            "send_email",
            "Send email",
            {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            "high",
            handler=lambda query: f"email sent for {query}",
        )
    )
    return registry


@dataclass
class AgentRunRecord:
    run_id: str
    agent_id: str
    tenant_id: str
    task: str
    status: str
    steps: list[AgentStep]


@dataclass
class AgentPlatformService:
    registry: ToolRegistry = field(default_factory=_default_registry)
    policy: PolicyEngine = field(default_factory=PolicyEngine)
    audit: AuditLogger = field(default_factory=AuditLogger)
    runs: list[AgentRunRecord] = field(default_factory=list)

    def _runtime(self) -> AgentRuntime:
        return AgentRuntime(self.registry, self.policy, self.audit)

    def run_agent(self, agent_id: str, tenant_id: str, task: str) -> AgentRunRecord:
        runtime = self._runtime()
        steps = runtime.run(tenant_id, task)
        status = "completed"
        if steps and "approval" in steps[-1].thought:
            status = "pending_approval"
        elif steps and "denied" in steps[-1].thought:
            status = "denied"
        record = AgentRunRecord(
            run_id=str(uuid.uuid4()),
            agent_id=agent_id,
            tenant_id=tenant_id,
            task=task,
            status=status,
            steps=steps,
        )
        self.runs.append(record)
        return record

    def list_runs(self) -> list[AgentRunRecord]:
        return list(self.runs)

    def invoke_tool(self, tenant_id: str, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        spec = self.registry.get(tool_name)
        if spec is None:
            return {
                "tool_name": tool_name,
                "allowed": False,
                "policy": "deny",
                "error": "tool not found",
            }
        decision = self.policy.evaluate(tenant_id, tool_name, spec.risk_level)
        if decision == PolicyDecision.DENY:
            return {
                "tool_name": tool_name,
                "allowed": False,
                "policy": decision.value,
                "error": "policy denied",
            }
        if decision == PolicyDecision.REQUIRE_APPROVAL:
            return {
                "tool_name": tool_name,
                "allowed": False,
                "policy": decision.value,
                "error": "approval required",
            }
        call = ToolCall(tool_name, arguments)
        if not self.registry.validate(call):
            return {
                "tool_name": tool_name,
                "allowed": False,
                "policy": "deny",
                "error": "invalid arguments",
            }
        result = spec.handler(**call.arguments) if spec.handler else "ok"
        self.audit.log({"tenant": tenant_id, "tool": tool_name, "args": arguments})
        return {
            "tool_name": tool_name,
            "allowed": True,
            "policy": decision.value,
            "result": result,
        }

    def stats(self) -> dict[str, Any]:
        return {
            "runs": len(self.runs),
            "tools_registered": len(self.registry._tools),
            "audit_events": len(self.audit.events),
        }
