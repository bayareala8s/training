"""Pydantic request/response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateOrderRequest(BaseModel):
    customer_id: str = Field(..., examples=["cust-42"])
    amount: float = Field(..., gt=0, examples=[99.99])
    region: str = Field(..., examples=["us-west"])
    order_id: str | None = Field(default=None, examples=["ord-demo-1"])
