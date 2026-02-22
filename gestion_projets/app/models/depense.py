"""
Modèle de données pour les dépenses

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
        expense_type: str,
        description: str,
        amount: float,
        currency: str = "XOF",
        expense_date: Optional[date] = None,
        status: str = "en_attente",
        receipt_url: Optional[str] = None,
        vendor: Optional[str] = None,
        category: Optional[str] = None,
        approved_by: Optional[int] = None,
        approved_at: Optional[datetime] = None,
        paid_by: Optional[int] = None,
        paid_at: Optional[datetime] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.expense_type = expense_type
        self.description = description
        self.amount = amount
        self.currency = currency
        self.expense_date = expense_date
        self.status = status
        self.receipt_url = receipt_url
        self.vendor = vendor
        self.category = category
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.paid_by = paid_by
        self.paid_at = paid_at
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "expense_type": self.expense_type,
            "description": self.description,
            "amount": self.amount,
            "currency": self.currency,
            "expense_date": self.expense_date,
            "status": self.status,
            "receipt_url": self.receipt_url,
            "vendor": self.vendor,
            "category": self.category,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "paid_by": self.paid_by,
            "paid_at": self.paid_at,
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
            expense_type=data.get("expense_type"),
            description=data.get("description"),
            amount=data.get("amount"),
            currency=data.get("currency", "XOF"),
            expense_date=data.get("expense_date"),
            status=data.get("status", "en_attente"),
            receipt_url=data.get("receipt_url"),
            vendor=data.get("vendor"),
            category=data.get("category"),
            approved_by=data.get("approved_by"),
            approved_at=data.get("approved_at"),
            paid_by=data.get("paid_by"),
            paid_at=data.get("paid_at"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_approved(self) -> bool:
        """Vérifie si la dépense est approuvée"""
        return self.status == "approuve"
    
    def is_paid(self) -> bool:
        """Vérifie si la dépense est payée"""
        return self.status == "paye"


class ExpenseCategoryModel:
    """Modèle de catégorie de dépense"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        description: Optional[str] = None,
        budget_category: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.budget_category = budget_category
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "budget_category": self.budget_category,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class ProjectExpenseTotalModel:
    """Modèle de total des dépenses du projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        total_planned: float = 0,
        total_actual: float = 0,
        total_approved: float = 0,
        total_paid: float = 0,
        currency: str = "XOF",
        as_of_date: Optional[date] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.total_planned = total_planned
        self.total_actual = total_actual
        self.total_approved = total_approved
        self.total_paid = total_paid
        self.currency = currency
        self.as_of_date = as_of_date
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "total_planned": self.total_planned,
            "total_actual": self.total_actual,
            "total_approved": self.total_approved,
            "total_paid": self.total_paid,
            "currency": self.currency,
            "as_of_date": self.as_of_date,
            "updated_at": self.updated_at
        }
    
    def variance(self) -> float:
        """Calcule l'écart"""
        return self.total_planned - self.total_actual
    
    def variance_percent(self) -> float:
        """Calcule le pourcentage d'écart"""
        if self.total_planned == 0:
            return 0
        return (self.variance / self.total_planned) * 100


class ExpenseApprovalModel:
    """Modèle d'approbation de dépense"""
    
    def __init__(
        self,
        id: int,
        expense_id: int,
        approved_by: int,
        approval_date: Optional[datetime] = None,
        status: str = "en_attente",
        comments: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.expense_id = expense_id
        self.approved_by = approved_by
        self.approval_date = approval_date
        self.status = status
        self.comments = comments
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "expense_id": self.expense_id,
            "approved_by": self.approved_by,
            "approval_date": self.approval_date,
            "status": self.status,
            "comments": self.comments,
            "created_at": self.created_at
        }
    
    def approve(self, comments: Optional[str] = None):
        """Approuve la dépense"""
        self.status = "approuve"
        self.approval_date = datetime.now()
        if comments:
            self.comments = comments
    
    def reject(self, comments: str):
        """Rejette la dépense"""
        self.status = "rejete"
        self.comments = comments
