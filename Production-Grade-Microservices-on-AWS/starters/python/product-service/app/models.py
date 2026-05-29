import uuid

from sqlalchemy import Column, Float, Integer, String, Text

from app.database import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    price = Column(Float, nullable=False)
    sku = Column(String, unique=True, nullable=False, index=True)
    stock = Column(Integer, default=0)
