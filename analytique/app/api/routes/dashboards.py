from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.dashboard import Dashboard
from app.schemas.dashboard import DashboardCreate, DashboardResponse

router = APIRouter(prefix="/dashboards", tags=["dashboards"])


@router.get("/", response_model=list[DashboardResponse])
def get_dashboards(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Dashboard).offset(skip).limit(limit).all()


@router.post("/", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
def create_dashboard(data: DashboardCreate, db: Session = Depends(get_db)):
    dashboard = Dashboard(**data.dict())
    db.add(dashboard)
    db.commit()
    db.refresh(dashboard)
    return dashboard
