"""
Modèle de données pour les clients

Ce module définit le modèle de données pour les clients
dans le module de gestion des clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class ClientModel:
    """Modèle de client"""
    
    def __init__(
        self,
        id: int,
        client_number: str,
        first_name: str,
        last_name: str,
        company_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: str = "Sénégal",
        client_type: str = "particulier",
        status: str = "actif",
        tax_id: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_number = client_number
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.country = country
        self.client_type = client_type
        self.status = status
        self.tax_id = tax_id
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_number": self.client_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company_name": self.company_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "client_type": self.client_type,
            "status": self.status,
            "tax_id": self.tax_id,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ClientModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            client_number=data.get("client_number"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            company_name=data.get("company_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            city=data.get("city"),
            country=data.get("country", "Sénégal"),
            client_type=data.get("client_type", "particulier"),
            status=data.get("status", "actif"),
            tax_id=data.get("tax_id"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def full_name(self) -> str:
        """Nom complet"""
        if self.company_name:
            return f"{self.first_name} {self.last_name} ({self.company_name})"
        return f"{self.first_name} {self.last_name}"
    
    def is_active(self) -> bool:
        """Vérifie si actif"""
        return self.status == "actif"


class ClientContactModel:
    """Modèle de contact client"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        role: Optional[str] = None,
        is_primary: bool = False,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.role = role
        self.is_primary = is_primary
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "is_primary": self.is_primary,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def full_name(self) -> str:
        """Nom complet"""
        return f"{self.first_name} {self.last_name}"


class ClientAddressModel:
    """Modèle d'adresse client"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        address_type: str = "facturation",
        street: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        postal_code: Optional[str] = None,
        country: str = "Sénégal",
        is_default: bool = False,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.address_type = address_type
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.is_default = is_default
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "address_type": self.address_type,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "is_default": self.is_default,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def full_address(self) -> str:
        """Adresse complète"""
        parts = [self.street, self.city, self.state, self.postal_code, self.country]
        return ", ".join([p for p in parts if p])
