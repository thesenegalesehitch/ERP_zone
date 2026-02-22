"""
Modèle de données pour les entrepôts

Ce module définit le modèle de données pour les entrepôts
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime, date
from typing import Optional


class WarehouseModel:
    """Modèle d'entrepôt"""
    
    def __init__(
        self,
        id: int,
        name: str,
        code: str,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: str = "Sénégal",
        phone: Optional[str] = None,
        email: Optional[str] = None,
        manager_id: Optional[int] = None,
        is_active: bool = True,
        capacity: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.code = code
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.email = email
        self.manager_id = manager_id
        self.is_active = is_active
        self.capacity = capacity
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "phone": self.phone,
            "email": self.email,
            "manager_id": self.manager_id,
            "is_active": self.is_active,
            "capacity": self.capacity,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "WarehouseModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            code=data.get("code"),
            address=data.get("address"),
            city=data.get("city"),
            country=data.get("country", "Sénégal"),
            phone=data.get("phone"),
            email=data.get("email"),
            manager_id=data.get("manager_id"),
            is_active=data.get("is_active", True),
            capacity=data.get("capacity"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active_status(self) -> bool:
        """Vérifie si actif"""
        return self.is_active


class WarehouseSectionModel:
    """Modèle de section d'entrepôt"""
    
    def __init__(
        self,
        id: int,
        warehouse_id: int,
        name: str,
        code: str,
        capacity: Optional[int] = None,
        is_available: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.warehouse_id = warehouse_id
        self.name = name
        self.code = code
        self.capacity = capacity
        self.is_available = is_available
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "warehouse_id": self.warehouse_id,
            "name": self.name,
            "code": self.code,
            "capacity": self.capacity,
            "is_available": self.is_available,
            "notes": self.notes,
            "created_at": self.created_at
        }


class WarehouseLocationModel:
    """Modèle d'emplacement d'entrepôt"""
    
    def __init__(
        self,
        id: int,
        section_id: int,
        aisle: str,
        rack: str,
        shelf: str,
        bin: Optional[str] = None,
        is_available: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.section_id = section_id
        self.aisle = aisle
        self.rack = rack
        self.shelf = shelf
        self.bin = bin
        self.is_available = is_available
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "section_id": self.section_id,
            "aisle": self.aisle,
            "rack": self.rack,
            "shelf": self.shelf,
            "bin": self.bin,
            "is_available": self.is_available,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def location_code(self) -> str:
        """Code d'emplacement"""
        return f"{self.aisle}-{self.rack}-{self.shelf}"
