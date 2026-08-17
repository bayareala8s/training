"""Pydantic schemas for Lab 001 API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AddNodeRequest(BaseModel):
    node_id: str = Field(..., examples=["node-a"])
    vnode_count: int = Field(default=128, ge=1, le=1024, examples=[128])


class LookupRequest(BaseModel):
    key: str = Field(..., examples=["user:42"])


class SimulationRequest(BaseModel):
    key_count: int = Field(default=10_000, ge=100, le=500_000)


class NodeFailureRequest(BaseModel):
    node_id: str = Field(..., examples=["node-b"])
    key_count: int = Field(default=10_000, ge=100, le=500_000)
