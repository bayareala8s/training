"""Pydantic schemas for Lab 012 API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RegionConfigSchema(BaseModel):
    name: str
    vpc_cidr: str
    is_primary: bool = False


class LabConfigSchema(BaseModel):
    primary_region: str
    dr_region: str
    rto_minutes: int = 15
    rpo_minutes: int = 5
    budget_usd: int = 25
    regions: list[RegionConfigSchema] = Field(default_factory=list)


class ConfigValidateRequest(BaseModel):
    config: LabConfigSchema | None = None
    use_example: bool = False


class ConfigValidateResponse(BaseModel):
    valid: bool
    errors: list[str]
    primary_region: str | None = None
    dr_region: str | None = None
    required_tags: dict[str, str] = Field(default_factory=dict)


class FailoverSimulateRequest(BaseModel):
    dry_run: bool = True


class FailoverStep(BaseModel):
    step: int
    action: str
    mode: str


class FailoverSimulateResponse(BaseModel):
    dry_run: bool
    steps: list[FailoverStep]


class HealthResponse(BaseModel):
    status: str
    lab: str
    primary_region: str | None = None
    dr_region: str | None = None
    required_tags: dict[str, str] = Field(default_factory=dict)
