"""
API routes pour la gestion comptable

Ce module définit les routes API pour les opérations CRUD
sur les comptes et écritures comptables.

Ce fichier fait partie du projet ERP développé pour le Sénégal.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.transaction import (
    AccountCreate, AccountUpdate, AccountResponse,
    JournalEntryCreate, JournalEntryUpdate, JournalEntryResponse,
    CostCenterCreate, CostCenterUpdate, CostCenterResponse,
    FiscalYearCreate, FiscalYearUpdate, FiscalYearResponse
)
from app.models.transaction import Account, JournalEntry, JournalEntryLine, CostCenter, FiscalYear
from app.models.user import User
from app.core.auth import get_current_user

router = APIRouter(prefix="/accounting", tags=["accounting"])


# Routes pour les comptes
@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau compte"""
    db_account = Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("/accounts", response_model=List[AccountResponse])
def list_accounts(
    account_type: str = None,
    parent_id: int = None,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les comptes avec filtres optionnels"""
    query = db.query(Account)
    
    if account_type:
        query = query.filter(Account.account_type == account_type)
    if parent_id:
        query = query.filter(Account.parent_id == parent_id)
    if is_active is not None:
        query = query.filter(Account.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()


@router.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un compte par son ID"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    return account


@router.put("/accounts/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    account_update: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour un compte"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    
    for key, value in account_update.dict(exclude_unset=True).items():
        setattr(account, key, value)
    
    db.commit()
    db.refresh(account)
    return account


# Routes pour les écritures journal
@router.post("/journal-entries", response_model=JournalEntryResponse, status_code=status.HTTP_201_CREATED)
def create_journal_entry(
    entry: JournalEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer une nouvelle écriture journal"""
    db_entry = JournalEntry(
        entry_number=f"JE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        **entry.dict()
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/journal-entries", response_model=List[JournalEntryResponse])
def list_journal_entries(
    status: str = None,
    transaction_type: str = None,
    date_from: datetime = None,
    date_to: datetime = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les écritures journal"""
    query = db.query(JournalEntry)
    
    if status:
        query = query.filter(JournalEntry.status == status)
    if transaction_type:
        query = query.filter(JournalEntry.transaction_type == transaction_type)
    if date_from:
        query = query.filter(JournalEntry.date >= date_from)
    if date_to:
        query = query.filter(JournalEntry.date <= date_to)
    
    return query.offset(skip).limit(limit).all()


@router.get("/journal-entries/{entry_id}", response_model=JournalEntryResponse)
def get_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer une écriture par son ID"""
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Écriture non trouvée")
    return entry


# Routes pour les centres de coût
@router.post("/cost-centers", response_model=CostCenterResponse, status_code=status.HTTP_201_CREATED)
def create_cost_center(
    cost_center: CostCenterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau centre de coût"""
    db_cost_center = CostCenter(**cost_center.dict())
    db.add(db_cost_center)
    db.commit()
    db.refresh(db_cost_center)
    return db_cost_center


@router.get("/cost-centers", response_model=List[CostCenterResponse])
def list_cost_centers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les centres de coût"""
    return db.query(CostCenter).all()


# Routes pour les exercices comptables
@router.post("/fiscal-years", response_model=FiscalYearResponse, status_code=status.HTTP_201_CREATED)
def create_fiscal_year(
    fiscal_year: FiscalYearCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouvel exercice comptable"""
    db_fiscal_year = FiscalYear(**fiscal_year.dict())
    db.add(db_fiscal_year)
    db.commit()
    db.refresh(db_fiscal_year)
    return db_fiscal_year


@router.get("/fiscal-years", response_model=List[FiscalYearResponse])
def list_fiscal_years(
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les exercices comptables"""
    query = db.query(FiscalYear)
    
    if is_active is not None:
        query = query.filter(FiscalYear.is_active == is_active)
    
    return query.all()


from datetime import datetime
