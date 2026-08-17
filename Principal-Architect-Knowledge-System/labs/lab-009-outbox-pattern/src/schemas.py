"""API request models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateOrderRequest(BaseModel):
    sku: str = Field(..., min_length=1, examples=["SKU-100"])
    quantity: int = Field(..., ge=1, examples=[2])

    model_config = {
        "json_schema_extra": {"examples": [{"sku": "SKU-100", "quantity": 2}]}
    }
