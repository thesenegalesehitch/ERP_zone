"""
Modèle de données pour le menu

Ce module définit le modèle de données pour le menu
dans le module restaurant.

Ce fichier fait partie du Projet ERP développé pour le Sénégal.
"""
from datetime import datetime
from typing import Optional


class MenuCategoryModel:
    """Modèle de catégorie de menu"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        display_order: int = 0,
        is_active: bool = True,
        available_from: Optional[str] = None,
        available_until: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.display_order = display_order
        self.is_active = is_active
        self.available_from = available_from
        self.available_until = available_until
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "display_order": self.display_order,
            "is_active": self.is_active,
            "available_from": self.available_from,
            "available_until": self.available_until,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MenuCategoryModel":
        """Crée un modèle depuis un dictionnaire"""
        return cls(
            id=data.get("id", 0),
            name=data.get("name"),
            description=data.get("description"),
            display_order=data.get("display_order", 0),
            is_active=data.get("is_active", True),
            available_from=data.get("available_from"),
            available_until=data.get("available_until"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


class MenuItemModel:
    """Modèle d'article du menu"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        category_id: int,
        price: float,
        cost_price: float = 0,
        preparation_time: int = 15,
        calories: Optional[int] = None,
        is_available: bool = True,
        is_vegetarian: bool = False,
        is_vegan: bool = False,
        is_gluten_free: bool = False,
        allergens: Optional[str] = None,
        ingredients: Optional[str] = None,
        image_url: Optional[str] = None,
        display_order: int = 0,
        is_featured: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.category_id = category_id
        self.price = price
        self.cost_price = cost_price
        self.preparation_time = preparation_time
        self.calories = calories
        self.is_available = is_available
        self.is_vegetarian = is_vegetarian
        self.is_vegan = is_vegan
        self.is_gluten_free = is_gluten_free
        self.allergens = allergens
        self.ingredients = ingredients
        self.image_url = image_url
        self.display_order = display_order
        self.is_featured = is_featured
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "price": self.price,
            "cost_price": self.cost_price,
            "preparation_time": self.preparation_time,
            "calories": self.calories,
            "is_available": self.is_available,
            "is_vegetarian": self.is_vegetarian,
            "is_vegan": self.is_vegan,
            "is_gluten_free": self.is_gluten_free,
            "allergens": self.allergens,
            "ingredients": self.ingredients,
            "image_url": self.image_url,
            "display_order": self.display_order,
            "is_featured": self.is_featured,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def profit_margin(self) -> float:
        """Calcule la marge bénéficiaire"""
        if self.price == 0:
            return 0
        return ((self.price - self.cost_price) / self.price) * 100


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
    
    def is_available(self) -> bool:
        """Vérifie si la table est disponible"""
        return self.status == "libre"


class ReservationModel:
    """Modèle de réservation"""
    
    def __init__(
        self,
        id: int,
        customer_name: str,
        customer_phone: str,
        customer_email: Optional[str] = None,
        table_id: Optional[int] = None,
        reservation_date: Optional[datetime] = None,
        party_size: int = 2,
        status: str = "en_attente",
        notes: Optional[str] = None,
        confirmed_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_email = customer_email
        self.table_id = table_id
        self.reservation_date = reservation_date
        self.party_size = party_size
        self.status = status
        self.notes = notes
        self.confirmed_at = confirmed_at
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> dict:
        """Convertit le modèle en dictionnaire"""
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_email": self.customer_email,
            "table_id": self.table_id,
            "reservation_date": self.reservation_date,
            "party_size": self.party_size,
            "status": self.status,
            "notes": self.notes,
            "confirmed_at": self.confirmed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def is_confirmed(self) -> bool:
        """Vérifie si la réservation est confirmée"""
        return self.status == "confirme"
