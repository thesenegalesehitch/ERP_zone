"""
Modèle de données pour les contacts

Ce module définit le modèle de données pour les contacts
dans le module de gestion des clients.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class ContactModel:
    """Modèle de contact"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobile: Optional[str] = None,
        position: Optional[str] = None,
        department: Optional[str] = None,
        is_primary: bool = False,
        is_active: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.mobile = mobile
        self.position = position
        self.department = department
        self.is_primary = is_primary
        self.is_active = is_active
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "position": self.position,
            "department": self.department,
            "is_primary": self.is_primary,
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ContactModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            client_id=data.get("client_id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            mobile=data.get("mobile"),
            position=data.get("position"),
            department=data.get("department"),
            is_primary=data.get("is_primary", False),
            is_active=data.get("is_active", True),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def get_full_name(self) -> str:
        """Retourne le nom complet"""
        return f"{self.first_name} {self.last_name}"
    
    def is_active(self) -> bool:
        """Vérifie si le contact est actif"""
        return self.is_active


class AddressModel:
    """Modèle d'adresse"""
    
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
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
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
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
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
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def get_full_address(self) -> str:
        """Retourne l'adresse complète"""
        parts = []
        if self.street:
            parts.append(self.street)
        if self.postal_code:
            parts.append(self.postal_code)
        if self.city:
            parts.append(self.city)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts)


class ClientNoteModel:
    """Modèle de note client"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        content: str,
        note_type: str = "generale",
        is_private: bool = False,
        created_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.content = content
        self.note_type = note_type
        self.is_private = is_private
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "content": self.content,
            "note_type": self.note_type,
            "is_private": self.is_private,
            "created_by": self.created_by,
            "created_at": self.created_at
        }


class ClientTagModel:
    """Modèle de tag client"""
    
    def __init__(
        self,
        id: int,
        name: str,
        color: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.color = color
        self.description = description
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "description": self.description,
            "created_at": self.created_at
        }


class ClientTagAssignmentModel:
    """Modèle d'assignation de tag"""
    
    def __init__(
        self,
        id: int,
        client_id: int,
        tag_id: int,
        assigned_by: int = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.client_id = client_id
        self.tag_id = tag_id
        self.assigned_by = assigned_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "tag_id": self.tag_id,
            "assigned_by": self.assigned_by,
            "created_at": self.created_at
        }
