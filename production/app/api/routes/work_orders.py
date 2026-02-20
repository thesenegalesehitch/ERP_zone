from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.work_order import WorkOrder
from app.schemas.work_order import WorkOrderCreate, WorkOrderResponse

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


@router.get("/", response_model=list[WorkOrderResponse])
def get_work_orders(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(WorkOrder).offset(skip).limit(limit).all()


@router.post("/", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
def create_work_order(data: WorkOrderCreate, db: Session = Depends(get_db)):
    order = WorkOrder(**data.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
