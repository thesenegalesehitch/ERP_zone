"""
Modèle de données pour les commandes

Ce module définit le modèle de données pour les commandes
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class PurchaseRequestModel:
    """Modèle de demande d'achat"""
    
    def __init__(
        self,
        id: int,
        request_number: str,
        requester_id: int,
        department_id: int,
        priority: str = "normale",
        status: str = "brouillon",
        request_date: Optional[date] = None,
        expected_date: Optional[date] = None,
        total_amount: float = 0,
        currency: str = "XOF",
        justification: Optional[str] = None,
        notes: Optional[str] = None,
        approved_by: Optional[int] = None,
        approved_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.request_number = request_number
        self.requester_id = requester_id
        self.department_id = department_id
        self.priority = priority
        self.status = status
        self.request_date = request_date
        self.expected_date = expected_date
        self.total_amount = total_amount
        self.currency = currency
        self.justification = justification
        self.notes = notes
        self.approved_by = approved_by
        self.approved_at = approved_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "request_number": self.request_number,
            "requester_id": self.requester_id,
            "department_id": self.department_id,
            "priority": self.priority,
            "status": self.status,
            "request_date": self.request_date,
            "expected_date": self.expected_date,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "justification": self.justification,
            "notes": self.notes,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PurchaseRequestModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            request_number=data.get("request_number"),
            requester_id=data.get("requester_id"),
            department_id=data.get("department_id"),
            priority=data.get("priority", "normale"),
            status=data.get("status", "brouillon"),
            request_date=data.get("request_date"),
            expected_date=data.get("expected_date"),
            total_amount=data.get("total_amount", 0),
            currency=data.get("currency", "XOF"),
            justification=data.get("justification"),
            notes=data.get("notes"),
            approved_by=data.get("approved_by"),
            approved_at=data.get("approved_at"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_approved(self) -> bool:
        """Vérifie si la demande est approuvée"""
        return self.status == "approuve"
    
    def is_pending(self) -> bool:
        """Vérifie si la demande est en attente"""
        return self.status in ["soumis", "en_attente"]


class RequisitionLineModel:
    """Modèle de ligne de demande"""
    
    def __init__(
        self,
        id: int,
        requisition_id: int,
        product_id: int,
        quantity: float = 1,
        estimated_price: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.requisition_id = requisition_id
        self.product_id = product_id
        self.quantity = quantity
        self.estimated_price = estimated_price
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "requisition_id": self.requisition_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "estimated_price": self.estimated_price,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def estimated_total(self) -> float:
        """Total estimé"""
        return self.quantity * self.estimated_price


class InventoryAlertModel:
    """Modèle d'alerte d'inventaire"""
    
    def __init__(
        self,
        id: int,
        product_id: int,
        alert_type: str,
        current_level: float = 0,
        threshold: float = 0,
        status: str = "active",
        triggered_at: Optional[datetime] = None,
        resolved_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.product_id = product_id
        self.alert_type = alert_type
        self.current_level = current_level
        self.threshold = threshold
        self.status = status
        self.triggered_at = triggered_at
        self.resolved_at = resolved_at
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "alert_type": self.alert_type,
            "current_level": self.current_level,
            "threshold": self.threshold,
            "status": self.status,
            "triggered_at": self.triggered_at,
            "resolved_at": self.resolved_at,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_resolved(self) -> bool:
        """Vérifie si résolu"""
        return self.status == "resolue"
    
    def is_low_stock(self) -> bool:
        """Vérifie si stock bas"""
        return self.alert_type == "stock_bas"
    
    def is_overstock(self) -> bool:
        """Vérifie si surstock"""
        return self.alert_type == "surstock"
