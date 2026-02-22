"""
Modèle de données pour les budgets de projet

Ce module définit le modèle de données pour les budgets
dans le module de gestion de projets.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class ProjectBudgetModel:
    """Modèle de budget de projet"""
    
    def __init__(
        self,
        id: int,
        project_id: int,
        name: str,
        total_budget: float = 0,
        currency: str = "XOF",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: str = "planifie",
        spent_amount: float = 0,
        committed_amount: float = 0,
        notes: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.total_budget = total_budget
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.spent_amount = spent_amount
        self.committed_amount = committed_amount
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
            "total_budget": self.total_budget,
            "currency": self.currency,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "spent_amount": self.spent_amount,
            "committed_amount": self.committed_amount,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProjectBudgetModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            project_id=data.get("project_id"),
            name=data.get("name"),
            total_budget=data.get("total_budget", 0),
            currency=data.get("currency", "XOF"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            status=data.get("status", "planifie"),
            spent_amount=data.get("spent_amount", 0),
            committed_amount=data.get("committed_amount", 0),
            notes=data.get("notes"),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def remaining_amount(self) -> float:
        """Calcule le montant restant"""
        return self.total_budget - self.spent_amount - self.committed_amount
    
    def utilization_percentage(self) -> float:
        """Calcule le pourcentage d'utilisation"""
        if self.total_budget == 0:
            return 0
        return ((self.spent_amount + self.committed_amount) / self.total_budget) * 100
    
    def is_over_budget(self) -> bool:
        """Vérifie si le budget est dépassé"""
        return (self.spent_amount + self.committed_amount) > self.total_budget


class BudgetCategoryModel:
    """Modèle de catégorie de budget"""
    
    def __init__(
        self,
        id: int,
        budget_id: int,
        name: str,
        allocated_amount: float = 0,
        spent_amount: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.budget_id = budget_id
        self.name = name
        self.allocated_amount = allocated_amount
        self.spent_amount = spent_amount
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
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def remaining_amount(self) -> float:
        """Calcule le montant restant"""
        return self.allocated_amount - self.spent_amount
    
    def utilization_percentage(self) -> float:
        """Calcule le pourcentage d'utilisation"""
        if self.allocated_amount == 0:
            return 0
        return (self.spent_amount / self.allocated_amount) * 100


class BudgetTransactionModel:
    """Modèle de transaction budgétaire"""
    
    def __init__(
        self,
        id: int,
        budget_id: int,
        category_id: Optional[int] = None,
        amount: float = 0,
        transaction_type: str = "depense",
        description: Optional[str] = None,
        transaction_date: Optional[date] = None,
        reference: Optional[str] = None,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.budget_id = budget_id
        self.category_id = category_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.transaction_date = transaction_date
        self.reference = reference
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "budget_id": self.budget_id,
            "category_id": self.category_id,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "description": self.description,
            "transaction_date": self.transaction_date,
            "reference": self.reference,
            "created_by": self.created_by,
            "created_at": self.created_at
        }
    
    def is_expense(self) -> bool:
        """Vérifie si c'est une dépense"""
        return self.transaction_type == "depense"
    
    def is_income(self) -> bool:
        """Vérifie si c'est un revenu"""
        return self.transaction_type == "revenu"
