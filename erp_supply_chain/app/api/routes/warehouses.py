from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.get("/", response_model=list[WarehouseResponse])
def get_warehouses(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Warehouse).offset(skip).limit(limit).all()


@router.post("/", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse(data: WarehouseCreate, db: Session = Depends(get_db)):
    warehouse = Warehouse(**data.dict())
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse
