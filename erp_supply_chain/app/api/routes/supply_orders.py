from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.supply_order import SupplyOrder
from app.schemas.supply_order import SupplyOrderCreate, SupplyOrderResponse

router = APIRouter(prefix="/supply-orders", tags=["supply-orders"])


@router.get("/", response_model=list[SupplyOrderResponse])
def get_supply_orders(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(SupplyOrder).offset(skip).limit(limit).all()


@router.post("/", response_model=SupplyOrderResponse, status_code=status.HTTP_201_CREATED)
def create_supply_order(data: SupplyOrderCreate, db: Session = Depends(get_db)):
    order = SupplyOrder(**data.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
