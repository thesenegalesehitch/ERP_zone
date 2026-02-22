"""
Modèle de données pour les membres de la librairie

Ce module définit le modèle de données pour les membres
dans le module de gestion de librairie.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class MemberModel:
    """Modèle de membre"""
    
    def __init__(
        self,
        id: int,
        member_number: str,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        member_type: str = "standard",
        membership_start: date = None,
        membership_expiry: Optional[date] = None,
        status: str = "actif",
        max_borrow_limit: int = 3,
        current_borrows: int = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_number = member_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.member_type = member_type
        self.membership_start = membership_start
        self.membership_expiry = membership_expiry
        self.status = status
        self.max_borrow_limit = max_borrow_limit
        self.current_borrows = current_borrows
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_number": self.member_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "member_type": self.member_type,
            "membership_start": self.membership_start,
            "membership_expiry": self.membership_expiry,
            "status": self.status,
            "max_borrow_limit": self.max_borrow_limit,
            "current_borrows": self.current_borrows,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MemberModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            member_number=data.get("member_number"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            member_type=data.get("member_type", "standard"),
            membership_start=data.get("membership_start"),
            membership_expiry=data.get("membership_expiry"),
            status=data.get("status", "actif"),
            max_borrow_limit=data.get("max_borrow_limit", 3),
            current_borrows=data.get("current_borrows", 0),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"
    
    def can_borrow(self) -> bool:
        """Vérifie si peut emprunter"""
        return (self.status == "actif" and 
                self.current_borrows < self.max_borrow_limit)
    
    def is_expired(self) -> bool:
        """Vérifie si l'adhésion est expirée"""
        if not self.membership_expiry:
            return False
        return date.today() > self.membership_expiry
    
    def borrow_slots_available(self) -> int:
        """Emplacements d'emprunt disponibles"""
        return self.max_borrow_limit - self.current_borrows


class MemberPaymentModel:
    """Modèle de paiement de membre"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        amount: float = 0,
        currency: str = "XOF",
        payment_type: str = "cotisation",
        payment_date: date = None,
        payment_method: str = "especes",
        reference: Optional[str] = None,
        status: str = "en_attente",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.amount = amount
        self.currency = currency
        self.payment_type = payment_type
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.reference = reference
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "amount": self.amount,
            "currency": self.currency,
            "payment_type": self.payment_type,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
            "reference": self.reference,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def is_paid(self) -> bool:
        """Vérifie si payé"""
        return self.status == "paye"


class MemberCredentialModel:
    """Modèle d'identifiant de membre"""
    
    def __init__(
        self,
        id: int,
        member_id: int,
        credential_type: str = "carte",
        credential_value: str,
        is_active: bool = True,
        issued_date: date = None,
        expiry_date: Optional[date] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.member_id = member_id
        self.credential_type = credential_type
        self.credential_value = credential_value
        self.is_active = is_active
        self.issued_date = issued_date
        self.expiry_date = expiry_date
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "member_id": self.member_id,
            "credential_type": self.credential_type,
            "credential_value": self.credential_value,
            "is_active": self.is_active,
            "issued_date": self.issued_date,
            "expiry_date": self.expiry_date,
            "created_at": self.created_at
        }
    
    def is_valid(self) -> bool:
        """Vérifie si valide"""
        if not self.is_active:
            return False
        if not self.expiry_date:
            return True
        return date.today() <= self.expiry_date
