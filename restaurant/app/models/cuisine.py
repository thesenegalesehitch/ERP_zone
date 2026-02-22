"""
Modèle de données pour la cuisine

Ce module définit le modèle de données pour la cuisine
dans le module restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class KitchenOrderModel:
    """Modèle de commande cuisine"""
    
    def __init__(
        self,
        id: int,
        order_id: int,
        table_id: int,
        status: str = "en_attente",
        priority: str = "normale",
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.order_id = order_id
        self.table_id = table_id
        self.status = status
        self.priority = priority
        self.started_at = started_at
        self.completed_at = completed_at
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "table_id": self.table_id,
            "status": self.status,
            "priority": self.priority,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "KitchenOrderModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            order_id=data.get("order_id"),
            table_id=data.get("table_id"),
            status=data.get("status", "en_attente"),
            priority=data.get("priority", "normale"),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def is_completed(self) -> bool:
        """Vérifie si terminé"""
        return self.status == "termine"
    
    def is_in_progress(self) -> bool:
        """Vérifie si en cours"""
        return self.status == "en_preparation"


class MenuItemModel:
    """Modèle d'article de menu"""
    
    def __init__(
        self,
        id: int,
        menu_category_id: int,
        name: str,
        description: Optional[str] = None,
        price: float = 0,
        currency: str = "XOF",
        preparation_time: int = 15,
        is_available: bool = True,
        is_vegetarian: bool = False,
        is_spicy: bool = False,
        allergens: Optional[str] = None,
        image_url: Optional[str] = None,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.menu_category_id = menu_category_id
        self.name = name
        self.description = description
        self.price = price
        self.currency = currency
        self.preparation_time = preparation_time
        self.is_available = is_available
        self.is_vegetarian = is_vegetarian
        self.is_spicy = is_spicy
        self.allergens = allergens
        self.image_url = image_url
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "menu_category_id": self.menu_category_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "currency": self.currency,
            "preparation_time": self.preparation_time,
            "is_available": self.is_available,
            "is_vegetarian": self.is_vegetarian,
            "is_spicy": self.is_spicy,
            "allergens": self.allergens,
            "image_url": self.image_url,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def get_allergen_list(self) -> list:
        """Liste des allergènes"""
        if not self.allergens:
            return []
        return [a.strip() for a in self.allergens.split(",")]


class IngredientModel:
    """Modèle d'ingrédient"""
    
    def __init__(
        self,
        id: int,
        name: str,
        unit: str = "unite",
        quantity_in_stock: float = 0,
        minimum_stock: float = 0,
        unit_cost: float = 0,
        currency: str = "XOF",
        supplier_id: Optional[int] = None,
        is_active: bool = True,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.unit = unit
        self.quantity_in_stock = quantity_in_stock
        self.minimum_stock = minimum_stock
        self.unit_cost = unit_cost
        self.currency = currency
        self.supplier_id = supplier_id
        self.is_active = is_active
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "quantity_in_stock": self.quantity_in_stock,
            "minimum_stock": self.minimum_stock,
            "unit_cost": self.unit_cost,
            "currency": self.currency,
            "supplier_id": self.supplier_id,
            "is_active": self.is_active,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_low_stock(self) -> bool:
        """Vérifie si stock bas"""
        return self.quantity_in_stock < self.minimum_stock
    
    def stock_value(self) -> float:
        """Valeur du stock"""
        return self.quantity_in_stock * self.unit_cost
