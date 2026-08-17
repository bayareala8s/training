"""API request/response models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChargeRequest(BaseModel):
    amount_cents: int = Field(..., ge=1, description="Charge amount in cents", examples=[2500])
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO currency code",
        examples=["usd"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"amount_cents": 2500, "currency": "usd"}]
        }
    }
