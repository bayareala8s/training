"""Pydantic schemas for Lab 014 API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SimulateRequest(BaseModel):
    route: str = Field(default="/api", examples=["/api"])


class InjectRequest(BaseModel):
    inject: str = Field(..., examples=["error-spike"])
    rate: float = Field(default=0.5, ge=0.0, le=1.0)
