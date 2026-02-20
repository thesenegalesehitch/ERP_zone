from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportResponse

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Report).offset(skip).limit(limit).all()


@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(data: ReportCreate, db: Session = Depends(get_db)):
    report = Report(**data.dict())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
