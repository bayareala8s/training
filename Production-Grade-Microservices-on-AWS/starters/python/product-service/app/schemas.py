from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    price: float = Field(gt=0)
    sku: str = Field(min_length=1)
    stock: int = Field(ge=0, default=0)


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    sku: str
    stock: int

    class Config:
        from_attributes = True
