"""Pydantic schemas for Lab 016 API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    task: str
    tenant_id: str = "default"
    agent_id: str = "support-agent"


class AgentStepResponse(BaseModel):
    step_index: int
    thought: str
    tool_name: str | None = None
    result: Any = None


class AgentRunResponse(BaseModel):
    run_id: str
    agent_id: str
    tenant_id: str
    task: str
    status: str
    steps: list[AgentStepResponse]


class AgentRunSummary(BaseModel):
    run_id: str
    agent_id: str
    tenant_id: str
    task: str
    status: str
    step_count: int


class AgentRunsListResponse(BaseModel):
    runs: list[AgentRunSummary]


class ToolInvokeRequest(BaseModel):
    tool_name: str
    tenant_id: str = "default"
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolInvokeResponse(BaseModel):
    tool_name: str
    allowed: bool
    result: Any = None
    policy: str
    error: str | None = None
