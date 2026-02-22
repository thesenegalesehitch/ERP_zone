"""
Modèle de données pour les entrepôts

Ce module définit le modèle de données pour les entrepôts
dans le module de gestion des stocks.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class WarehouseModel:
    """Modèle d'entrepôt"""
    
    def __init__(
        self,
        id: int,
        warehouse_code: str,
        name: str,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: str = "Sénégal",
        phone: Optional[str] = None,
        email: Optional[str] = None,
        capacity: float = 0,
        is_active: bool = True,
        manager_id: Optional[int] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.warehouse_code = warehouse_code
        self.name = name
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.email = email
        self.capacity = capacity
        self.is_active = is_active
        self.manager_id = manager_id
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "warehouse_code": self.warehouse_code,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "phone": self.phone,
            "email": self.email,
            "capacity": self.capacity,
            "is_active": self.is_active,
            "manager_id": self.manager_id,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "WarehouseModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            warehouse_code=data.get("warehouse_code"),
            name=data.get("name"),
            address=data.get("address"),
            city=data.get("city"),
            country=data.get("country", "Sénégal"),
            phone=data.get("phone"),
            email=data.get("email"),
            capacity=data.get("capacity", 0),
            is_active=data.get("is_active", True),
            manager_id=data.get("manager_id"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_active_warehouse(self) -> bool:
        """Vérifie si actif"""
        return self.is_active
    
    def full_address(self) -> str:
        """Adresse complète"""
        parts = [self.address, self.city, self.country]
        return ", ".join([p for p in parts if p])


class ZoneModel:
    """Modèle de zone"""
    
    def __init__(
        self,
        id: int,
        warehouse_id: int,
        name: str,
        zone_code: str,
        zone_type: str = "stockage",
        capacity: float = 0,
        is_active: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.warehouse_id = warehouse_id
        self.name = name
        self.zone_code = zone_code
        self.zone_type = zone_type
        self.capacity = capacity
        self.is_active = is_active
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "warehouse_id": self.warehouse_id,
            "name": self.name,
            "zone_code": self.zone_code,
            "zone_type": self.zone_type,
            "capacity": self.capacity,
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": self.created_at
        }


class LocationModel:
    """Modèle d'emplacement"""
    
    def __init__(
        self,
        id: int,
        warehouse_id: int,
        zone_id: Optional[int] = None,
        location_code: str,
        location_type: str = "rack",
        row: Optional[str] = None,
        column: Optional[str] = None,
        level: Optional[str] = None,
        is_active: bool = True,
        max_weight: float = 0,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.warehouse_id = warehouse_id
        self.zone_id = zone_id
        self.location_code = location_code
        self.location_type = location_type
        self.row = row
        self.column = column
        self.level = level
        self.is_active = is_active
        self.max_weight = max_weight
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "warehouse_id": self.warehouse_id,
            "zone_id": self.zone_id,
            "location_code": self.location_code,
            "location_type": self.location_type,
            "row": self.row,
            "column": self.column,
            "level": self.level,
            "is_active": self.is_active,
            "max_weight": self.max_weight,
            "notes": self.notes,
            "created_at": self.created_at
        }
    
    def full_location(self) -> str:
        """Emplacement complet"""
        parts = [self.row, self.column, self.level]
        return "-".join([p for p in parts if p])
