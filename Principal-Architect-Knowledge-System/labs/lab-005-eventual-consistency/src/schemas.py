"""Pydantic schemas for Lab 005 API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PutKeyRequest(BaseModel):
    value: Any = Field(..., examples=["alice"])
    replica_id: str = Field(default="r1", examples=["r1"])


class PartitionRequest(BaseModel):
    replicas: list[str] = Field(..., examples=[["r3"]])
    enabled: bool = Field(default=True, examples=[True])
