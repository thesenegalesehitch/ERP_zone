"""
Modèle de données pour la trésorerie

Ce module définit le modèle de données pour la trésorerie
dans le module de comptabilité.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class CashFlowModel:
    """Modèle de flux de trésorerie"""
    
    def __init__(
        self,
        id: int,
        transaction_date: date = None,
        description: str,
        amount: float = 0,
        flow_type: str = "entree",
        category: str = "autre",
        reference: Optional[str] = None,
        status: str = "en_attente",
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.transaction_date = transaction_date
        self.description = description
        self.amount = amount
        self.flow_type = flow_type
        self.category = category
        self.reference = reference
        self.status = status
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "transaction_date": self.transaction_date,
            "description": self.description,
            "amount": self.amount,
            "flow_type": self.flow_type,
            "category": self.category,
            "reference": self.reference,
            "status": self.status,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CashFlowModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            transaction_date=data.get("transaction_date"),
            description=data.get("description"),
            amount=data.get("amount", 0),
            flow_type=data.get("flow_type", "entree"),
            category=data.get("category", "autre"),
            reference=data.get("reference"),
            status=data.get("status", "en_attente"),
            created_at=data.get("created_at")
        )
    
    def is_inflow(self) -> bool:
        """Vérifie si entrée"""
        return self.flow_type == "entree"
    
    def is_outflow(self) -> bool:
        """Vérifie si sortie"""
        return self.flow_type == "sortie"


class BudgetModel:
    """Modèle de budget"""
    
    def __init__(
        self,
        id: int,
        name: str,
        period: str,
        start_date: date = None,
        end_date: date = None,
        total_budget: float = 0,
        spent_amount: float = 0,
        currency: str = "XOF",
        status: str = "actif",
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.total_budget = total_budget
        self.spent_amount = spent_amount
        self.currency = currency
        self.status = status
        self.notes = notes
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "period": self.period,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_budget": self.total_budget,
            "spent_amount": self.spent_amount,
            "currency": self.currency,
            "status": self.status,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def remaining_amount(self) -> float:
        """Montant restant"""
        return self.total_budget - self.spent_amount
    
    def utilization_percentage(self) -> float:
        """Pourcentage d'utilisation"""
        if self.total_budget == 0:
            return 0
        return (self.spent_amount / self.total_budget) * 100


class ExpenseCategoryModel:
    """Modèle de catégorie de dépense"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        parent_id: Optional[int] = None,
        budget_allocation: float = 0,
        is_active: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.parent_id = parent_id
        self.budget_allocation = budget_allocation
        self.is_active = is_active
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "parent_id": self.parent_id,
            "budget_allocation": self.budget_allocation,
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": self.created_at
        }
