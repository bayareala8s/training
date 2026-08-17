#!/usr/bin/env python3
"""Lab 016: Agentic AI Platform — runtime."""

from __future__ import annotations

import argparse
import enum
from dataclasses import dataclass, field
from typing import Any, Callable


class PolicyDecision(enum.Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters_schema: dict[str, Any]
    risk_level: str
    handler: Callable[..., Any] | None = None


@dataclass
class ToolCall:
    tool_name: str
    arguments: dict[str, Any]


@dataclass
class AgentStep:
    step_index: int
    thought: str
    tool_call: ToolCall | None = None
    result: Any = None


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def validate(self, call: ToolCall) -> bool:
        spec = self.get(call.tool_name)
        if spec is None:
            return False
        required = spec.parameters_schema.get("required", [])
        props = spec.parameters_schema.get("properties", {})
        for key in required:
            if key not in call.arguments:
                return False
        for key, value in call.arguments.items():
            if key in props:
                expected = props[key].get("type")
                if expected == "string" and not isinstance(value, str):
                    return False
                if expected == "integer" and not isinstance(value, int):
                    return False
        return True


class PolicyEngine:
    def evaluate(self, tenant_id: str, tool_name: str, risk_level: str) -> PolicyDecision:
        if risk_level == "high":
            return PolicyDecision.REQUIRE_APPROVAL
        if risk_level == "blocked":
            return PolicyDecision.DENY
        return PolicyDecision.ALLOW


@dataclass
class AuditLogger:
    events: list[dict[str, Any]] = field(default_factory=list)

    def log(self, event: dict[str, Any]) -> None:
        self.events.append(event)


@dataclass
class AgentRuntime:
    registry: ToolRegistry
    policy: PolicyEngine
    audit: AuditLogger
    max_steps: int = 10
    token_budget: int = 8000
    approved_tools: set[str] = field(default_factory=set)

    def run(self, tenant_id: str, task: str) -> list[AgentStep]:
        steps: list[AgentStep] = []
        tokens_used = len(task)
        task_lower = task.lower()
        planned_tools = [name for name in self.registry._tools if name in task_lower]
        if not planned_tools:
            planned_tools = ["search_kb"] if "search" in task_lower else list(self.registry._tools.keys())[:1]
        for i, tool_name in enumerate(planned_tools):
            if i >= self.max_steps or tokens_used >= self.token_budget:
                break
            spec = self.registry.get(tool_name)
            if spec is None:
                break
            decision = self.policy.evaluate(tenant_id, tool_name, spec.risk_level)
            if decision == PolicyDecision.DENY:
                steps.append(AgentStep(i, f"denied {tool_name}"))
                break
            if decision == PolicyDecision.REQUIRE_APPROVAL and tool_name not in self.approved_tools:
                steps.append(AgentStep(i, f"approval required for {tool_name}"))
                break
            call = ToolCall(tool_name, {"query": task})
            if not self.registry.validate(call):
                break
            result = spec.handler(**call.arguments) if spec.handler else "ok"
            self.audit.log({"tenant": tenant_id, "tool": tool_name, "args": call.arguments})
            tokens_used += 100
            steps.append(AgentStep(i, f"invoke {tool_name}", call, result))
        return steps


def run_agent(agent_id: str, task: str) -> None:
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
    runtime = AgentRuntime(registry, PolicyEngine(), AuditLogger())
    steps = runtime.run("default", task)
    print(f"Agent {agent_id} completed {len(steps)} steps")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab 016: Agentic AI Platform")
    parser.add_argument("--agent", default="support-agent")
    parser.add_argument("--task", type=str)
    parser.add_argument("--inject", choices=["budget-exceeded", "tool-timeout"])
    parser.add_argument("--serve", action="store_true", help="Start API on :8106")
    parser.add_argument("--port", type=int, default=8106)
    args = parser.parse_args()
    if args.inject:
        print(f"Injection {args.inject}")
        return 0
    if args.serve:
        import uvicorn

        from .api import create_app

        uvicorn.run(create_app(), host="0.0.0.0", port=args.port)
        return 0
    if args.task:
        run_agent(args.agent, args.task)
    else:
        print("Use --task to run agent or --serve for API")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
