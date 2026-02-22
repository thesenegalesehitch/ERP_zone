"""
Modèle de données pour les tables

Ce module définit le modèle de données pour les tables
dans le module restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class TableModel:
    """Modèle de table"""
    
    def __init__(
        self,
        id: int,
        table_number: str,
        capacity: int = 4,
        table_type: str = "standard",
        status: str = "libre",
        section: Optional[str] = None,
        position_x: Optional[int] = None,
        position_y: Optional[int] = None,
        is_active: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.table_number = table_number
        self.capacity = capacity
        self.table_type = table_type
        self.status = status
        self.section = section
        self.position_x = position_x
        self.position_y = position_y
        self.is_active = is_active
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "table_number": self.table_number,
            "capacity": self.capacity,
            "table_type": self.table_type,
            "status": self.status,
            "section": self.section,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TableModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            table_number=data.get("table_number"),
            capacity=data.get("capacity", 4),
            table_type=data.get("table_type", "standard"),
            status=data.get("status", "libre"),
            section=data.get("section"),
            position_x=data.get("position_x"),
            position_y=data.get("position_y"),
            is_active=data.get("is_active", True),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_available(self) -> bool:
        """Vérifie si la table est disponible"""
        return self.status == "libre"
    
    def is_occupied(self) -> bool:
        """Vérifie si la table est occupée"""
        return self.status == "occupy"


class TableReservationModel:
    """Modèle de réservation de table"""
    
    def __init__(
        self,
        id: int,
        table_id: int,
        reservation_id: int,
        status: str = "reserve",
        seated_at: Optional[datetime] = None,
        released_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.table_id = table_id
        self.reservation_id = reservation_id
        self.status = status
        self.seated_at = seated_at
        self.released_at = released_at
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "table_id": self.table_id,
            "reservation_id": self.reservation_id,
            "status": self.status,
            "seated_at": self.seated_at,
            "released_at": self.released_at,
            "created_at": self.created_at
        }
    
    def seat(self):
        """ Marque les clients comme installés"""
        self.status = "assis"
        self.seated_at = datetime.now()
    
    def release(self):
        """Libère la table"""
        self.status = "libere"
        self.released_at = datetime.now()


class TableLayoutModel:
    """Modèle de disposition des tables"""
    
    def __init__(
        self,
        id: int,
        name: str,
        floor: str,
        is_active: bool = True,
        layout_config: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.floor = floor
        self.is_active = is_active
        self.layout_config = layout_config
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "floor": self.floor,
            "is_active": self.is_active,
            "layout_config": self.layout_config,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class WaiterModel:
    """Modèle de serveur"""
    
    def __init__(
        self,
        id: int,
        user_id: int,
        employee_id: int,
        section: Optional[str] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.employee_id = employee_id
        self.section = section
        self.is_active = is_active
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "employee_id": self.employee_id,
            "section": self.section,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class TableAssignmentModel:
    """Modèle d'assignation de table"""
    
    def __init__(
        self,
        id: int,
        table_id: int,
        waiter_id: int,
        assigned_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.assigned_at = assigned_at or datetime.now()
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "table_id": self.table_id,
            "waiter_id": self.waiter_id,
            "assigned_at": self.assigned_at,
            "created_at": self.created_at
        }
