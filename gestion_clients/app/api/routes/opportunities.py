from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate, OpportunityResponse

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


@router.get("/", response_model=list[OpportunityResponse])
def get_opportunities(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(Opportunity).offset(skip).limit(limit).all()


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity


@router.post("/", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(opportunity_data: OpportunityCreate, db: Session = Depends(get_db)):
    opportunity = Opportunity(**opportunity_data.dict())
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity


@router.delete("/{opportunity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    db.delete(opportunity)
    db.commit()
    return
