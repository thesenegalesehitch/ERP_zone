"""
Modèle de données pour les opérations de librairie

Ce module définit le modèle de données pour les opérations
dans le module de gestion de librairie.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class BorrowingModel:
    """Modèle d'emprunt de livre"""
    
    def __init__(
        self,
        id: int,
        book_id: int,
        member_id: int,
        borrow_date: Optional[date] = None,
        due_date: Optional[date] = None,
        return_date: Optional[date] = None,
        status: str = "en_cours",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "borrow_date": self.borrow_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "BorrowingModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            book_id=data.get("book_id"),
            member_id=data.get("member_id"),
            borrow_date=data.get("borrow_date"),
            due_date=data.get("due_date"),
            return_date=data.get("return_date"),
            status=data.get("status", "en_cours"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_overdue(self) -> bool:
        """Vérifie si l'emprunt est en retard"""
        if self.return_date or not self.due_date:
            return False
        return date.today() > self.due_date
    
    def days_until_due(self) -> int:
        """Jours jusqu'à l'échéance"""
        if not self.due_date:
            return 0
        return (self.due_date - date.today()).days
    
    def days_overdue(self) -> int:
        """Jours de retard"""
        if not self.is_overdue() or not self.due_date:
            return 0
        return (date.today() - self.due_date).days


class ReservationModel:
    """Modèle de réservation de livre"""
    
    def __init__(
        self,
        id: int,
        book_id: int,
        member_id: int,
        reservation_date: Optional[date] = None,
        expiry_date: Optional[date] = None,
        status: str = "en_attente",
        notification_sent: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.book_id = book_id
        self.member_id = member_id
        self.reservation_date = reservation_date
        self.expiry_date = expiry_date
        self.status = status
        self.notification_sent = notification_sent
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "reservation_date": self.reservation_date,
            "expiry_date": self.expiry_date,
            "status": self.status,
            "notification_sent": self.notification_sent,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_expired(self) -> bool:
        """Vérifie si la réservation est expirée"""
        if not self.expiry_date:
            return False
        return date.today() > self.expiry_date
    
    def days_until_expiry(self) -> int:
        """Jours jusqu'à l'expiration"""
        if not self.expiry_date:
            return 0
        return (self.expiry_date - date.today()).days


class LateFeeModel:
    """Modèle de frais de retard"""
    
    def __init__(
        self,
        id: int,
        borrowing_id: int,
        member_id: int,
        amount: float = 0,
        currency: str = "XOF",
        status: str = "en_attente",
        paid_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.borrowing_id = borrowing_id
        self.member_id = member_id
        self.amount = amount
        self.currency = currency
        self.status = status
        self.paid_at = paid_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "borrowing_id": self.borrowing_id,
            "member_id": self.member_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "paid_at": self.paid_at,
            "created_at": self.created_at
        }
    
    def is_paid(self) -> bool:
        """Vérifie si les frais sont payés"""
        return self.status == "paye"
