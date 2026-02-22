"""
Modèle de données pour les budgets de projet

Ce module définit le modèle de données pour les budgets
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class BudgetModel:
    """Modèle de budget"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        total_amount: float = 0,
        currency: str = "XOF",
        start_date: date = None,
        end_date: Optional[date] = None,
        status: str = "planifie",
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.total_amount = total_amount
        self.currency = currency
        self.start_date = start_date or date.today()
        self.end_date = end_date
        self.status = status
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "BudgetModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            name=data.get("name"),
            total_amount=data.get("total_amount", 0),
            currency=data.get("currency", "XOF"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            status=data.get("status", "planifie"),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"


class BudgetCategoryModel:
    """Modèle de catégorie de budget"""
    
    def __init__(
        self,
        id: int,
        budget_id: int,
        name: str,
        allocated_amount: float = 0,
        spent_amount: float = 0,
        currency: str = "XOF",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.budget_id = budget_id
        self.name = name
        self.allocated_amount = allocated_amount
        self.spent_amount = spent_amount
        self.currency = currency
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "budget_id": self.budget_id,
            "name": self.name,
            "allocated_amount": self.allocated_amount,
            "spent_amount": self.spent_amount,
            "currency": self.currency,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def remaining_amount(self) -> float:
        """Montant restant"""
        return self.allocated_amount - self.spent_amount
    
    def utilization_percentage(self) -> float:
        """Pourcentage d'utilisation"""
        if self.allocated_amount == 0:
            return 0
        return (self.spent_amount / self.allocated_amount) * 100


class BudgetExpenseModel:
    """Modèle de dépense de budget"""
    
    def __init__(
        self,
        id: int,
        category_id: int,
        description: str,
        amount: float = 0,
        currency: str = "XOF",
        expense_date: date = None,
        status: str = "en_attente",
        vendor: Optional[str] = None,
        invoice_number: Optional[str] = None,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.category_id = category_id
        self.description = description
        self.amount = amount
        self.currency = currency
        self.expense_date = expense_date or date.today()
        self.status = status
        self.vendor = vendor
        self.invoice_number = invoice_number
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "category_id": self.category_id,
            "description": self.description,
            "amount": self.amount,
            "currency": self.currency,
            "expense_date": self.expense_date,
            "status": self.status,
            "vendor": self.vendor,
            "invoice_number": self.invoice_number,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at
        }
    
    def is_approved(self) -> bool:
        """Vérifie si approuvé"""
        return self.status == "approuve"
