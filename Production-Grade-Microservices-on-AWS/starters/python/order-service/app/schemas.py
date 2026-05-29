from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemInput(BaseModel):
    product_id: str
    quantity: int = Field(ge=1)


class OrderCreate(BaseModel):
    user_id: str
    items: list[OrderItemInput] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float


class OrderResponse(BaseModel):
    id: str
    user_id: str
    status: str
    total: float
    created_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True
