"""
Modèle de données pour les réservations

Ce module définit le modèle de données pour les réservations
dans le module restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date, time
from typing import Optional


class ReservationModel:
    """Modèle de réservation"""
    
    def __init__(
        self,
        id: int,
        customer_id: int,
        table_id: Optional[int] = None,
        reservation_date: date = None,
        reservation_time: time = None,
        guest_count: int = 1,
        status: str = "en_attente",
        special_requests: Optional[str] = None,
        notes: Optional[str] = None,
        confirmed_at: Optional[datetime] = None,
        cancelled_at: Optional[datetime] = None,
        cancellation_reason: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.customer_id = customer_id
        self.table_id = table_id
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.guest_count = guest_count
        self.status = status
        self.special_requests = special_requests
        self.notes = notes
        self.confirmed_at = confirmed_at
        self.cancelled_at = cancelled_at
        self.cancellation_reason = cancellation_reason
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "table_id": self.table_id,
            "reservation_date": self.reservation_date,
            "reservation_time": self.reservation_time,
            "guest_count": self.guest_count,
            "status": self.status,
            "special_requests": self.special_requests,
            "notes": self.notes,
            "confirmed_at": self.confirmed_at,
            "cancelled_at": self.cancelled_at,
            "cancellation_reason": self.cancellation_reason,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ReservationModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            customer_id=data.get("customer_id"),
            table_id=data.get("table_id"),
            reservation_date=data.get("reservation_date"),
            reservation_time=data.get("reservation_time"),
            guest_count=data.get("guest_count", 1),
            status=data.get("status", "en_attente"),
            special_requests=data.get("special_requests"),
            notes=data.get("notes"),
            confirmed_at=data.get("confirmed_at"),
            cancelled_at=data.get("cancelled_at"),
            cancellation_reason=data.get("cancellation_reason"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_confirmed(self) -> bool:
        """Vérifie si la réservation est confirmée"""
        return self.status == "confirmee"
    
    def is_cancelled(self) -> bool:
        """Vérifie si la réservation est annulée"""
        return self.status == "annulee"
    
    def is_completed(self) -> bool:
        """Vérifie si la réservation est terminée"""
        return self.status == "terminee"


class TableModel:
    """Modèle de table"""
    
    def __init__(
        self,
        id: int,
        table_number: str,
        capacity: int = 4,
        location: Optional[str] = None,
        status: str = "disponible",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.table_number = table_number
        self.capacity = capacity
        self.location = location
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "table_number": self.table_number,
            "capacity": self.capacity,
            "location": self.location,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_available(self) -> bool:
        """Vérifie si la table est disponible"""
        return self.status == "disponible"
    
    def can_accommodate(self, guest_count: int) -> bool:
        """Vérifie si peut accommoder les invités"""
        return self.capacity >= guest_count


class OrderModel:
    """Modèle de commande restaurant"""
    
    def __init__(
        self,
        id: int,
        order_number: str,
        table_id: int,
        waiter_id: int = None,
        customer_id: Optional[int] = None,
        order_type: str = "sur_place",
        status: str = "nouvelle",
        subtotal: float = 0,
        tax_amount: float = 0,
        discount_amount: float = 0,
        total_amount: float = 0,
        currency: str = "XOF",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_number = order_number
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.customer_id = customer_id
        self.order_type = order_type
        self.status = status
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.total_amount = total_amount
        self.currency = currency
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "table_id": self.table_id,
            "waiter_id": self.waiter_id,
            "customer_id": self.customer_id,
            "order_type": self.order_type,
            "status": self.status,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def calculate_total(self):
        """Calcule le montant total"""
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
    
    def is_served(self) -> bool:
        """Vérifie si servi"""
        return self.status == "servie"
    
    def is_paid(self) -> bool:
        """Vérifie si payé"""
        return self.status == "payee"
