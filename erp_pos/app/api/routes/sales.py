from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/", response_model=list[SaleResponse])
def get_sales(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Sale).offset(skip).limit(limit).all()


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(data: SaleCreate, db: Session = Depends(get_db)):
    sale = Sale(**data.dict())
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale
