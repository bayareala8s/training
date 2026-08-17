"""Pydantic schemas for Lab 011 API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CheckRequest(BaseModel):
    tenant_id: str = Field(..., examples=["tenant-1"])
    route: str = Field(..., examples=["/api/v1/orders"])


class RedisDownRequest(BaseModel):
    enabled: bool = Field(default=True, examples=[True])
    mode: str = Field(default="fail-closed", examples=["fail-closed"])
