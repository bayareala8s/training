"""API request models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Charge amount", examples=[10.0])
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO currency code",
        examples=["USD"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"amount": 10.0, "currency": "USD"}]
        }
    }
