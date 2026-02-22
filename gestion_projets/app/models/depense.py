"""
Modèle de données pour les dépenses de projet

Ce module définit le modèle de données pour les dépenses
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class ExpenseModel:
    """Modèle de dépense"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        description: str,
        amount: float = 0,
        currency: str = "XOF",
        expense_type: str = "autre",
        expense_date: date = None,
        status: str = "en_attente",
        vendor: Optional[str] = None,
        invoice_number: Optional[str] = None,
        receipt_url: Optional[str] = None,
        approved_by: Optional[int] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.description = description
        self.amount = amount
        self.currency = currency
        self.expense_type = expense_type
        self.expense_date = expense_date or date.today()
        self.status = status
        self.vendor = vendor
        self.invoice_number = invoice_number
        self.receipt_url = receipt_url
        self.approved_by = approved_by
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "description": self.description,
            "amount": self.amount,
            "currency": self.currency,
            "expense_type": self.expense_type,
            "expense_date": self.expense_date,
            "status": self.status,
            "vendor": self.vendor,
            "invoice_number": self.invoice_number,
            "receipt_url": self.receipt_url,
            "approved_by": self.approved_by,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ExpenseModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            description=data.get("description"),
            amount=data.get("amount", 0),
            currency=data.get("currency", "XOF"),
            expense_type=data.get("expense_type", "autre"),
            expense_date=data.get("expense_date"),
            status=data.get("status", "en_attente"),
            vendor=data.get("vendor"),
            invoice_number=data.get("invoice_number"),
            receipt_url=data.get("receipt_url"),
            approved_by=data.get("approved_by"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"
    
    def is_rejected(self) -> bool:
        """Vérifie si rejeté"""
        return self.status == "rejete"


class ExpenseCategoryModel:
    """Modèle de catégorie de dépense"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        budget_code: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.budget_code = budget_code
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "budget_code": self.budget_code,
            "is_active": self.is_active,
            "created_at": self.created_at
        }


class ExpenseReportModel:
    """Modèle de rapport de dépenses"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        title: str,
        start_date: date,
        end_date: date,
        total_amount: float = 0,
        currency: str = "XOF",
        status: str = "brouillon",
        submitted_by: int = None,
        submitted_date: Optional[date] = None,
        approved_by: Optional[int] = None,
        approved_date: Optional[date] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.total_amount = total_amount
        self.currency = currency
        self.status = status
        self.submitted_by = submitted_by
        self.submitted_date = submitted_date
        self.approved_by = approved_by
        self.approved_date = approved_date
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "status": self.status,
            "submitted_by": self.submitted_by,
            "submitted_date": self.submitted_date,
            "approved_by": self.approved_by,
            "approved_date": self.approved_date,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_submitted(self) -> bool:
        """Vérifie si soumis"""
        return self.status == "soumis"
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"
