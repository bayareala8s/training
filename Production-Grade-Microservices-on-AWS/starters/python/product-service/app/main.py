from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db
from app.models import ProductModel
from app.schemas import ProductCreate, ProductResponse

SEED_PRODUCTS = [
    {
        "name": "Cloud Native Handbook",
        "description": "Enterprise microservices guide",
        "price": 49.99,
        "sku": "BOOK-001",
        "stock": 100,
    },
    {
        "name": "AWS Practice Kit",
        "description": "Hands-on lab accessories",
        "price": 29.99,
        "sku": "KIT-001",
        "stock": 50,
    },
]


def seed_products(db: Session):
    if db.query(ProductModel).count() == 0:
        for item in SEED_PRODUCTS:
            db.add(ProductModel(**item))
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_products(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Product Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}


@app.get("/products", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()


@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(ProductModel).filter(ProductModel.sku == payload.sku).first()
    if existing:
        raise HTTPException(status_code=409, detail="SKU already exists")
    product = ProductModel(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
