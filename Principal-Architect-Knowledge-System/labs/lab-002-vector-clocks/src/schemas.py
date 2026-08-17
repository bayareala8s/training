"""Pydantic schemas for Lab 002 API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class LocalEventRequest(BaseModel):
    process_id: int = Field(..., ge=0, examples=[0])
    num_processes: int = Field(default=2, ge=1, le=64, examples=[2])


class SendMessageRequest(BaseModel):
    from_process: int = Field(..., alias="from", ge=0, examples=[0])
    to: int = Field(..., ge=0, examples=[1])
    payload: Any = Field(..., examples=["hello"])
    msg_id: str = Field(..., examples=["m1"])

    model_config = {"populate_by_name": True}


class CompareRequest(BaseModel):
    clock_a: list[int] = Field(..., examples=[[1, 0]])
    clock_b: list[int] = Field(..., examples=[[2, 1]])
