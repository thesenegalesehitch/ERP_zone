from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
