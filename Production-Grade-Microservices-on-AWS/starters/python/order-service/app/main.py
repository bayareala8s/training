import os

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.events import publish_event
from app.models import OrderItemModel, OrderModel
from app.schemas import OrderCreate, OrderItemResponse, OrderResponse

app = FastAPI(title="Order Service", version="1.0.0")
Base.metadata.create_all(bind=engine)

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8002")


def fetch_product(product_id: str) -> dict:
    with httpx.Client(timeout=10.0) as client:
        response = client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        response.raise_for_status()
        return response.json()


@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}


@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    order_items = []
    total = 0.0

    for item in payload.items:
        product = fetch_product(item.product_id)
        if product["stock"] < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product['name']}",
            )
        line_total = product["price"] * item.quantity
        total += line_total
        order_items.append(
            OrderItemModel(
                product_id=product["id"],
                product_name=product["name"],
                quantity=item.quantity,
                unit_price=product["price"],
            )
        )

    order = OrderModel(user_id=payload.user_id, total=total, status="PLACED", items=order_items)
    db.add(order)
    db.commit()
    db.refresh(order)

    publish_event(
        source="course.orders",
        detail_type="OrderPlaced",
        detail={
            "order_id": order.id,
            "user_id": order.user_id,
            "total": order.total,
            "items": [
                {
                    "product_id": i.product_id,
                    "product_name": i.product_name,
                    "quantity": i.quantity,
                }
                for i in order.items
            ],
        },
    )

    return _to_response(order)


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _to_response(order)


def _to_response(order: OrderModel) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        total=order.total,
        created_at=order.created_at,
        items=[
            OrderItemResponse(
                product_id=i.product_id,
                product_name=i.product_name,
                quantity=i.quantity,
                unit_price=i.unit_price,
            )
            for i in order.items
        ],
    )
