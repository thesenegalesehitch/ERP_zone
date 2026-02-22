"""
API routes pour les demandes decongé

Ce module définit les routes API pour les opérations CRUD
sur les demandes decongé du système de ressources humaines.

Ce fichier fait partie du projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.leave_request import (
    LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestResponse
)
from app.models.leave_request import LeaveRequest, LeaveStatus
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter(prefix="/leave-requests", tags=["leave_requests"])


@router.post("/", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
def create_leave_request(
    leave_request: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle demande decongé"""
    db_leave_request = LeaveRequest(**leave_request.dict())
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request


@router.get("/", response_model=List[LeaveRequestResponse])
def list_leave_requests(
    employee_id: int = None,
    status: str = None,
    leave_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les demandes decongé avec filtres optionnels"""
    query = db.query(LeaveRequest)
    
    if employee_id:
        query = query.filter(LeaveRequest.employee_id == employee_id)
    if status:
        query = query.filter(LeaveRequest.status == status)
    if leave_type:
        query = query.filter(LeaveRequest.leave_type == leave_type)
    
    return query.offset(skip).limit(limit).all()


@router.get("/{leave_request_id}", response_model=LeaveRequestResponse)
def get_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer une demande decongé par son ID"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Demande decongé non trouvée")
    return leave_request


@router.put("/{leave_request_id}", response_model=LeaveRequestResponse)
def update_leave_request(
    leave_request_id: int,
    leave_request_update: LeaveRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour une demande decongé"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Demande decongé non trouvée")
    
    for key, value in leave_request_update.dict(exclude_unset=True).items():
        setattr(leave_request, key, value)
    
    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.put("/{leave_request_id}/approve", response_model=LeaveRequestResponse)
def approve_leave_request(
    leave_request_id: int,
    approval_notes: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approuver une demande decongé"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Demande decongé non trouvée")
    
    if leave_request.status != LeaveStatus.EN_ATTENTE:
        raise HTTPException(status_code=400, detail="La demande n'est plus en attente")
    
    leave_request.status = LeaveStatus.APPROUVÉE
    leave_request.approved_by = current_user.id
    leave_request.approval_notes = approval_notes
    
    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.put("/{leave_request_id}/reject", response_model=LeaveRequestResponse)
def reject_leave_request(
    leave_request_id: int,
    approval_notes: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rejeter une demande decongé"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Demande decongé non trouvée")
    
    if leave_request.status != LeaveStatus.EN_ATTENTE:
        raise HTTPException(status_code=400, detail="La demande n'est plus en attente")
    
    leave_request.status = LeaveStatus.REJETÉE
    leave_request.approved_by = current_user.id
    leave_request.approval_notes = approval_notes
    
    db.commit()
    db.refresh(leave_request)
    return leave_request


@router.delete("/{leave_request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprimer une demande decongé"""
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Demande decongé non trouvée")
    
    db.delete(leave_request)
    db.commit()
    return None
