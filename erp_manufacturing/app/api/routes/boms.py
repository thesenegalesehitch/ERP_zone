from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.bom import BillOfMaterials
from app.schemas.bom import BOMCreate, BOMResponse

router = APIRouter(prefix="/boms", tags=["boms"])


@router.get("/", response_model=list[BOMResponse])
def get_boms(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(BillOfMaterials).offset(skip).limit(limit).all()


@router.post("/", response_model=BOMResponse, status_code=status.HTTP_201_CREATED)
def create_bom(data: BOMCreate, db: Session = Depends(get_db)):
    bom = BillOfMaterials(**data.dict())
    db.add(bom)
    db.commit()
    db.refresh(bom)
    return bom
