"""
Modèle de données pour les emprunts

Ce module définit le modèle de données pour les emprunts
dans le module librairie.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class BorrowingModel:
    """Modèle d'emprunt"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        book_id: int,
        borrow_date: Optional[date] = None,
        due_date: Optional[date] = None,
        return_date: Optional[date] = None,
        status: str = "emprunte",
        renewal_count: int = 0,
        late_fee: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date or date.today()
        self.due_date = due_date
        self.return_date = return_date
        self.status = status
        self.renewal_count = renewal_count
        self.late_fee = late_fee
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "borrow_date": self.borrow_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status,
            "renewal_count": self.renewal_count,
            "late_fee": self.late_fee,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "BorrowingModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            member_id=data.get("member_id"),
            book_id=data.get("book_id"),
            borrow_date=data.get("borrow_date"),
            due_date=data.get("due_date"),
            return_date=data.get("return_date"),
            status=data.get("status", "emprunte"),
            renewal_count=data.get("renewal_count", 0),
            late_fee=data.get("late_fee", 0),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_returned(self) -> bool:
        """Vérifie si le livre est retourné"""
        return self.status == "retourne"
    
    def is_overdue(self) -> bool:
        """Vérifie si l'emprunt est en retard"""
        if self.is_returned() or not self.due_date:
            return False
        return date.today() > self.due_date
    
    def days_overdue(self) -> int:
        """Calcule les jours de retard"""
        if not self.is_overdue():
            return 0
        delta = date.today() - self.due_date
        return delta.days
    
    def calculate_late_fee(self, daily_rate: float = 100) -> float:
        """Calcule les frais de retard"""
        if not self.is_overdue():
            return 0
        return self.days_overdue() * daily_rate


class ReservationModel:
    """Modèle de réservation"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        book_id: int,
        reservation_date: Optional[date] = None,
        expiry_date: Optional[date] = None,
        status: str = "en_attente",
        notified_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.book_id = book_id
        self.reservation_date = reservation_date or date.today()
        self.expiry_date = expiry_date
        self.status = status
        self.notified_at = notified_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "reservation_date": self.reservation_date,
            "expiry_date": self.expiry_date,
            "status": self.status,
            "notified_at": self.notified_at,
            "created_at": self.created_at
        }
    
    def is_expired(self) -> bool:
        """Vérifie si la réservation est expirée"""
        if not self.expiry_date:
            return False
        return date.today() > self.expiry_date
    
    def is_fulfilled(self) -> bool:
        """Vérifie si la réservation est satisfaite"""
        return self.status == "satisfaite"


class AuthorModel:
    """Modèle d'auteur"""
    
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        biography: Optional[str] = None,
        birth_date: Optional[date] = None,
        death_date: Optional[date] = None,
        country: Optional[str] = None,
        photo_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography
        self.birth_date = birth_date
        self.death_date = death_date
        self.country = country
        self.photo_url = photo_url
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "biography": self.biography,
            "birth_date": self.birth_date,
            "death_date": self.death_date,
            "country": self.country,
            "photo_url": self.photo_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def get_full_name(self) -> str:
        """Retourne le nom complet"""
        return f"{self.first_name} {self.last_name}"


class PublisherModel:
    """Modèle d'éditeur"""
    
    def __init__(
        self,
        id: int,
        name: str,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.email = email
        self.website = website
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
